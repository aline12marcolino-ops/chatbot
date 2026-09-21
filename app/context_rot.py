import tiktoken
from .chain import llm
from .prompts import SYSTEM_PROMPT
from langchain_core.messages import HumanMessage, SystemMessage

MODELO_TOKEN = "cl100k_base"

def contar_tokens(texto: str) -> int:
    """
    Conta a quantidade de tokens do contexto usando tiktoken.
    """

    encoding = tiktoken.get_encoding(MODELO_TOKEN)
    return len(encoding.encode(texto))

def gerar_contextos():
    """
    Cria diferentes tamanhos de contexto para o experimento.

    O experimento utiliza a mesma pergunta final, mas aumenta
    progressivamente a quantidade de informações no contexto.

    Informações relevantes são colocadas no início e no final,
    enquanto conteúdos secundários são adicionados no meio.
    Isso permite observar se o modelo mantém as informações
    importantes conforme o contexto cresce.
    """

    informacao_inicial = """
Informação importante da conversa:
O veículo elétrico do usuário está com 20% de bateria.
O usuário deseja carregar o veículo até 80%.
A prioridade é realizar o carregamento de forma segura e eficiente.
"""

    informacao_final = """
Informação importante mais recente:
O usuário está utilizando um carregador GoodWe.
A orientação deve considerar segurança, bateria e eficiência
durante o carregamento.
"""

    conteudo_irrelevante = """
Durante a conversa foram mencionados diversos assuntos secundários.

O usuário comentou sobre tecnologia, computadores, programação,
aplicativos, internet, estudos, inteligência artificial,
sustentabilidade, energia solar, sistemas digitais,
desenvolvimento de software, bancos de dados, dispositivos móveis,
redes de comunicação, programação em Python, análise de dados,
automação, sensores, sistemas embarcados e outros assuntos.

Também foram mencionadas questões gerais sobre tecnologia,
educação, ferramentas digitais, plataformas online,
desenvolvimento de projetos acadêmicos e organização de arquivos.

Essas informações não são necessárias para responder à pergunta
final sobre o carregamento do veículo elétrico.
"""

    return {
        0: "",

        5: (
            informacao_inicial
            + "\n"
            + conteudo_irrelevante * 2
            + informacao_final
        ),

        10: (
            informacao_inicial
            + "\n"
            + conteudo_irrelevante * 5
            + informacao_final
        ),

        15: (
            informacao_inicial
            + "\n"
            + conteudo_irrelevante * 8
            + informacao_final
        ),

        20: (
            informacao_inicial
            + "\n"
            + conteudo_irrelevante * 12
            + informacao_final
        ),

        30: (
            informacao_inicial
            + "\n"
            + conteudo_irrelevante * 20
            + informacao_final
        ),
    }

def gerar_resposta(contexto: str):
    """
    Envia a mesma pergunta ao modelo, alterando apenas
    o tamanho do contexto.
    """

    mensagem = f"""
Contexto da conversa:

{contexto}

Agora responda EXATAMENTE à seguinte pergunta:

O veículo está com 20% de bateria e o usuário quer carregá-lo
até 80% usando um carregador GoodWe.

Como realizar esse carregamento de forma eficiente e segura?

A resposta deve:
- considerar as informações disponíveis no contexto;
- explicar o procedimento de forma clara;
- mencionar a segurança durante o carregamento;
- evitar inventar informações;
- responder em português do Brasil.
"""

    mensagens = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=mensagem)
    ]

    resposta = llm.invoke(mensagens)

    return resposta.content

def avaliar_resposta(resposta: str) -> int:
    """
    Avalia de forma simples a qualidade da resposta.

    Pontuação máxima: 5 pontos.

    Critérios:
    1. menciona a bateria inicial de 20%;
    2. menciona o objetivo de 80%;
    3. menciona o carregador GoodWe;
    4. aborda segurança;
    5. apresenta orientação coerente sobre carregamento.
    """

    texto = resposta.lower()

    pontos = 0

    criterios = [
        ["20%", "20 %"],
        ["80%", "80 %"],
        ["goodwe"],
        ["segurança", "seguro"],
        ["carregamento", "carregar", "carga"],
    ]

    for palavras in criterios:

        if any(palavra in texto for palavra in palavras):
            pontos += 1

    return pontos

def analisar_contexto(contextos):
    """
    Executa o experimento de Context Rot.

    Para cada tamanho de contexto:
    - conta os tokens;
    - gera uma resposta;
    - calcula uma pontuação de qualidade.
    """

    resultados = []

    for turnos, contexto in contextos.items():

        tokens = contar_tokens(contexto)

        print(
            f"Analisando contexto com {turnos} turnos "
            f"({tokens} tokens)..."
        )

        resposta = gerar_resposta(contexto)

        qualidade = avaliar_resposta(resposta)

        resultados.append({
            "turnos": turnos,
            "tokens": tokens,
            "qualidade": qualidade,
            "resposta": resposta
        })

    return resultados

def exibir_resultados(resultados):
    """
    Exibe os resultados do experimento no terminal.
    """

    print()
    print("=" * 70)
    print("              EXPERIMENTO - CONTEXT ROT")
    print("=" * 70)

    print(
        f"{'Turnos':<10}"
        f"{'Tokens':<12}"
        f"{'Qualidade':<12}"
    )

    print("-" * 34)

    for resultado in resultados:

        print(
            f"{resultado['turnos']:<10}"
            f"{resultado['tokens']:<12}"
            f"{resultado['qualidade']}/5"
        )

    print("-" * 34)

    print()
    print("RESUMO DAS RESPOSTAS")
    print("=" * 70)

    for resultado in resultados:

        print()
        print(f"--- {resultado['turnos']} turnos ---")
        print(f"Tokens: {resultado['tokens']}")
        print(f"Qualidade: {resultado['qualidade']}/5")
        print("Resposta:")
        print(resultado["resposta"])

    print()
    print("=" * 70)


def executar_experimento():
    """
    Executa o experimento completo de Context Rot.
    """

    contextos = gerar_contextos()

    resultados = analisar_contexto(contextos)

    exibir_resultados(resultados)

    return resultados


if __name__ == "__main__":
    executar_experimento()
