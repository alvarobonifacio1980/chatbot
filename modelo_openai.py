from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts.chat import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

conversas = {}
def pegar_sessao(session_id):
    if session_id not in conversas:
        conversas[session_id] = InMemoryChatMessageHistory()
    return conversas[session_id]    


template_chat = ChatPromptTemplate(
    [
        ("system", "Responda as perguntas de forma curta, com até 140 caracteres, somente sobre o mercado financeiro brasileiro. "
                   "Para qualquer questão fora deste contexto, responda: Desculpe, estou focado em fornecer informações sobre o mercado financeiro brasileiro. Posso te ajudar com mais alguma dúvida nesse tema? "
                   "No caso de saudações, responda cordialmente, limitada a apensas uma resposta, depois retone a mensagem Desculpe..."                   
                   ),
        ("placeholder", "{history}"),
        ("user", "{mensagem}")
    ], partial_variables={"tema": "Mercado Financeiro Brasileiro"}
)

modelo = ChatOpenAI()

chain = template_chat | modelo
chain_memoria = RunnableWithMessageHistory(chain,
                                           get_session_history=pegar_sessao,
                                           input_messages_key="mensagem",
                                           history_messages_key="history")