import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from .prompts import SYSTEM_PROMPT
from .schemas import AnaliseConsulta
load_dotenv()

parser = PydanticOutputParser(
    pydantic_object=AnaliseConsulta
)

api_key = os.getenv("OLLAMA_API_KEY")

if not api_key:
    raise RuntimeError(
        "OLLAMA_API_KEY não foi encontrada no arquivo .env"
    )

llm = ChatOllama(
    model="gemma4:cloud",
    base_url="https://ollama.com",
    client_kwargs={
        "headers": {
            "Authorization": f"Bearer {api_key}"
        }
    }
)

structured_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    (
        "human",
        "{input}\n\n"
        "Analise a pergunta e produza a resposta seguindo exatamente "
        "o formato solicitado abaixo.\n\n"
        "{format_instructions}"
    )
]).partial(
    format_instructions=parser.get_format_instructions()
)

chain = structured_prompt | llm | parser