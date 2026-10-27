"""Assistente educacional de investimentos — Streamlit."""
from __future__ import annotations

import os

import streamlit as st

from chat_core import TOPICS, WELCOME, fresh_history, validate_prompt, MAX_INPUT_CHARS
from modelo_openai import responder

st.set_page_config(page_title="Chatbot Financeiro | Educação em Investimentos", page_icon="💬", layout="centered")
st.title("💬 Chatbot Financeiro")
st.caption("Educação financeira sobre renda fixa e renda variável no mercado brasileiro.")

def get_key() -> str:
    # Os secrets só são acessados quando configurados; não os mostre na interface.
    try:
        value = st.secrets.get("OPENAI_API_KEY", "")
    except (FileNotFoundError, KeyError):
        value = ""
    return value or os.getenv("OPENAI_API_KEY", "")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = fresh_history()

with st.sidebar:
    st.header("Configurações")
    topic = st.selectbox("Tema da conversa", TOPICS)
    if st.button("Limpar conversa deste tema"):
        st.session_state["chat_history"][topic] = []
        st.rerun()
    st.divider()
    st.caption("Projeto educacional. Não é assessoria financeira nem recomendação individual.")
    st.caption("As respostas da IA podem conter erros ou estar desatualizadas.")

history = st.session_state["chat_history"][topic]
if not history:
    st.info(WELCOME)

for item in history:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

prompt = st.chat_input(f"Pergunte sobre {topic.lower()}…", max_chars=MAX_INPUT_CHARS)
if prompt is not None:
    try:
        prompt = validate_prompt(prompt)
    except ValueError as exc:
        st.warning(str(exc))
        st.stop()

    key = get_key()
    if not key:
        st.error("Serviço de IA indisponível: configure OPENAI_API_KEY no ambiente do servidor.")
        st.stop()

    # O histórico pertence somente à sessão atual do navegador, não a um global compartilhado.
    history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Preparando uma resposta…"):
                answer = responder(topic, history, key)
            st.markdown(answer)
        history.append({"role": "assistant", "content": answer})
        # Limite memória mantida por tema na sessão; não gravamos logs das perguntas.
        del history[:-MAX_INPUT_CHARS // 60] if False else history[:0]
        if len(history) > 20:
            del history[:-20]
    except Exception:
        history.pop()  # Evita mensagem do usuário órfã após uma falha da API.
        st.error("Não foi possível consultar a IA agora. Verifique a configuração e tente novamente.")
