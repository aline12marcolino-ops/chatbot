import gradio as gr
from dotenv import load_dotenv
from langchain_classic.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .chain import llm, chain
from .memory_manager import criar_memoria
from .prompts import SYSTEM_PROMPT

memoria = criar_memoria()

conversation_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

conversation_chain = ConversationChain(
    llm=llm,
    memory=memoria,
    prompt=conversation_prompt,
    verbose=False
)

def gerar_chat(historico):

    if not historico:
        return """
        <div class="chat-area">

            <div class="message assistant-message">

                <div class="avatar-gw">
                    GW
                </div>

                <div class="message-content">

                    <div class="message-name">
                        GoodWe
                        <span>agora</span>
                    </div>

                    <div class="bubble assistant-bubble">
                        Olá! 👋 Sou a Norah, assistente inteligente da GoodWe.
                        <br><br>
                        Como posso ajudar você hoje?
                    </div>

                </div>

            </div>

        </div>
        """

    html = '<div class="chat-area">'

    for mensagem in historico:

        role = mensagem.get("role", "")
        content = str(mensagem.get("content", ""))

        # Proteção básica para HTML
        content = (
            content
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )

        if role == "user":

            html += f"""
            <div class="message user-message">

                <div class="user-bubble">
                    {content}
                </div>

                <div class="avatar-user">

                    <svg
                        viewBox="0 0 24 24"
                        width="20"
                        height="20"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >

                        <circle
                            cx="12"
                            cy="8"
                            r="3.5"
                            fill="white"
                        />

                        <path
                            d="M5 20C5.5 15.8 8 13.5 12 13.5C16 13.5 18.5 15.8 19 20"
                            stroke="white"
                            stroke-width="2"
                            stroke-linecap="round"
                        />

                    </svg>

                </div>

            </div>
            """

        elif role == "assistant":

            html += f"""
            <div class="message assistant-message">

                <div class="avatar-gw">
                    GW
                </div>

                <div class="message-content">

                    <div class="message-name">
                        GoodWe
                        <span>agora</span>
                    </div>

                    <div class="bubble assistant-bubble">
                        {content}
                    </div>

                </div>

            </div>
            """

    html += "</div>"

    return html

def responder(mensagem, historico):

    historico = list(historico or [])

    if not mensagem or not str(mensagem).strip():

        return (
            "",
            gerar_chat(historico),
            historico
        )

    mensagem = str(mensagem).strip()

    try:
        resposta = conversation_chain.predict(
            input=mensagem
        )

        resposta = str(resposta).strip()

        try:

            analise = chain.invoke({
                "input": mensagem
            })

            # ------------------------------------------------
            # EXIBE A ANÁLISE PYDANTIC NO TERMINAL
            # ------------------------------------------------

            if analise is not None:

                print("\n========================================")
                print("           ANÁLISE PYDANTIC")
                print("========================================")

                print("\nCategoria:")
                print(analise.categoria)

                print("\nAssunto:")
                print(analise.assunto)

                print("\nNível de urgência:")
                print(analise.nivel_urgencia)

                print("\nRecomendação:")
                print(analise.recomendacao)

                print("\nConfiança:")
                print(analise.confianca)

                print("\n========================================\n")

        except Exception as erro_parser:

            print("\n========================================")
            print("ERRO NA VALIDAÇÃO PYDANTIC")
            print("========================================")
            print(erro_parser)
            print("========================================\n")

        historico.append({
            "role": "user",
            "content": mensagem
        })

        historico.append({
            "role": "assistant",
            "content": resposta
        })

        return (
            "",
            gerar_chat(historico),
            historico
        )

    except Exception as erro:

        print("\n========================================")
        print("ERRO AO CONSULTAR A IA")
        print("========================================")
        print(erro)
        print("========================================\n")

        resposta_erro = (
            "Desculpe, ocorreu um erro ao processar sua pergunta. "
            "Verifique a conexão com a IA e tente novamente."
        )

        historico.append({
            "role": "user",
            "content": mensagem
        })

        historico.append({
            "role": "assistant",
            "content": resposta_erro
        })

        return (
            "",
            gerar_chat(historico),
            historico
        )


def pergunta_filme(historico):

    return responder(
        "Posso carregar meu carro enquanto assisto a um filme?",
        historico
    )


def pergunta_bateria(historico):

    return responder(
        "Isso prejudica minha bateria?",
        historico
    )


def pergunta_suporte(historico):

    return responder(
        "Meu carregador suporta isso?",
        historico
    )


def pergunta_energia(historico):

    return responder(
        "Eu recebo por ceder energia?",
        historico
    )


def pergunta_urgencia(historico):

    return responder(
        "Preciso sair com urgência. O que posso fazer?",
        historico
    )

css = """

* {
    box-sizing: border-box !important;
}

html,
body {
    margin: 0 !important;
    padding: 0 !important;

    width: 100% !important;
    height: 100% !important;

    overflow: hidden !important;

    font-family:
        Arial,
        Helvetica,
        sans-serif !important;

    background: #edf5f2 !important;
}

.gradio-container {
    width: 100vw !important;
    height: 100vh !important;

    max-width: none !important;
    min-height: 100vh !important;

    margin: 0 !important;
    padding: 0 !important;

    background: #edf5f2 !important;
}

.gradio-container > div,
.gradio-container .contain,
.gradio-container .main {
    width: 100% !important;
    max-width: none !important;

    margin: 0 !important;
    padding: 0 !important;
}


/* =========================================================
   APLICAÇÃO
   ========================================================= */

#app {
    width: 100% !important;
    height: 100vh !important;

    padding: 14px !important;

    display: flex !important;
    flex-direction: row !important;

    gap: 12px !important;

    background: #edf5f2 !important;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

#sidebar {
    width: 200px !important;
    min-width: 200px !important;
    max-width: 200px !important;

    height: 100% !important;

    display: flex !important;
    flex-direction: column !important;

    gap: 14px !important;
}

.profile-card {
    width: 100% !important;
    min-height: 160px !important;
    padding: 16px 10px !important;
    text-align: center !important;
    background: #ffffff !important;
    border: 1px solid #dfe6e3 !important;
    border-radius: 8px !important;

    box-shadow:
        0 3px 10px rgba(0, 0, 0, 0.035) !important;
}


.profile-avatar {
    width: 43px !important;
    height: 43px !important;
    margin: 0 auto 9px auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 11px !important;
    background: #df101b !important;
    color: white !important;
    font-size: 11px !important;
    font-weight: 800 !important;
}

.profile-title {
    margin-bottom: 6px !important;
    color: #202525 !important;
    font-size: 14px !important;
    font-weight: 700 !important;
}

.profile-subtitle {
    padding: 0 5px !important;
    color: #7c8581 !important;
    font-size: 10px !important;
    line-height: 1.5 !important;
}

.online-status {
    display: inline-flex !important;
    align-items: center !important;
    gap: 4px !important;
    margin-top: 9px !important;
    padding: 4px 8px !important;
    border-radius: 15px !important;
    background: #fff0f1 !important;
    color: #d71920 !important;
    font-size: 10px !important;
    font-weight: 700 !important;
}


.online-dot {
    width: 5px !important;
    height: 5px !important;

    border-radius: 50% !important;

    background: #d71920 !important;
}

.questions-card {
    width: 100% !important;

    flex: 1 !important;

    padding: 12px 8px !important;

    background: #ffffff !important;

    border: 1px solid #dfe6e3 !important;

    border-radius: 8px !important;

    overflow-y: auto !important;

    box-shadow:
        0 3px 10px rgba(0, 0, 0, 0.035) !important;
}

.section-title {
    margin: 0 0 14px 10px !important;
    color: #858c89 !important;
    font-size: 10px !important;
    font-weight: 800 !important;
    letter-spacing: 0.4px !important;
}
.quick-question {
    width: 100% !important;
    min-height: 45px !important;
    margin: 0 0 9px 0 !important;
    padding: 7px 10px !important;
    background: #ffffff !important;
    color: #343b39 !important;
    border: 1px solid #dfe4e3 !important;
    border-radius: 6px !important;
    box-shadow: none !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}

/* Texto dentro dos botões do Gradio */
.quick-question button {
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #343b39 !important;
}

/* Garante o tamanho do texto interno */
.quick-question button span {
    font-size: 12px !important;
    font-weight: 500 !important;
}

.quick-question:hover {
    background: #ff5f5 !important;

    color: #d71920 !important;
    border-color: #d71920 !important;
}

.quick-question:hover button,
.quick-question:hover button span {
    color: #d71920 !important;
}

#main-chat {
    flex: 1 !important;

    width: auto !important;
    min-width: 0 !important;

    height: 100% !important;

    display: flex !important;
    flex-direction: column !important;

    overflow: hidden !important;

    background: #ffffff !important;

    border: 1px solid #dfe6e3 !important;

    border-radius: 16px !important;

    box-shadow:
        0 3px 10px rgba(0, 0, 0, 0.035) !important;
}


/* =========================================================
   CABEÇALHO
   ========================================================= */

#header {
    width: 100% !important;

    height: 68px !important;
    min-height: 68px !important;

    padding: 16px 24px !important;

    background: #ffffff !important;

    border-bottom: 1px solid #e6e9e8 !important;
}

.header-content {
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
}

.title {
    color: #202525 !important;
    font-size: 20px !important;
    font-weight: 700 !important;
}

.subtitle {
    margin-top: 5px !important;
    color: #8a918f !important;
    font-size: 11px !important;
}

.goodwe-badge {
    padding: 7px 11px !important;
    background: #fff0f1 !important;
    color: #d71920 !important;
    border-radius: 7px !important;
    font-size: 10px !important;
    font-weight: 800 !important;
}

#conversation {
    flex: 1 !important;
    min-height: 0 !important;
    width: 100% !important;
    overflow: hidden !important;
    background: #ffffff !important;
}

#chat-display {
    width: 100% !important;
    height: 100% !important;
    min-height: 0 !important;
    padding: 25px 28px !important;
    overflow-y: auto !important;
    background: #ffffff !important;
    border: none !important;
}

.chat-area {
    width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 25px !important;
}

.message {
    width: 100% !important;
    display: flex !important;
    align-items: flex-start !important;
}


.assistant-message {
    justify-content: flex-start !important;
    gap: 9px !important;
}


.avatar-gw {
    width: 35px !important;
    height: 35px !important;
    min-width: 35px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 50% !important;
    background: #df101b !important;
    color: #ffffff !important;
    font-size: 12px !important;
    font-weight: 800 !important;
}


.message-content {
    max-width: 75% !important;
}


.message-name {
    margin: 2px 0 7px 0 !important;
    color: #242928 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
}


.message-name span {
    margin-left: 5px !important;
    color: #a0a6a4 !important;
    font-weight: 400 !important;
    font-size: 10px !important;
}


.bubble {
    padding: 12px 15px !important;
    font-size: 13px !important;
    line-height: 1.55 !important;
}


.assistant-bubble {
    max-width: 600px !important;
    background: #f8faf9 !important;
    color: #414846 !important;
    border: 1px solid #dfe4e3 !important;
    border-radius: 0 13px 13px 13px !important;
}


.user-message {
    justify-content: flex-end !important;
    gap: 9px !important;
}


.user-bubble {
    max-width: 65% !important;
    padding: 10px 14px !important;
    background: #df101b !important;
    color: #ffffff !important;
    border-radius: 13px 13px 0 13px !important;
    font-size: 11px !important;
    line-height: 1.5 !important;
}

.avatar-user {
    width: 35px !important;
    height: 35px !important;
    min-width: 35px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 50% !important;
    background: #df101b !important;
    color: #ffffff !important;
}

#input-area {
    width: 100% !important;
    flex: 0 0 auto !important;
    padding: 13px 16px 9px 16px !important;
    background: #ffffff !important;
    border-top: 1px solid #eeeeee !important;
}
#input-row {
    width: 100% !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    gap: 8px !important;
}
#message-box {
    flex: 1 !important;
    min-width: 0 !important;
    background: #ffffff !important;
    border: none !important;
    box-shadow: none !important;
}

#message-box > *,
#message-box .wrap,
#message-box .inner-wrap,
#message-box .container,
#message-box label {
    background: #ffffff !important;
    border: none !important;
    box-shadow: none !important;
}
#message-box textarea,
#message-box input {
    width: 100% !important;
    height: 44px !important;
    min-height: 44px !important;
    max-height: 44px !important;
    padding: 13px 15px !important;
    background: #ffffff !important;
    color: #52677d !important;
    border: 1px solid #d8e0e8 !important;
    border-radius: 11px !important;
    outline: none !important;
    box-shadow: none !important;
    font-size: 9px !important;
    resize: none !important;
}

#message-box textarea::placeholder,
#message-box input::placeholder {
    color: #8295a8 !important;
    opacity: 1 !important;
}

#message-box textarea:focus,
#message-box input:focus {
    background: #ffffff !important;
    border-color: #d8e0e8 !important;
    box-shadow: none !important;
    outline: none !important;
}

#send-button {
    width: 42px !important;
    min-width: 42px !important;
    max-width: 42px !important;
    height: 42px !important;
    min-height: 42px !important;
    padding: 0 !important;
    border: none !important;
    border-radius: 10px !important;
    background: #df101b !important;
    box-shadow: none !important;
}

#send-button button {
    width: 42px !important;
    height: 42px !important;
    min-height: 42px !important;
    padding: 0 !important;
    border: none !important;
    border-radius: 10px !important;
    background: #df101b !important;
    color: white !important;
    box-shadow: none !important;
    font-size: 18px !important;
    font-weight: bold !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

#send-button button:hover {
    background: #c90d17 !important;
}

#send-button button span {
    color: white !important;
    display: block !important;
    font-size: 18px !important;
    line-height: 1 !important;
}

#disclaimer {
    width: 100% !important;
    padding-top: 5px !important;
    text-align: center !important;
    color: #a0a5a3 !important;
    font-size: 6px !important;
    line-height: 10px !important;
}

footer {
    display: none !important;
}

@media (max-width: 700px) {

    #app {
        padding: 7px !important;
        gap: 7px !important;
    }

    #sidebar {
        width: 185px !important;
        min-width: 185px !important;
        max-width: 185px !important;
    }

    #header {
        padding: 15px !important;
    }

    #chat-display {
        padding: 18px 14px !important;
    }

    .message-content {
        max-width: 82% !important;
    }
}

@media (max-width: 550px) {

    body {
        overflow: auto !important;
    }

    .gradio-container {
        height: auto !important;
        min-height: 100vh !important;
    }

    #app {
        height: auto !important;
        min-height: 100vh !important;
        flex-direction: column !important;
    }

    #sidebar {
        width: 100% !important;
        max-width: none !important;
        min-width: 0 !important;
        height: auto !important;
    }

    .profile-card {
        min-height: 135px !important;
    }

    #main-chat {
        min-height: 600px !important;
    }
}

"""
with gr.Blocks(
    title="Assistente de Energia — GoodWe",
    css=css
) as demo:

    historico_state = gr.State([])
    with gr.Row(elem_id="app"):

        with gr.Column(
            elem_id="sidebar",
            scale=0,
            min_width=200
        ):

            gr.HTML("""
            <div class="profile-card">

                <div class="profile-avatar">
                    GW
                </div>

                <div class="profile-title">
                    Assistente GoodWe
                </div>

                <div class="profile-subtitle">
                    Seu assistente inteligente para
                    carregamento de veículos elétricos.
                </div>

                <div class="online-status">
                    <span class="online-dot"></span>
                    IA online
                </div>

            </div>
            """)

            with gr.Column(
                elem_id="questions-card",
                elem_classes=["questions-card"]
            ):

                gr.HTML("""
                <div class="section-title">
                    PERGUNTAS RÁPIDAS
                </div>
                """)

                pergunta_1 = gr.Button(
                    "Carregar durante meu filme",
                    elem_classes=["quick-question"],
                    variant="secondary"
                )

                pergunta_2 = gr.Button(
                    "Isso prejudica minha bateria?",
                    elem_classes=["quick-question"],
                    variant="secondary"
                )

                pergunta_3 = gr.Button(
                    "Meu carregador suporta isso?",
                    elem_classes=["quick-question"],
                    variant="secondary"
                )

                pergunta_4 = gr.Button(
                    "Eu recebo por ceder energia?",
                    elem_classes=["quick-question"],
                    variant="secondary"
                )

                pergunta_5 = gr.Button(
                    "Preciso sair com urgência",
                    elem_classes=["quick-question"],
                    variant="secondary"
                )

        with gr.Column(
            elem_id="main-chat",
            scale=1
        ):

            gr.HTML("""
            <div id="header">

                <div class="header-content">

                    <div>

                        <div class="title">
                            Assistente de Energia
                        </div>

                        <div class="subtitle">
                            Como posso ajudar com seu carregamento?
                        </div>

                    </div>

                    <div class="goodwe-badge">
                        GOODWE AI
                    </div>

                </div>

            </div>
            """)

            with gr.Column(elem_id="conversation"):

                chat_display = gr.HTML(
                    value=gerar_chat([]),
                    elem_id="chat-display"
                )

            with gr.Column(elem_id="input-area"):

                with gr.Row(elem_id="input-row"):

                    message = gr.Textbox(
                        placeholder="Digite sua pergunta sobre o carregador...",
                        show_label=False,
                        lines=1,
                        max_lines=1,
                        scale=1,
                        container=False,
                        elem_id="message-box"
                    )

                    enviar = gr.Button(
                        "➤",
                        scale=0,
                        min_width=42,
                        elem_id="send-button"
                    )

                gr.HTML("""
                <div id="disclaimer">
                    Assistente demonstrativo. Confirme funções,
                    limites e condições comerciais nos documentos
                    oficiais do produto.
                </div>
                """)

    enviar.click(
        fn=responder,
        inputs=[
            message,
            historico_state
        ],
        outputs=[
            message,
            chat_display,
            historico_state
        ]
    )

    message.submit(
        fn=responder,
        inputs=[
            message,
            historico_state
        ],
        outputs=[
            message,
            chat_display,
            historico_state
        ]
    )

    pergunta_1.click(
        fn=pergunta_filme,
        inputs=[historico_state],
        outputs=[
            message,
            chat_display,
            historico_state
        ]
    )

    pergunta_2.click(
        fn=pergunta_bateria,
        inputs=[historico_state],
        outputs=[
            message,
            chat_display,
            historico_state
        ]
    )

    pergunta_3.click(
        fn=pergunta_suporte,
        inputs=[historico_state],
        outputs=[
            message,
            chat_display,
            historico_state
        ]
    )

    pergunta_4.click(
        fn=pergunta_energia,
        inputs=[historico_state],
        outputs=[
            message,
            chat_display,
            historico_state
        ]
    )

    pergunta_5.click(
        fn=pergunta_urgencia,
        inputs=[historico_state],
        outputs=[
            message,
            chat_display,
            historico_state
        ]
    )

if __name__ == "__main__":
    demo.launch(
        inbrowser=True,
        server_port=7860
    )