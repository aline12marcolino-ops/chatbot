from langchain_text_splitters import RecursiveCharacterTextSplitter


def dividir_documentos(documentos, chunk_size, chunk_overlap):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_documents(documentos)

    print(f"Chunks gerados: {len(chunks)}")

    return chunks