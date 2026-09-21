from pydantic import BaseModel, Field
class AnaliseConsulta(BaseModel):

    categoria: str = Field(
        description="Categoria da pergunta"
    )
    assunto: str = Field(
        description="Assunto principal da pergunta"
    )
    nivel_urgencia: str = Field(
        description="Nível de urgência"
    )
    recomendacao: str = Field(
        description="Recomendação para o usuário"
    )
    confianca: float = Field(
        description="Nível de confiança da análise"
    )