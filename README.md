# CKP01 — Chatbot Profissional · GoodWe / Norah
**Prompt Engineering & AI · FIAP · 2º Semestre 2026**

## Integrantes
* **Aline Medri Marcolino** — RM 569349
* **Luis Fernando de Azevedo** — RM 574167
--- 

# 1. Domínio
O projeto consiste na criação da **Norah**, uma assistente virtual especializada em **mobilidade elétrica e carregadores de veículos elétricos da GoodWe**.
O domínio foi escolhido por estar relacionado ao desafio da GoodWe de desenvolver soluções inteligentes para mobilidade elétrica, carregamento de veículos elétricos e utilização de Inteligência Artificial no atendimento aos usuários.
A Norah foi desenvolvida para responder dúvidas, manter o contexto das conversas e auxiliar o usuário em situações relacionadas ao uso de carregadores e estações de recarga.

---

# 2. Usuários-alvo
A Norah foi desenvolvida principalmente para:

* Usuários de veículos elétricos;
* Pessoas que utilizam estações de carregamento;
* Clientes que possuem dúvidas sobre carregadores GoodWe;
* Usuários que precisam acompanhar ou interromper uma recarga;
* Usuários que possuem dúvidas sobre pagamento e utilização do carregador.

A assistente também consegue lidar com conversas gerais, como saudações e perguntas introdutórias, mantendo uma comunicação profissional e coerente com sua persona.
---

# 3. Objetivo do projeto
O objetivo do CKP01 é desenvolver um chatbot profissional utilizando as técnicas de **LangChain, LCEL, ChatOllama, memória gerenciada, engenharia de contexto e Pydantic v2**.

A Norah utiliza uma arquitetura composta por duas partes principais:
1. **ConversationChain com memória**, responsável pela conversa com o usuário e pela manutenção do histórico;
2. **Pipeline LCEL**, utilizando `ChatPromptTemplate | ChatOllama | PydanticOutputParser`, responsável pela geração e validação de uma saída estruturada.

---

# 4. Arquitetura
O projeto utiliza duas chains, conforme a arquitetura proposta no CKP01.

## 4.1 Chain de conversa

A primeira chain é responsável pela interação com o usuário e pelo gerenciamento da memória da conversa.

```text
Usuário
   │
   ▼
ConversationChain
   │
   ▼
Memória gerenciada
   │
   ▼
ChatOllama
   │
   ▼
Resposta da Norah
```
A memória permite que a Norah utilize informações apresentadas anteriormente pelo usuário durante a mesma sessão.

---

## 4.2 Pipeline LCEL para saída estruturada
A segunda chain utiliza o operador `|` do LangChain Expression Language (LCEL).

```text
ChatPromptTemplate
        │
        ▼
    ChatOllama
        │
        ▼
PydanticOutputParser
        │
        ▼
Saída estruturada validada
```

O pipeline utiliza:

```text
ChatPromptTemplate | ChatOllama | PydanticOutputParser
```

O `ChatPromptTemplate` recebe variáveis e separa as mensagens de sistema e usuário.

O `ChatOllama` utiliza o modelo disponibilizado pelo Ollama Cloud.

O `PydanticOutputParser` transforma a resposta do modelo em uma estrutura validada pelo modelo Pydantic.

---

# 5. Estrutura do projeto
```text
CKP01-GoodWe/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── chain.py
│   ├── memory_manager.py
│   ├── schemas.py
│   ├── context_rot.py
│   └── prompts.py
│
├── .env.example
├── requirements.txt
└── README.md
```

### `app/main.py`

Responsável pelo ponto de entrada da aplicação e pela interface de interação com o chatbot.

### `app/chain.py`

Responsável pela construção das chains do projeto e pelo pipeline LCEL.

### `app/memory_manager.py`

Responsável pela configuração e gerenciamento da memória da conversa.

### `app/schemas.py`

Contém os modelos `BaseModel` do **Pydantic v2** utilizados para validar as saídas estruturadas.

### `app/context_rot.py`

Responsável pela demonstração do **context rot**, comparando a qualidade das respostas em diferentes tamanhos de contexto.

### `app/prompts.py`

Contém o system prompt da Norah e as instruções utilizadas pelo chatbot.

---

# 6. Requisitos atendidos
| Requisito            | Status | Implementação                                       |
| -------------------- | ------ | --------------------------------------------------- |
| Pipeline LCEL        | ✅      | `chain.py` utilizando o operador `\|`               |
| ChatOllama           | ✅      | Ollama Cloud utilizando `gemma4:cloud`              |
| ChatPromptTemplate   | ✅      | Templates com variáveis e mensagens separadas       |
| Memória gerenciada   | ✅      | `ConversationChain` + estratégia de memória         |
| Memória em 5+ turnos | ✅      | Teste de continuidade da conversa                   |
| Pydantic v2          | ✅      | `BaseModel` com campos tipados                      |
| PydanticOutputParser | ✅      | Validação da saída estruturada                      |
| Context rot          | ✅      | `context_rot.py` com diferentes janelas de contexto |
| System prompt        | ✅      | Persona, regras e restrições da Norah               |
| XML tagging          | ✅      | Organização das instruções do system prompt         |
| Domínio documentado  | ✅      | GoodWe / mobilidade elétrica                        |
| Projeto local        | ✅      | Pacote Python organizado em `app/`                  |
| `.env`               | ✅      | Chave carregada por variável de ambiente            |
| `.env.example`       | ✅      | Modelo da variável necessária                       |

---

# 7. Tecnologias utilizadas
* **Python**
* **LangChain**
* **LangChain Expression Language (LCEL)**
* **ChatOllama**
* **Ollama Cloud**
* **Pydantic v2**
* **python-dotenv**

---

# 8. Modelo de IA
O projeto utiliza exclusivamente o modelo:

```text
modelo:gemma4:cloud
```
---

# 9. Como executar
Crie esses arquivos 
```env          |    .env.example
OLLAMA_API_KEY= |OLLAMA_API_KEY= "sua chave"
```

No terminal:

```bash
python -m pip install -r requirements.txt --> instalar biblioteca
python -m app.main --> executar o projeto
```
---

# 10. Chain de conversa
A Norah utiliza uma `ConversationChain` para gerenciar a interação com o usuário.

A chain mantém o histórico da sessão para que informações apresentadas anteriormente possam ser utilizadas em respostas posteriores.

O fluxo é:

```text
Pergunta do usuário
        ↓
ConversationChain
        ↓
Memória
        ↓
System Prompt
        ↓
ChatOllama
        ↓
Resposta da Norah
```

Essa abordagem permite que a conversa seja mais natural e que a assistente mantenha informações relevantes apresentadas anteriormente.

---

# 11. Memória gerenciada

## Estratégia escolhida

A estratégia de memória utilizada no projeto é:

```text
[PREENCHER: Buffer / Summary / TokenBuffer]
```

### Justificativa

A estratégia foi escolhida considerando o domínio da Norah e a necessidade de manter informações relevantes durante uma conversa sobre carregamento de veículos elétricos.
A memória permite que perguntas posteriores sejam interpretadas considerando informações apresentadas anteriormente pelo usuário.
Isso é importante, por exemplo, quando o usuário fornece uma informação em um turno e faz referência a ela posteriormente sem repeti-la.

### Limite de contexto

A memória foi configurada considerando a faixa de aproximadamente **800 a 1500 tokens**, conforme o requisito do CKP01.

A escolha busca equilibrar:

* continuidade da conversa;
* quantidade de informações mantidas;
* custo de tokens;
* qualidade das respostas.

---

# 12. Demonstração da memória
A memória foi testada durante pelo menos cinco turnos de conversa.

Exemplo de sequência de teste:

```text
Turno 1
Usuário: Olá, meu carro é elétrico.

Turno 2
Usuário:Como faço para carregar meu carro elétrico usando um carregador GoodWe?

Turno 3
Usuário: Quero carregar ele até 80%.

Turno 4
Usuário: Meu carro está com 20% de bateria e preciso carregar para viajar amanhã. O que devo fazer?

Turno 5
Usuário: E depois posso interromper a recarga?
```
O objetivo do teste é verificar se a Norah consegue utilizar informações apresentadas nos turnos anteriores sem que o usuário precise repetir todo o contexto.

---

# 13. Pydantic v2
O projeto utiliza **Pydantic v2** para definir estruturas tipadas e validar a saída gerada pelo modelo.
O schema possui pelo menos quatro campos tipados e é utilizado em conjunto com o:

```text
PydanticOutputParser
```

A validação evita que a aplicação dependa apenas de uma resposta textual livre do modelo.

## Estrutura utilizada
O schema implementado no projeto está localizado em:

```text
app/schemas.py
```

### Exemplo conceitual
```python
class AnaliseConsulta(BaseModel):
    categoria: str
    intencao: str
    prioridade: str
    resposta: str
```

 Os campos acima devem corresponder exatamente ao schema existente no código final do projeto.
A saída passa pelo `PydanticOutputParser`, garantindo que o resultado siga a estrutura definida pelo modelo Pydantic.

---

# 14. System Prompt
A Norah possui um system prompt responsável por definir sua persona, comportamento e restrições.
A estrutura do prompt utiliza seções organizadas por **XML tagging**, conforme apresentado no Módulo 1.

Exemplo de organização:

```xml
<persona>
Você é Norah, assistente virtual especializada em mobilidade elétrica
e soluções de carregamento da GoodWe.
</persona>

<dominio>
Você atua no contexto de veículos elétricos, carregadores,
estações de recarga e utilização de soluções GoodWe.
</dominio>

<comportamento>
Seja profissional, clara, empática e didática.
</comportamento>

<restricoes>
Não invente informações técnicas.
Quando não possuir informações suficientes,
deixe isso claro ao usuário.
</restricoes>

<resposta>
Responda de maneira objetiva e adequada ao contexto da pergunta.
</resposta>
```

O prompt completo utilizado pela aplicação está em:

```text
app/prompts.py
```

---

# 15. Context Engineering
O projeto aplica técnicas de **context engineering** para controlar as informações fornecidas ao modelo.
O objetivo é evitar que o crescimento excessivo do contexto prejudique a qualidade das respostas.
O mesmo prompt é utilizado durante os testes, alterando-se a quantidade de contexto disponível para o modelo.

---

# 16. Context Rot
O projeto possui o arquivo:

```text
app/context_rot.py
```

responsável por demonstrar o comportamento do modelo com diferentes tamanhos de contexto.

O teste compara diferentes janelas de contexto, por exemplo:

```text
0 turnos
5 turnos
10 turnos
15 turnos
20 turnos
```

A qualidade das respostas é então comparada para observar possíveis sinais de degradação conforme o contexto aumenta.

## Resultado
|  Contexto | Qualidade observada | Observação                              |
| --------: | ------------------- | ----------------------------------------|
|  0 turnos |       5/5           | Resposta coerente e alinhada ao domínio |
|  5 turnos |       5/5           |         Qualidade mantida               |
| 10 turnos |       5/5           |         Qualidade mantida               |
| 15 turnos |       5/5           |         Qualidade mantida               |
| 20 turnos |       5/5           |         Qualidade mantida               |

### Conclusão do teste
O teste de contexto crescente mostrou que o chatbot manteve uma qualidade de resposta de 5/5 nos cenários avaliados, mesmo com o aumento do contexto de 0 para 20 turnos

---

# 17. Métricas de contexto
Como diferencial de Context Engineering, o projeto pode utilizar `tiktoken` para contabilizar a quantidade de tokens utilizada em cada janela de contexto.

### Comparação

|    Janela |      Tokens | Qualidade   |
| --------: | ----------: | ----------- |
|  0 turnos |       0     |     5/5     |
|  5 turnos |      449    |     5/5     |
| 10 turnos |      977    |     5/5     |
| 15 turnos |      1505   |     5/5     |
| 20 turnos |      2209   |     5/5     |

---

# 18. Testes realizados
Foram realizados testes para verificar:

### Teste 1 — Saudação
O resultado foi categoria Saudação, assunto Interação inicial, urgência Baixa e confiança 1.0. E Norah respondeu sobre ela e o que ela pode ajudar.

### Teste 2 — Domínio
A pergunta foi como usar o carregador da Goodwe. A Norah respondeu com um passo a passo sobre o carregamento e mandou verificar os LEDs de status. A categoria foi operação de equipamento, assunto procedimento de carregamento de veículo elétrico, nível de urgência baixa e confiança 1.0.

### Teste 3 — Memória
A pergunta foi que a pessoa quer carregar o carro até 80%. E a recomendação foi que o limite (até 80%) é configurado diretamente no painel do veículo elétrico ou no aplicativo do fabricante do carro, e não no carregador GoodWe. Recomendo ajustar essa configuração nas definições de bateria do seu veículo para preservar a vida útil da célula. A categoria foi operação de carregamento, o assunto foi limite de carga da bateria, nível de urgência foi baixo e confiança 1.0.

### Teste 4 — Saída estruturada
A pergunta foi sobre um carro com 20% de bateria que precisa viajar no dia seguinte. A Norah respondeu Conecte seu veículo imediatamente a um carregador GoodWe ou a outra estação de recarga compatível. Como você tem tempo até amanhã, a recarga lenta (AC) é suficiente para atingir a carga total, mas recomendo iniciar o processo agora para garantir a autonomia necessária para a viagem. A cetgoria foi carregamento de veículo elétrico, assunto planejamento de carga para viagem, nível de urgência alta e cofiança 1.0.


### Teste 5 — Contexto crescente
Foi feito um teste aumentando a quantidade de turnos do contexto. Foram analisados 0, 5, 10, 15 e 20 turnos.

---

# 19. Organização profissional
O projeto foi organizado como um pacote Python local, separando as responsabilidades em diferentes módulos.

Essa estrutura facilita:

* manutenção do código;
* evolução do chatbot;
* testes;
* alteração do prompt;
* gerenciamento da memória;
* validação das respostas;
* implementação futura de RAG;
* implementação futura de agentes.

A modularização também permite que o chatbot desenvolvido neste CKP01 seja utilizado como base para os próximos checkpoints.

---

# 2. Evolução do projeto
O CKP01 representa a primeira etapa do projeto.
A arquitetura foi organizada pensando na continuidade do desenvolvimento durante o semestre:

```text
CKP01
Chatbot + Memória
       ↓
CKP02
RAG
       ↓
CKP03
Agente
       ↓
LangGraph
```

Dessa forma, o domínio da GoodWe e a Norah permanecem como base para a evolução do projeto.

---

# 21. Conclusão
O CKP01 apresenta a implementação de um chatbot profissional especializado no domínio de mobilidade elétrica e carregadores GoodWe.

A solução utiliza **LangChain LCEL, ChatOllama, ChatPromptTemplate, ConversationChain, memória gerenciada e Pydantic v2**, além de técnicas de context engineering.

A estrutura modular permite que o projeto seja executado localmente e evolua nos próximos checkpoints do semestre.

A Norah foi desenvolvida com foco em manter uma persona consistente, preservar o contexto das conversas e produzir respostas estruturadas e validadas.

---
