import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_last_error = None


def get_last_error():
    global _last_error
    return _last_error


def get_api_key():
    # 1. Check local environment / .env
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key.strip()

    # 2. Check Streamlit Cloud secrets (or .streamlit/secrets.toml)
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            return str(st.secrets["GROQ_API_KEY"]).strip()
    except Exception:
        pass

    return None


def get_client():
    global _last_error
    api_key = get_api_key()
    if not api_key:
        _last_error = "GROQ_API_KEY is not set. Please add it to your .env file or Streamlit Cloud Secrets."
        print(f"WARNING: {_last_error}")
        return None

    try:
        return Groq(api_key=api_key)
    except Exception as e:
        _last_error = f"Failed to initialize Groq client: {e}"
        print(f"ERROR: {_last_error}")
        return None


# Module-level client instance (for backwards compatibility)
client = get_client()


def call_claude(prompt, max_tokens=1024):
    global _last_error
    # Dynamically fetch client so runtime key updates / secrets are detected
    active_client = get_client()
    if active_client is None:
        print("ERROR: Groq client is not set up. Check your .env file or Streamlit secrets.")
        return None

    try:
        # model: llama-3.3-70b-versatile is fast and capable for structured tasks.
        response = active_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=max_tokens,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        _last_error = str(e)
        print(f"ERROR: Something went wrong calling Groq: {e}")
        return None


if __name__ == "__main__":
    print("Testing Groq connection...")
    response = call_claude("Say hello and tell me today's date. Reply in one sentence.")

    if response:
        print("SUCCESS! Groq says:")
        print(response)
    else:
        print("FAILED — check the error message above.")
        if _last_error:
            print(f"Reason: {_last_error}")
