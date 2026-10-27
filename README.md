# Chatbot Financeiro — Educação em Investimentos

Protótipo de **assistente virtual educacional**, desenvolvido com Python, Streamlit e API OpenAI para esclarecer conceitos de investimentos no mercado brasileiro.

**Estado:** projeto funcional em código, sem implantação pública confirmada. Requer chave de API válida no servidor.

## Objetivo

Demonstrar integração de IA generativa em uma aplicação conversacional, com interface web, engenharia de prompts, delimitação temática e histórico de diálogo separado por sessão e por tema.

### O que o projeto faz

- Responde perguntas educativas sobre **renda fixa** e **renda variável**.
- Mantém contexto recente da conversa para cada tema **na sessão atual**.
- Permite limpar o histórico do tema, sem afetar outro tema.
- Restringe o uso a um domínio financeiro educacional por instruções de sistema.
- Não consulta cotações em tempo real nem oferece recomendações personalizadas.

## Diferença em relação ao BazinBot

| Chatbot Financeiro | [BazinBot](https://github.com/alvarobonifacio1980/BazinBot) |
|---|---|
| Conversação com IA generativa | Avaliação numérica de ações pelo Método de Bazin |
| Explicações conceituais | Coleta de dividendos e preços |
| Temas de renda fixa e variável | Estudo específico de valuation |
| Exige uma chave de API OpenAI | Depende de dados de mercado |

Os dois projetos são complementares, **não compartilham código nem processamento de dados**.

## Executar localmente

Requer Python 3.11+.

```bash
python -m pip install -r requirements.txt
export OPENAI_API_KEY="sua_chave"
streamlit run chat.py
```

No Windows PowerShell: `$env:OPENAI_API_KEY="sua_chave"`.

A chave também pode ser configurada nos *secrets* do Streamlit ou nas variáveis de ambiente da hospedagem. **Nunca inclua chaves no Git**. O arquivo `.env.example` é apenas ilustrativo; variáveis de um arquivo `.env` não são carregadas automaticamente.

## Executar testes

```bash
python -m unittest discover -s tests -v
```

GitHub Actions executa verificação de sintaxe e testes offline em cada alteração. Esses testes não consomem créditos da API e **não equivalem a uma execução integrada com o serviço OpenAI**.

## Arquitetura

```text
chat.py               # Interface Streamlit e estado por sessão
chat_core.py          # Regras de entrada, histórico e prompt de sistema
modelo_openai.py      # Chamada isolada ao modelo
tests/                # Testes de lógica sem credenciais
.github/workflows/    # Verificação automática
requirements.txt      # Bibliotecas da aplicação
.env.example          # Modelo de configuração, sem segredos
```

## Privacidade e limites

As mensagens permanecem na memória da sessão Streamlit no servidor durante o uso e são enviadas à API OpenAI para gerar respostas. **Não há persistência em banco de dados nem exportação das conversas implementada no código**, mas a plataforma de hospedagem e a API podem processar informações conforme suas políticas. Não envie CPF, senhas, contas ou dados financeiros sensíveis.

O prompt delimita o tema, mas **não garante bloqueio absoluto** de perguntas fora do escopo. As respostas podem conter erros e não substituem orientação de profissionais habilitados.

Este projeto demonstra uma aplicação de IA conversacional; **não presta consultoria, análise certificada ou assessoria de investimentos**.

---

**Autor:** Álvaro Bonifácio.
