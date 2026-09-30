import os
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings

load_dotenv()


def criar_embeddings():
    api_key = os.getenv("OLLAMA_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OLLAMA_API_KEY não encontrada no arquivo .env"
        )

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="https://ollama.com",
        client_kwargs={
            "headers": {
                "Authorization": f"Bearer {api_key}"
            }
        }
    )

    return embeddings