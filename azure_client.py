"""Azure OpenAI client wrapper for CovenantLens."""
from __future__ import annotations
import os
import base64
import requests
import streamlit as st


def get_azure_config() -> dict:
    """Get Azure config from Streamlit secrets or env vars."""
    # Streamlit Cloud uses st.secrets; local uses .env / env vars
    def get(key, default=""):
        try:
            if key in st.secrets:
                return st.secrets[key]
        except Exception:
            pass
        return os.environ.get(key, default)

    endpoint = get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    # Strip common appendages users sometimes paste
    for suffix in ("/API", "/api", "/openai"):
        if endpoint.endswith(suffix):
            endpoint = endpoint[: -len(suffix)]

    return {
        "endpoint": endpoint,
        "key": get("AZURE_OPENAI_KEY", ""),
        "deployment": get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        "api_version": get("AZURE_OPENAI_API_VERSION", "2024-10-21"),
    }


def is_configured() -> bool:
    cfg = get_azure_config()
    return bool(cfg["endpoint"] and cfg["key"])


def call_azure(messages: list[dict], file_bytes: bytes | None = None, file_name: str | None = None,
               file_mime: str | None = None, system_prompt: str = "", max_tokens: int = 2500,
               temperature: float = 0.3) -> str:
    """
    Call Azure OpenAI chat completions with optional file attachment.

    `messages` should be a list of {"role": "user"|"assistant", "content": "..."}.
    If file_bytes is provided, it's attached to the LAST user message.
    """
    cfg = get_azure_config()
    if not cfg["endpoint"] or not cfg["key"]:
        raise RuntimeError(
            "Azure OpenAI is not configured. Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY "
            "in your environment or Streamlit secrets."
        )

    api_messages: list[dict] = [{"role": "system", "content": system_prompt}]

    for idx, m in enumerate(messages):
        if idx == len(messages) - 1 and m["role"] == "user" and file_bytes is not None:
            content = []
            b64 = base64.b64encode(file_bytes).decode("ascii")
            mime = file_mime or "application/pdf"
            if mime == "application/pdf":
                content.append({
                    "type": "file",
                    "file": {
                        "filename": file_name or "document.pdf",
                        "file_data": f"data:application/pdf;base64,{b64}",
                    },
                })
            elif mime.startswith("image/"):
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime};base64,{b64}"},
                })
            content.append({"type": "text", "text": m["content"]})
            api_messages.append({"role": "user", "content": content})
        else:
            api_messages.append({"role": m["role"], "content": m["content"]})

    url = (
        f"{cfg['endpoint']}/openai/deployments/{cfg['deployment']}/chat/completions"
        f"?api-version={cfg['api_version']}"
    )
    headers = {"Content-Type": "application/json", "api-key": cfg["key"]}
    payload = {
        "messages": api_messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=120)
    if not response.ok:
        raise RuntimeError(f"Azure OpenAI error ({response.status_code}): {response.text[:600]}")

    data = response.json()
    return data["choices"][0]["message"]["content"]
