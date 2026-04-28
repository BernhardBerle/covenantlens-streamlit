"""Bond and covenant dataset for CovenantLens."""

RC = {
    250: "Super Senior Secured",
    251: "Senior Secured",
    252: "Senior Unsecured",
    270: "Subordinated",
}

RC_CLR = {251: "#2563eb", 252: "#9333ea", 250: "#059669", 270: "#dc2626"}

BONDS = [
    {"isin": "NO0013670562", "issuer": "Famkaa Invest ApS", "dis": "2025-10-09", "mat": "2029-04-09", "ccy": "EUR", "amt": 40_000_000, "rc": 252, "cpn": 7.279, "tid": "4a8824f7"},
    {"isin": "NO0013593889", "issuer": "Bulk Infrastructure Group AS", "dis": "2025-06-20", "mat": "2029-12-20", "ccy": "NOK", "amt": 1_750_000_000, "rc": 252, "cpn": 8.6, "tid": "2dfc5416"},
    {"isin": "NO0013526020", "issuer": "Servatur Holding AS", "dis": "2025-04-23", "mat": "2030-04-23", "ccy": "EUR", "amt": 135_000_000, "rc": 251, "cpn": 8.433, "tid": "f2e17260"},
    {"isin": "NO0013513598", "issuer": "Hospitality Invest AS", "dis": "2025-04-07", "mat": "2029-04-07", "ccy": "NOK", "amt": 850_000_000, "rc": 252, "cpn": 9.58, "tid": "f2effc59"},
    {"isin": "NO0013380105", "issuer": "Borås V-tyget 1 AB (publ)", "dis": "2024-10-29", "mat": "2027-04-29", "ccy": "SEK", "amt": 575_000_000, "rc": 251, "cpn": 8.624, "tid": "9297b5ff"},
    {"isin": "NO0013331231", "issuer": "Carucel Property AS", "dis": "2024-09-18", "mat": "2028-09-18", "ccy": "NOK", "amt": 550_000_000, "rc": 252, "cpn": 10.24, "tid": "6f19c378"},
    {"isin": "NO0013318725", "issuer": "AKA AS", "dis": "2024-08-28", "mat": "2029-08-28", "ccy": "NOK", "amt": 280_000_000, "rc": 251, "cpn": 5.65, "tid": "06bf9a7a"},
    {"isin": "NO0013318717", "issuer": "AKA AS", "dis": "2024-08-28", "mat": "2029-08-28", "ccy": "NOK", "amt": 200_000_000, "rc": 251, "cpn": 6.84, "tid": "9d7f260e"},
    {"isin": "NO0013222968", "issuer": "Havila Invest AS", "dis": "2024-04-30", "mat": "2027-04-30", "ccy": "NOK", "amt": 115_000_000, "rc": 251, "cpn": 7.85, "tid": "47a50f72"},
    {"isin": "NO0013013219", "issuer": "Bulk Infrastructure Group AS", "dis": "2023-09-21", "mat": "2028-03-21", "ccy": "NOK", "amt": 1_250_000_000, "rc": 252, "cpn": 10.46, "tid": "7b24b387"},
    {"isin": "NO0012955105", "issuer": "KMC Properties ASA", "dis": "2023-07-06", "mat": "2026-07-06", "ccy": "NOK", "amt": 222_000_000, "rc": 251, "cpn": 9.38, "tid": "f76c375c"},
    {"isin": "NO0012708165", "issuer": "Hospitality Invest AS", "dis": "2022-10-03", "mat": "2025-10-03", "ccy": "NOK", "amt": 700_000_000, "rc": 252, "cpn": 9.9, "tid": "eb0abbda"},
    {"isin": "NO0012698390", "issuer": "AKA AS", "dis": "2022-09-21", "mat": "2027-09-21", "ccy": "NOK", "amt": 480_000_000, "rc": 251, "cpn": 4.92, "tid": "1f047c39"},
    {"isin": "NO0012701269", "issuer": "Bulk Infrastructure Group AS", "dis": "2022-09-15", "mat": "2026-09-15", "ccy": "NOK", "amt": 500_000_000, "rc": 252, "cpn": 9.25, "tid": "95ac3015"},
    {"isin": "NO0012460007", "issuer": "Silver Retail AS", "dis": "2022-03-15", "mat": "2027-03-15", "ccy": "NOK", "amt": 107_000_000, "rc": 251, "cpn": 4.32, "tid": "4905bb4b"},
    {"isin": "NO0011159485", "issuer": "Havila Ariel AS", "dis": "2021-12-06", "mat": "2024-12-06", "ccy": "NOK", "amt": 400_000_000, "rc": 251, "cpn": 6.57, "tid": "d59a790c"},
    {"isin": "NO0011099772", "issuer": "Sunborn London Oyj", "dis": "2021-09-22", "mat": "2027-02-05", "ccy": "EUR", "amt": 25_500_000, "rc": 251, "cpn": 5.5, "tid": "2f598bbc"},
    {"isin": "NO0010915119", "issuer": "Ideco AS", "dis": "2020-12-22", "mat": "2024-06-22", "ccy": "NOK", "amt": 53_940_000, "rc": 251, "cpn": 8.25, "tid": "3869e8ba"},
    {"isin": "NO0010907736", "issuer": "Borgestad ASA", "dis": "2020-12-08", "mat": "2024-01-08", "ccy": "NOK", "amt": 300_000_000, "rc": 251, "cpn": 8.35, "tid": "ea57a93c"},
]

COV = {
    "4a8824f7": {"m": [{"n": "Net LTV Ratio", "t": "< 65%"}, {"n": "Interest Coverage Ratio", "t": "≥ 1.25x"}, {"n": "Liquidity", "t": "≥ DKK 45M (incl. up to DKK 15M unused overdraft)"}], "i": [{"n": "Incurrence Test – Net LTV", "t": "< 55%"}, {"n": "Incurrence Test – ICR", "t": "≥ 1.55x"}, {"n": "Distribution Test – Net LTV", "t": "≤ 50%"}, {"n": "Distribution Test – ICR", "t": "≥ 1.75x"}], "defs": "Net LTV Ratio, Interest Coverage Ratio, Liquidity, Total Net Debt, Market Value, Adjusted EBITDA, Net Interest Cost, Adjusted Group, Relevant Period, Cure Amount", "cure": "Max 2 cures, no consecutive Quarter Dates", "freq": "Quarterly (each Quarter Date, first Q4 2025)"},
    "2dfc5416": {"m": [{"n": "Equity Ratio", "t": "≥ 35%"}, {"n": "Interest Cover Ratio (post replacement)", "t": "≥ 1.50x"}], "i": [{"n": "Equity Ratio (pre replacement)", "t": "≥ 45%"}, {"n": "Interest Cover Ratio (post replacement)", "t": "≥ 1.75x"}, {"n": "Distribution restriction", "t": "Incurrence Test must be met pro forma"}], "defs": "Equity Ratio, Interest Coverage Ratio, EBITDA, Net Interest Expense, Total Assets, Total Equity", "cure": "One-time Financial Covenant Replacement option", "freq": "Quarterly"},
    "f2e17260": {"m": [{"n": "Liquidity", "t": "≥ EUR 10M"}, {"n": "Interest Cover Ratio", "t": "≥ 2.00x"}], "i": [{"n": "Leverage Ratio (Non-recourse)", "t": "≤ 2.50x (gross)"}, {"n": "Leverage Ratio (All debt / Tap)", "t": "≤ 4.00x (net)"}], "defs": "Liquidity, Interest Cover Ratio, Leverage Ratio, Total Debt, Adjusted EBITDA, EBITDA, Net Finance Charges, Cash and Cash Equivalents", "cure": "Max 3 cures, max 2 consecutive", "freq": "Each Reporting Date"},
    "f2effc59": {"m": [{"n": "Book Equity", "t": "≥ NOK 550M"}, {"n": "Cash and Cash Equivalents", "t": "≥ NOK 30M"}], "i": [{"n": "Book Equity for Tap Issue", "t": "≥ NOK 1,000M (pro forma)"}, {"n": "Net Debt to Capital Ratio for Tap", "t": "≤ 50% (pro forma)"}], "defs": "Book Equity, Cash and Cash Equivalents, Net Debt, Capital, Net Debt to Capital Ratio, Quarter Date, GAAP", "cure": "Max 2 cures, no consecutive", "freq": "Quarterly"},
    "9297b5ff": {"m": [{"n": "LTV Ratio", "t": "≤ 75%"}], "i": [{"n": "Permitted Distribution LTV", "t": "< 65% + max SEK 10M/year"}], "defs": "LTV Ratio, Net Interest-Bearing Debt, Market Value, Distribution, Permitted Distribution", "cure": "None specified", "freq": "Annual"},
    "6f19c378": {"m": [{"n": "LTV Ratio", "t": "< 75%"}, {"n": "Liquidity", "t": "≥ NOK 30M"}], "i": [{"n": "Incurrence Test LTV", "t": "< 65%"}], "defs": "LTV Ratio, Liquidity, Total Net Debt, Total Market Value, Incurrence Test, Cure Amount", "cure": "Max 1 cure during entire bond term", "freq": "Quarterly"},
    "06bf9a7a": {"m": [{"n": "Rentedekningsgrad (ICR)", "t": "≥ 2.0x"}, {"n": "LTV", "t": "< 75%"}], "i": [{"n": "Dividend restriction at LTV", "t": "LTV ≤ 75% (valuation max 3mo old)"}, {"n": "Tap Issue LTV", "t": "Must be met post-issuance"}], "defs": "Rentedekningsgrad, LTV", "cure": "5 Business Day cure (pledge cash at A-rated bank)", "freq": "Annual"},
    "9d7f260e": {"m": [{"n": "Rentedekningsgrad (ICR)", "t": "≥ 2.0x"}, {"n": "LTV", "t": "< 75%"}], "i": [{"n": "Dividend restriction at LTV", "t": "LTV ≤ 75% (valuation max 3mo old)"}, {"n": "Tap Issue LTV", "t": "Must be met post-issuance"}], "defs": "Rentedekningsgrad, LTV. Bondholders (2/3) can demand extra valuation.", "cure": "5 Business Day cure (pledge cash at A-rated bank)", "freq": "Annual"},
    "47a50f72": {"m": [{"n": "Loan-to-Value Ratio", "t": "≤ 75%"}, {"n": "Min Book Equity Ratio (Parent)", "t": "≥ 30%"}], "i": [{"n": "Distribution LTV", "t": "≤ 65%"}, {"n": "Distribution ICR", "t": "≥ 1.75x"}], "defs": "LTV Ratio, Book Equity Ratio, Interest Cover Ratio, EBITDA, Liquidity, Market Value, Distribution", "cure": "Trustee can request additional valuation", "freq": "Annual (31 Dec)"},
    "7b24b387": {"m": [{"n": "Equity Ratio", "t": "≥ 35%"}], "i": [{"n": "Distribution Incurrence Test", "t": "Equity Ratio ≥ 45% (pro forma)"}], "defs": "Equity Ratio, Distribution, Compliance Certificate", "cure": "None specified", "freq": "Quarterly"},
    "f76c375c": {"m": [{"n": "Interest Cover Ratio", "t": "≥ 1.5x"}, {"n": "Net LTV Ratio", "t": "< 75%"}, {"n": "Liquidity", "t": "≥ 3mo Net Interest Costs"}, {"n": "LTV Ratio (Property Group)", "t": "< 75%"}], "i": [{"n": "Distribution – Net LTV", "t": "< 65%"}, {"n": "Distribution – Liquidity", "t": "> 1.5x minimum"}, {"n": "Tap Issue – LTV", "t": "< 65%"}, {"n": "Tap Issue – Acquisition LTV", "t": "≤ 60%"}], "defs": "ICR, Net LTV, Liquidity, LTV, Net Interest Bearing Debt, Aggregated Market Value, EBITDA", "cure": "Equity cure (ICR & Net LTV). LTV not curable.", "freq": "Quarterly"},
    "eb0abbda": {"m": [{"n": "Book Equity", "t": "≥ NOK 550M (unconsol.)"}, {"n": "Cash and Cash Equivalents", "t": "≥ NOK 30M (unconsol.)"}], "i": [], "defs": "Book Equity, Cash and Cash Equivalents, GAAP", "cure": "None specified", "freq": "Quarterly"},
    "1f047c39": {"m": [{"n": "Rentedekningsgrad (ICR)", "t": "≥ 2.0x"}, {"n": "LTV", "t": "< 75%"}], "i": [{"n": "Tap Issue LTV", "t": "Must be met post-issuance"}, {"n": "Subsidiary debt cap", "t": "≤ 20% consolidated book assets"}], "defs": "Rentedekningsgrad, LTV", "cure": "5 Business Day cure", "freq": "Annual"},
    "95ac3015": {"m": [{"n": "Equity Ratio", "t": "≥ 35%"}], "i": [{"n": "Distribution Incurrence Test", "t": "Equity Ratio ≥ 45% (pro forma)"}], "defs": "Equity Ratio, Total Assets, Total Equity, Distribution. Green bond.", "cure": "None specified", "freq": "Quarterly"},
    "4905bb4b": {"m": [{"n": "LTV Maximum", "t": "≤ 75%"}], "i": [{"n": "Dividend/Group Contribution LTV", "t": "LTV ≤ 70%"}], "defs": "LTV (annual valuation). Norwegian-language terms.", "cure": "3 month cure: repay bonds (2/3 vote) or post additional security", "freq": "Annual"},
    "3869e8ba": {"m": [{"n": "LTV", "t": "≤ 70%"}], "i": [], "defs": "LTV (Adjusted Book Assets / Net Debt)", "cure": "None specified", "freq": "With Financial Reports"},
    "d59a790c": {"m": [], "i": [], "defs": "No covenants (amendment)", "cure": "N/A", "freq": "N/A"},
    "2f598bbc": {"m": [], "i": [], "defs": "No covenants (amendment)", "cure": "N/A", "freq": "N/A"},
    "ea57a93c": {"m": [], "i": [], "defs": "No covenants (amendment)", "cure": "N/A", "freq": "N/A"},
}


def fmt_amount(n: float, ccy: str) -> str:
    if n >= 1e9:
        return f"{ccy} {n/1e9:.1f}B"
    if n >= 1e6:
        return f"{ccy} {n/1e6:.0f}M"
    return f"{ccy} {n:,.0f}"


def has_covenants(tid: str) -> bool:
    c = COV.get(tid)
    return bool(c and (c.get("m") or c.get("i")))


def build_system_prompt() -> str:
    """Build the system prompt with the full dataset embedded."""
    sections = []
    for b in BONDS:
        c = COV.get(b["tid"], {})
        m_lines = "\n".join(f"  M: {x['n']} → {x['t']}" for x in c.get("m", [])) or "  No maintenance covenants"
        i_lines = "\n".join(f"  I: {x['n']} → {x['t']}" for x in c.get("i", [])) or "  No incurrence covenants"
        sections.append(
            f"{b['issuer']} | {b['isin']} | {RC[b['rc']]} | {b['ccy']} {b['amt']} | {b['cpn']}% | {b['dis']}→{b['mat']}\n"
            f"{m_lines}\n{i_lines}\n"
            f"  Defs: {c.get('defs', 'N/A')} | Cure: {c.get('cure', 'N/A')} | Testing: {c.get('freq', 'N/A')}"
        )
    data = "\n---\n".join(sections)

    return f"""You are CovenantLens, an expert analyst for Norwegian high-yield real estate bond covenants. You have complete data on {len(BONDS)} bonds in the existing database.

CAPABILITIES:
1. Answer questions about the existing bond covenant dataset
2. When a user uploads a PDF document, extract its financial covenants and compare them against the existing dataset
3. Score and rank covenant packages on the **Issuer-Investor Friendliness Spectrum**

WHEN ANALYZING AN UPLOADED DOCUMENT — STRUCTURE YOUR RESPONSE AS FOLLOWS:

## 1. Extracted Covenants
List all maintenance and incurrence covenants found in the document with exact thresholds, plus testing frequency and cure provisions.

## 2. Issuer-Investor Friendliness Score
Provide a score from **1 (extremely investor-friendly / tight)** to **10 (extremely issuer-friendly / loose)**, with a one-line justification.

Scoring criteria (lower score = more investor-friendly):
- **Tight financial thresholds** (low LTV cap, high ICR floor, high equity ratio) → investor-friendly
- **Multiple maintenance covenants** vs only incurrence-based → investor-friendly
- **Quarterly testing** vs annual → investor-friendly
- **Limited or no cure rights** → investor-friendly
- **Strict distribution / dividend tests** → investor-friendly

## 3. Comparison Against Database
Identify the 3 most similar bonds in the database (by seniority, size, currency, covenant type) and compare in a markdown table:
- Where the new document is MORE restrictive (more investor-friendly)
- Where the new document is LESS restrictive (more issuer-friendly)

## 4. Notable Observations
Any unusual provisions, missing standard covenants, or red flags.

GENERAL FORMATTING:
- Use ## for section headers, ** for bold, • or - for bullets
- Be concise and analytical — quote specific thresholds and ISINs
- Do not editorialize beyond the data

EXISTING DATABASE:
{data}"""
