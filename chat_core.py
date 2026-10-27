"""Regras de conversa e armazenamento em memória local à sessão Streamlit.

Não armazena mensagens em disco. Não compartilha histórico entre visitantes.
"""
from __future__ import annotations

MAX_INPUT_CHARS = 1200
MAX_HISTORY_MESSAGES = 16
TOPICS = ("Renda Fixa", "Renda Variável")
WELCOME = "Olá! Pergunte sobre conceitos, riscos e funcionamento de investimentos no Brasil."

SYSTEM_PROMPT = """Você é um assistente EDUCACIONAL sobre o mercado financeiro brasileiro.
Responda em português claro e didático, priorizando o tema: {topic}.
Explique conceitos de renda fixa e renda variável, riscos, tributação e funcionamento geral.
Não apresente estimativas como fatos, não invente cotações, taxas, legislação ou notícias atuais.
Você NÃO tem acesso a dados de mercado em tempo real ou a informações pessoais do usuário.
Se depender de dados atuais, explique que é necessário consultar fontes oficiais atualizadas.
Não recomende ativos específicos como adequados ao perfil pessoal e não prometa rentabilidade.
Não peça senhas, CPF, dados bancários ou outras informações sensíveis.
Se a pergunta não tratar de educação financeira, redirecione de forma breve e cordial.
Responda de forma objetiva, normalmente em até três parágrafos.
"""

def validate_prompt(prompt: str) -> str:
    if not isinstance(prompt, str):
        raise ValueError("A pergunta deve ser um texto.")
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("Digite uma pergunta.")
    if len(prompt) > MAX_INPUT_CHARS:
        raise ValueError(f"Limite de {MAX_INPUT_CHARS} caracteres por pergunta.")
    return prompt

def fresh_history() -> dict[str, list[dict[str, str]]]:
    return {topic: [] for topic in TOPICS}

def api_messages(topic: str, history: list[dict[str, str]]) -> list[dict[str, str]]:
    if topic not in TOPICS:
        raise ValueError("Tema não reconhecido.")
    valid = [
        {"role": item["role"], "content": item["content"]}
        for item in history[-MAX_HISTORY_MESSAGES:]
        if item.get("role") in ("user", "assistant") and isinstance(item.get("content"), str)
    ]
    return [{"role": "system", "content": SYSTEM_PROMPT.format(topic=topic)}, *valid]
