# -------------------------
# 🤖 AI AGENT (PRODUCTION SAFE)
# -------------------------

import os

# Try importing Groq safely
try:
    from groq import Groq
except ImportError:
    Groq = None

# Optional: for Streamlit secrets
try:
    import streamlit as st
except:
    st = None


def get_api_key():
    """
    Get API key from environment or Streamlit secrets
    """
    # 1. Try environment variable
    api_key = os.getenv("GROQ_API_KEY")

    # 2. Try Streamlit secrets (for cloud)
    if not api_key and st is not None:
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except:
            pass

    return api_key


def ask_llm(prompt: str) -> str:
    """
    Send prompt to Groq LLM and return response safely
    """

    try:
        # -------------------------
        # 🔐 GET API KEY
        # -------------------------
        api_key = get_api_key()

        if not api_key:
            return "⚠️ AI unavailable: Missing GROQ_API_KEY (set in .env or Streamlit Secrets)"

        # -------------------------
        # 📦 CHECK GROQ INSTALL
        # -------------------------
        if Groq is None:
            return "⚠️ AI unavailable: 'groq' package not installed"

        # -------------------------
        # 🤖 INIT CLIENT
        # -------------------------
        client = Groq(api_key=api_key)

        # -------------------------
        # 💬 CALL MODEL
        # -------------------------
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ stable model
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        # -------------------------
        # 🛡️ FAIL-SAFE (NO CRASH)
        # -------------------------
        return f"⚠️ AI temporarily unavailable: {str(e)}"