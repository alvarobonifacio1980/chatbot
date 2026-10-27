"""Integração OpenAI isolada da interface Streamlit.

Configure OPENAI_API_KEY no ambiente ou nos secrets do Streamlit.
Nunca envie credenciais ao navegador ou ao repositório.
"""
from __future__ import annotations

from chat_core import api_messages

def responder(topic: str, history: list[dict[str, str]], api_key: str, model: str = "gpt-4.1-mini") -> str:
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não configurada.")
    from openai import OpenAI
    client = OpenAI(api_key=api_key, timeout=30.0, max_retries=1)
    result = client.chat.completions.create(
        model=model,
        messages=api_messages(topic, history),
        temperature=0.3,
        max_tokens=350,
    )
    text = (result.choices[0].message.content or "").strip()
    if not text:
        raise RuntimeError("O provedor não retornou uma resposta.")
    return text
