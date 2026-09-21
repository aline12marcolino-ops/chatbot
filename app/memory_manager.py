from langchain_classic.memory import ConversationBufferMemory

LIMITE_TOKENS = 1200

def estimar_tokens(texto):
    """
    Estimativa simples de tokens.
    Aproximadamente 1 token para cada 4 caracteres.
    """
    if not texto:
        return 0

    return max(1, len(texto) // 4)

def calcular_tokens_historico(memoria):
    """
    Calcula aproximadamente a quantidade de tokens
    presentes no histórico da conversa.
    """

    total_caracteres = 0

    for mensagem in memoria.chat_memory.messages:
        if hasattr(mensagem, "content"):
            total_caracteres += len(str(mensagem.content))

    return estimar_tokens("x" * total_caracteres)

def limitar_memoria(memoria):
    """
    Remove os turnos mais antigos quando o histórico
    ultrapassa aproximadamente 1200 tokens.
    """

    while calcular_tokens_historico(memoria) > LIMITE_TOKENS:

        mensagens = memoria.chat_memory.messages

        if len(mensagens) <= 2:
            break

        memoria.chat_memory.messages.pop(0)
        memoria.chat_memory.messages.pop(0)

    return memoria

class MemoriaLimitada(ConversationBufferMemory):
    """
    ConversationBufferMemory com limite aproximado
    de 1200 tokens.
    """

    def save_context(self, inputs, outputs):
        # Salva o novo turno
        super().save_context(inputs, outputs)

        # Controla o tamanho do histórico
        limitar_memoria(self)

def criar_memoria():
    """
    Cria a memória conversacional da Norah.

    Estratégia escolhida:
    ConversationBufferMemory (Buffer).

    O histórico é limitado a aproximadamente 1200 tokens,
    valor que está dentro da faixa de 800 a 1500 tokens
    definida para o projeto.
    """

    memoria = MemoriaLimitada(
        memory_key="history",
        return_messages=True
    )

    return memoria