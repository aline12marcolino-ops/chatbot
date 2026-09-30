from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from .chain import llm


RAG_PROMPT = """
Você é Norah, assistente da GoodWe.

Responda à pergunta utilizando somente as informações
presentes no contexto fornecido.

Se a resposta não estiver no contexto, diga claramente
que não encontrou essa informação na base de conhecimento.

Não invente informações.

Contexto:
{context}

Pergunta:
{question}

Resposta:
"""


prompt = ChatPromptTemplate.from_template(RAG_PROMPT)


def formatar_documentos(documentos):

    return "\n\n".join(
        documento.page_content
        for documento in documentos
    )


def criar_rag_chain(retriever):

    rag_chain = (
        {
            "context": retriever | formatar_documentos,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain