from langchain_chroma import Chroma


CHROMA_PATH = "chroma_db"


def criar_vectorstore(chunks, embeddings):

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    return vectorstore