import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from modelo_openai import chain_memoria, conversas

def abrir_chat(prompt, chain_memoria, conversas):
    area = st.selectbox("Selecione um tema", options=["Renda Fixa", "Renda Variável"])
    config = {"configurable": {"session_id":area}}
    
    if prompt:
        chain_memoria.invoke({"mensagem":prompt}, config=config)
    
    if area in conversas:
        for mensagem in conversas[area].messages:
            if mensagem.type != "system":
                with st.chat_message(mensagem.type):
                    st.write(mensagem.content)

def meu_app():
    st.header("Bot Assessor de Investimentos", divider=True)
    st.markdown("#### Converse com nosso especialista em investimentos")
    prompt = st.chat_input("Digite aqui seu prompt") 
    ##st.caption("#### Quer falar com especialista humano??? Chama no Zap: ....")       
    abrir_chat(prompt, chain_memoria, conversas)  

if __name__ == "__main__":
    meu_app()