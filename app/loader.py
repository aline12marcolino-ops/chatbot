from pathlib import Path
from langchain_core.documents import Document


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "documentos"


def carregar_documentos():
    documentos = []

    if not DATA_PATH.exists():
        print(f"Pasta não encontrada: {DATA_PATH}")
        return documentos

    arquivos = []

    # Arquivos Markdown
    arquivos.extend(DATA_PATH.glob("*.md"))

    # Arquivos TXT
    arquivos.extend(DATA_PATH.glob("*.txt"))

    print(f"Pasta de documentos: {DATA_PATH}")
    print(f"Arquivos encontrados: {len(arquivos)}")

    for arquivo in arquivos:

        try:
            texto = arquivo.read_text(encoding="utf-8")

            if texto.strip():

                documento = Document(
                    page_content=texto,
                    metadata={
                        "source": arquivo.name,
                        "tipo": arquivo.suffix
                    }
                )

                documentos.append(documento)

                print(f"OK: {arquivo.name}")

        except Exception as erro:
            print(f"Erro ao carregar {arquivo.name}: {erro}")

    print(f"Documentos carregados: {len(documentos)}")

    return documentos