# CovenantLens (Streamlit)

Norwegian high-yield real estate bond covenant intelligence — Streamlit edition.

Search, compare, and analyze 19 Norwegian RE bonds with AI-powered Q&A. Drop a bond terms PDF and get automatic covenant extraction, friendliness scoring (1-10), and ranking against the database.

## Features

- 🔍 **Search & Compare** — filter, sort, and inspect bond covenants
- 📈 **Trends** — covenant frequency, LTV thresholds over time
- 💬 **Q&A** — natural language analysis powered by Azure OpenAI (`gpt-4o`)
- 📄 **PDF drag-and-drop** — covenant extraction + investor-friendliness scoring + database comparison
- 🔒 **Secrets-managed credentials** — API key never in code

## Three ways to run it

### Option A — Streamlit Community Cloud (free, public)

1. Push this repo to GitHub (private is fine — the app can still deploy)
2. Go to https://share.streamlit.io and sign in with GitHub
3. Click **New app**, select your repo, branch `main`, main file `app.py`
4. Click **Advanced settings** → **Secrets** and paste:
   ```toml
   AZURE_OPENAI_ENDPOINT = "https://nt-openai-4o-test.openai.azure.com"
   AZURE_OPENAI_KEY = "your-key-here"
   AZURE_OPENAI_DEPLOYMENT = "gpt-4o"
   AZURE_OPENAI_API_VERSION = "2024-10-21"
   ```
5. Click **Deploy**. Wait ~2 minutes.

> ⚠ **Note for Azure VNet-restricted resources**: Streamlit Cloud egress IPs are AWS-based. If your Azure resource has a Virtual Network restriction, you'll need IT to whitelist Streamlit Cloud's IP ranges or use a public-endpoint Azure resource.

### Option B — GitHub Codespace

1. Open the repo in a Codespace (Code → Codespaces → Create codespace)
2. The devcontainer auto-installs dependencies
3. Set up secrets:
   ```bash
   mkdir -p .streamlit
   nano .streamlit/secrets.toml
   ```
   Paste your Azure credentials (see template above), save with `Ctrl+O`, `Enter`, `Ctrl+X`.
4. Run:
   ```bash
   streamlit run app.py
   ```
5. Codespace will forward port `8501` — click the popup or the PORTS tab.

### Option C — Local

You'll need Python 3.10+ installed.

```bash
git clone <your-repo>
cd covenantlens-streamlit
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your Azure credentials
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

## Project structure

```
covenantlens-streamlit/
├── app.py                          # Main Streamlit app (3 tabs)
├── data.py                         # Bonds, covenants, system prompt builder
├── azure_client.py                 # Azure OpenAI wrapper (text + PDF + image)
├── requirements.txt
├── .streamlit/
│   ├── config.toml                 # Theme + server settings
│   └── secrets.toml.example        # Template (do NOT commit your real secrets.toml)
├── .devcontainer/
│   └── devcontainer.json           # Codespace auto-setup
└── .gitignore
```

## How the friendliness scoring works

When you upload a PDF, the chat auto-fills a structured prompt that asks for:

1. **Extracted Covenants** — full list with thresholds, testing frequency, cure provisions
2. **Issuer-Investor Friendliness Score (1-10)** — 1 = extremely investor-friendly (tight thresholds, quarterly testing, minimal cures), 10 = extremely issuer-friendly (loose, generous cures, annual testing)
3. **Comparison Against Database** — markdown table comparing the new doc against the 3 most similar bonds, noting where it's more or less restrictive
4. **Notable Observations** — unusual provisions, missing standard covenants, red flags

You can edit the prompt before hitting Send if you want to focus the analysis differently.

## Common issues

- **"Azure not configured"** — secrets missing. On Cloud: App settings → Secrets. Locally: `.streamlit/secrets.toml`.
- **403 from Azure with VNet message** — your Azure resource has IP restrictions. Either whitelist the deployment platform's IPs (ask IT), or run from an approved network.
- **404 from Azure** — your `AZURE_OPENAI_DEPLOYMENT` doesn't match what's in Azure. Check Azure portal → Deployments.
- **PDF not being read correctly** — `gpt-4o` supports PDFs natively but very large or scanned PDFs may need OCR pre-processing first.
