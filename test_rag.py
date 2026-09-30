from app.loader import carregar_documentos
from app.splitter import dividir_documentos
from app.embeddings import criar_embeddings
from app.vectorstore import criar_vectorstore
from app.retriever import criar_retriever
from app.rag_chain import criar_rag_chain


documentos = carregar_documentos()

chunks = dividir_documentos(
    documentos,
    chunk_size=1000,
    chunk_overlap=100
)

embeddings = criar_embeddings()

vectorstore = criar_vectorstore(
    chunks,
    embeddings
)

retriever = criar_retriever(
    vectorstore
)

rag = criar_rag_chain(
    retriever
)


pergunta = "Como funciona o carregamento de veículos elétricos?"

resposta = rag.invoke(pergunta)

print("\n==============================")
print("RESPOSTA DA NORAH")
print("==============================")
print(resposta)