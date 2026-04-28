"""CovenantLens — Streamlit edition.

Norwegian high-yield real estate bond covenant intelligence.
Tabs: Search & Compare, Trends, Q&A (with drag-and-drop PDF analysis).
"""
from __future__ import annotations
import io
import streamlit as st
import pandas as pd

from data import BONDS, COV, RC, RC_CLR, fmt_amount, has_covenants, build_system_prompt
from azure_client import call_azure, is_configured, get_azure_config

# ─────────────────────────────────────────────────────────────────────────────
# Page config + styling
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CovenantLens",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .main .block-container { padding-top: 1rem; max-width: 1400px; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; }
    .stTabs [data-baseweb="tab"] { padding: 8px 16px; }
    .badge {
        display: inline-block; padding: 2px 8px; border-radius: 4px;
        font-size: 11px; font-weight: 600; letter-spacing: 0.3px;
        white-space: nowrap; margin-right: 4px;
    }
    .bond-card-title { font-weight: 700; font-size: 15px; }
    .bond-card-isin { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #888; }
    .threshold { font-family: 'IBM Plex Mono', monospace; font-weight: 700; }
    div[data-testid="stStatusWidget"] { display: none; }
</style>
""", unsafe_allow_html=True)

DEFAULT_DOC_PROMPT = """Analyze this bond terms document and provide:

**1. Extracted Covenants** — list all maintenance and incurrence covenants with exact thresholds, plus testing frequency and cure provisions.

**2. Issuer-Investor Friendliness Score (1-10)** — rank this bond on the spectrum where 1 = extremely investor-friendly (tight covenants, low LTV, high ICR, minimal cure rights, quarterly testing) and 10 = extremely issuer-friendly (loose thresholds, generous cures, annual or no testing). Provide a one-line justification.

**3. Comparison Against Database** — identify the 3 most similar bonds in the database and compare. For each comparator, note where the new document is MORE or LESS restrictive in a markdown table.

**4. Notable Observations** — unusual provisions, missing standard covenants, or red flags."""


def badge(text: str, color: str) -> str:
    return f'<span class="badge" style="color:{color};background:{color}1a">{text}</span>'


# ─────────────────────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────────────────────
header_l, header_r = st.columns([3, 2])
with header_l:
    st.markdown("# 📊 CovenantLens")
    st.caption(f"Norwegian RE Bonds · {len(BONDS)} issues · AI-powered covenant analysis")
with header_r:
    cfg = get_azure_config()
    if is_configured():
        st.success(f"✓ Azure connected · {cfg['deployment']}", icon="🟢")
    else:
        st.warning("⚠ Azure not configured — set credentials in env or secrets", icon="🟡")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────────────────────────────────────
tab_search, tab_trends, tab_chat = st.tabs(["🔍 Search & Compare", "📈 Trends", "💬 Q&A"])


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — SEARCH & COMPARE
# ═════════════════════════════════════════════════════════════════════════════
with tab_search:
    f1, f2, f3, f4, f5 = st.columns([2, 1, 1, 1, 1])
    with f1:
        search = st.text_input("Search", placeholder="Issuer or ISIN...", label_visibility="collapsed")
    with f2:
        f_rc = st.selectbox("Seniority", ["All", "Secured", "Unsecured"], label_visibility="collapsed")
    with f3:
        f_ccy = st.selectbox("Currency", ["All", "NOK", "EUR", "SEK"], label_visibility="collapsed")
    with f4:
        f_cov = st.selectbox("Covenants", ["All", "Has covenants", "No covenants"], label_visibility="collapsed")
    with f5:
        sort_by = st.selectbox("Sort", ["Newest", "Coupon ↓", "Size ↓", "A–Z"], label_visibility="collapsed")

    # Apply filters
    rows = list(BONDS)
    if search:
        s = search.lower()
        rows = [b for b in rows if s in b["issuer"].lower() or s in b["isin"].lower()]
    if f_rc == "Secured":
        rows = [b for b in rows if b["rc"] == 251]
    elif f_rc == "Unsecured":
        rows = [b for b in rows if b["rc"] == 252]
    if f_ccy != "All":
        rows = [b for b in rows if b["ccy"] == f_ccy]
    if f_cov == "Has covenants":
        rows = [b for b in rows if has_covenants(b["tid"])]
    elif f_cov == "No covenants":
        rows = [b for b in rows if not has_covenants(b["tid"])]
    sort_key = {
        "Newest": lambda b: b["dis"],
        "Coupon ↓": lambda b: b["cpn"],
        "Size ↓": lambda b: b["amt"],
        "A–Z": lambda b: b["issuer"],
    }[sort_by]
    rows.sort(key=sort_key, reverse=(sort_by != "A–Z"))

    st.caption(f"{len(rows)} bonds")

    left, right = st.columns([1, 1.2])

    with left:
        # Summary table
        df = pd.DataFrame([{
            "Issuer": b["issuer"],
            "ISIN": b["isin"],
            "Seniority": RC[b["rc"]],
            "Amount": fmt_amount(b["amt"], b["ccy"]),
            "Coupon": f"{b['cpn']}%",
            "Maturity": b["mat"],
            "Covenants": "✓" if has_covenants(b["tid"]) else "—",
        } for b in rows])
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            key="bond_selector",
        )

    with right:
        sel = st.session_state.get("bond_selector", {}).get("selection", {}).get("rows", [])
        if sel and rows:
            bond = rows[sel[0]]
            cov = COV.get(bond["tid"], {})

            st.markdown(f"### {bond['issuer']}")
            st.caption(bond["isin"])

            badge_html = (
                badge(RC[bond["rc"]], RC_CLR[bond["rc"]])
                + badge(fmt_amount(bond["amt"], bond["ccy"]), "#2563eb")
                + badge(f"{bond['cpn']}%", "#9333ea")
                + badge(f"{bond['dis']} → {bond['mat']}", "#6b7280")
            )
            st.markdown(badge_html, unsafe_allow_html=True)
            st.write("")

            if not has_covenants(bond["tid"]):
                st.warning("⚠ No financial covenants extracted (likely an amendment agreement).")
            else:
                if cov.get("m"):
                    st.markdown("##### 🛡️ Maintenance Covenants")
                    for x in cov["m"]:
                        c1, c2 = st.columns([2, 1])
                        with c1:
                            st.write(f"**{x['n']}**")
                        with c2:
                            st.markdown(f"<div class='threshold' style='color:#059669;text-align:right'>{x['t']}</div>", unsafe_allow_html=True)

                if cov.get("i"):
                    st.markdown("##### 📈 Incurrence Covenants")
                    for x in cov["i"]:
                        c1, c2 = st.columns([2, 1])
                        with c1:
                            st.write(f"**{x['n']}**")
                        with c2:
                            st.markdown(f"<div class='threshold' style='color:#d97706;text-align:right'>{x['t']}</div>", unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Testing Frequency**")
                    st.caption(cov.get("freq", "N/A"))
                with col_b:
                    st.markdown("**Cure Provisions**")
                    st.caption(cov.get("cure", "N/A"))

                st.markdown("**Key Definitions**")
                st.caption(cov.get("defs", "N/A"))
        else:
            st.info("👈 Select a bond from the table to see its covenant breakdown")


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — TRENDS
# ═════════════════════════════════════════════════════════════════════════════
with tab_trends:
    st.markdown("### Covenant Trends")
    st.caption(f"Patterns across {len(BONDS)} Norwegian RE bonds")

    bonds_with_cov = [b for b in BONDS if has_covenants(b["tid"])]

    # Stats
    sec = [b for b in bonds_with_cov if b["rc"] == 251]
    unsec = [b for b in bonds_with_cov if b["rc"] == 252]
    sec_avg = sum(len(COV[b["tid"]]["m"]) + len(COV[b["tid"]]["i"]) for b in sec) / max(1, len(sec))
    unsec_avg = sum(len(COV[b["tid"]]["m"]) + len(COV[b["tid"]]["i"]) for b in unsec) / max(1, len(unsec))

    s1, s2, s3 = st.columns(3)
    s1.metric("Bonds with covenants", f"{len(bonds_with_cov)}/{len(BONDS)}")
    s2.metric("Avg covenants (Secured)", f"{sec_avg:.1f}")
    s3.metric("Avg covenants (Unsecured)", f"{unsec_avg:.1f}")

    st.write("")

    # Maintenance covenant type frequency
    metrics: dict[str, int] = {}
    for b in bonds_with_cov:
        for x in COV[b["tid"]]["m"]:
            n = x["n"]
            if "LTV" in n or "Loan-to-Value" in n:
                k = "LTV"
            elif "Equity" in n:
                k = "Equity Ratio"
            elif "Interest" in n or "Rentedekning" in n:
                k = "Interest Coverage"
            elif "Liquidity" in n or "Cash" in n:
                k = "Liquidity / Cash"
            elif "Book Equity" in n:
                k = "Book Equity"
            else:
                k = n
            metrics[k] = metrics.get(k, 0) + 1

    metric_df = pd.DataFrame(
        sorted(metrics.items(), key=lambda x: -x[1]),
        columns=["Metric", "Count"],
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Most common maintenance covenant types")
        st.bar_chart(metric_df.set_index("Metric"), height=320)

    with c2:
        st.markdown("##### LTV thresholds over time")
        ltv_rows = []
        for b in sorted(bonds_with_cov, key=lambda b: b["dis"]):
            ltv = next((x for x in COV[b["tid"]]["m"] if "LTV" in x["n"] or "Loan-to-Value" in x["n"]), None)
            if ltv:
                # Extract numeric threshold
                num = "".join(ch for ch in ltv["t"] if ch.isdigit() or ch == ".")
                try:
                    val = float(num) if num else None
                except ValueError:
                    val = None
                ltv_rows.append({
                    "Issued": b["dis"][:7],
                    "Issuer": b["issuer"][:30],
                    "LTV cap (%)": val,
                    "Threshold": ltv["t"],
                })
        if ltv_rows:
            ltv_df = pd.DataFrame(ltv_rows)
            st.line_chart(
                ltv_df.set_index("Issued")[["LTV cap (%)"]],
                height=320,
            )
            with st.expander("LTV detail by issuer"):
                st.dataframe(ltv_df, use_container_width=True, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — Q&A WITH PDF DROP
# ═════════════════════════════════════════════════════════════════════════════
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = build_system_prompt()

    # File uploader
    upl_col, btn_col = st.columns([4, 1])
    with upl_col:
        uploaded_file = st.file_uploader(
            "Drop a bond terms PDF for friendliness scoring + database comparison",
            type=["pdf", "png", "jpg", "jpeg", "webp"],
            help="Auto-extracts covenants, scores 1-10 friendliness, and compares against the database",
            label_visibility="visible",
        )
    with btn_col:
        st.write("")
        st.write("")
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # Suggestion chips when chat is empty
    if not st.session_state.messages and not uploaded_file:
        st.markdown("##### Try asking:")
        suggestions = [
            "Compare all LTV covenants across the dataset",
            "How do AKA's covenants differ across their 3 bonds?",
            "Rank all bonds by investor-friendliness",
            "Summarize Bulk Infrastructure's covenant evolution",
            "Compare cure provisions — which is tightest?",
            "Secured vs unsecured: typical covenant package?",
        ]
        s_cols = st.columns(3)
        for i, s in enumerate(suggestions):
            with s_cols[i % 3]:
                if st.button(s, key=f"sug_{i}", use_container_width=True):
                    st.session_state.pending_input = s
                    st.rerun()

    # Render existing messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # If a file is uploaded, pre-populate the prompt and offer Send
    pending_text = st.session_state.pop("pending_input", None)

    if uploaded_file is not None:
        st.info(f"📄 **{uploaded_file.name}** ready to analyze. Edit the prompt below if you want, then hit Send.")
        default_prompt = pending_text or DEFAULT_DOC_PROMPT
        with st.form(key="file_form", clear_on_submit=True):
            user_prompt = st.text_area(
                "Analysis prompt",
                value=default_prompt,
                height=200,
                label_visibility="collapsed",
            )
            submitted = st.form_submit_button("📨 Send for analysis", use_container_width=True, type="primary")
        if submitted and user_prompt.strip():
            file_bytes = uploaded_file.getvalue()
            file_name = uploaded_file.name
            file_mime = uploaded_file.type or "application/pdf"
            display_msg = f"📄 *{file_name}*\n\n{user_prompt}"
            st.session_state.messages.append({"role": "user", "content": display_msg})

            api_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[:-1]
            ]
            api_messages.append({"role": "user", "content": user_prompt})

            with st.chat_message("user"):
                st.markdown(display_msg)
            with st.chat_message("assistant"):
                with st.spinner("Reading document and analyzing covenants..."):
                    try:
                        reply = call_azure(
                            messages=api_messages,
                            file_bytes=file_bytes,
                            file_name=file_name,
                            file_mime=file_mime,
                            system_prompt=st.session_state.system_prompt,
                        )
                    except Exception as e:
                        reply = f"❌ Error: {e}"
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
    else:
        # Standard chat input (no file)
        prompt = pending_text or st.chat_input("Ask about covenants, compare bonds, explore trends...")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    try:
                        reply = call_azure(
                            messages=api_messages,
                            system_prompt=st.session_state.system_prompt,
                        )
                    except Exception as e:
                        reply = f"❌ Error: {e}"
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
