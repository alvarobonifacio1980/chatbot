from langchain_core.chat_history import InMemoryChatMessageHistory

memoria = InMemoryChatMessageHistory()

memoria.add_user_message("O q é o Python?")
memoria.add_ai_message("Não sei...")

print(memoria.messages)