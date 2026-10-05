# Cia. Hering | AI First Transformation: Remanejamento Inteligente de Grade

> **Desafio Técnico para Desenvolvedor IA — Premiersoft / Cia. Hering**  
> Prova de Conceito (PoC) funcional de arquitetura e agente cognitivo para eliminação de fricção operacional no remanejamento de estoque entre lojas e Centro de Distribuição.

---

## Contexto e Visão AI First

No modelo tradicional de varejo (**AS-IS**), a ruptura de grade em loja física desencadeia um fluxo lento e burocrático: preenchimento de planilhas estáticas, abertura de tickets e troca de e-mails com a central de suporte, levando dias para resolução e gerando perda de sell-out.

Esta solução redesenha o processo sob a ótica **AI First (TO-BE)**:

- **Elimina:** Planilhas manuais, e-mails de triagem básica (tier 0/1) e decisões reativas tardias.
- **Mantém:** Governança fiscal, limites de crédito de franquias e supervisão humana (_Human-in-the-Loop_) para exceções e altos volumes financeiros.
- **Inova:** Monitoramento preditivo com agente autônomo conectado aos canais corporativos (Microsoft Teams/Chat), sugerindo remanejamentos otimizados por proximidade logística e permitindo aprovação em 1 clique.

---

## Arquitetura e Decisões de Engenharia

O projeto foi construído seguindo princípios estritos de pragmatismo técnico para validação rápida de hipótese (MVP em 10 dias), evitando _overengineering_:

```text
[ Lojista (Teams / Chat) ]
           │
           ▼
[ FastAPI / Webhook Engine ]
           │
           ▼
[ Agente Preditivo (LangGraph / Python Core) ]
     ├── Base de Conhecimento (Regras de Remanejamento & Distâncias)
     └── Base de Dados Operacional (Estoque em Tempo Real / SKUs)
           │
           ▼
[ Output Estruturado JSON & Notificação em 1 Clique ]
           │
           ▼
[ ERP / WMS Corporativo ]
```

### Stack Tecnológica

- **Linguagem:** Python 3.10+
- **Contratos de Dados:** Pydantic v2 (validação estrita e tipagem estruturada)
- **API & Webhooks:** FastAPI + Uvicorn
- **Interface de Demonstração:** Streamlit
- **Conteinerização:** Docker & Docker Compose

---

## Alinhamento com o MVP de 10 Dias

| Dimensão                                 | Escopo do Piloto                                                                                                                                 |
| :--------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| **O que foi construído**                 | Agente de análise de grade, motor de recomendação por proximidade geográfica, contratos Pydantic e interface de validação rápida.                |
| **O que foi deliberadamente descartado** | Barramentos complexos de eventos assíncronos (Kafka/RabbitMQ) e dashboards paralelos de BI, mantendo foco na comprovação da hipótese de negócio. |
| **Métricas de Sucesso**                  | Redução > 50% no tempo de solicitação de grade; taxa de aceitação das recomendações > 80%.                                                       |
| **Gatilho de Decisão**                   | Caso a precisão das sugestões ficasse abaixo de 70%, o agente conversacional seria revertido para modelo de recomendação assistida estática.     |

---

## Como Executar Localmente

### 1. Clonar e Instalar Dependências

```bash
git clone https://github.com/tiago-coderia/hering-ai-first-remanejamento.git
cd hering-ai-first-remanejamento

python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Rodar a Interface de Demonstração (Streamlit)

```bash
streamlit run app/ui.py
```

Acesse: [http://localhost:8501](http://localhost:8501)

### 3. Rodar a API FastAPI (Swagger)

```bash
uvicorn app.main:app --reload --port 8000
```

Documentação interativa: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Executar via Docker

```bash
docker compose up --build
```

---

## Meta-Análise: Uso de IA e Senso Crítico de Engenharia

Durante a concepção técnica, modelos generativos propuseram arquiteturas distribuídas com microsserviços segregados e orquestração assíncrona por mensageria.

**A decisão crítica de engenharia humana** foi descartar a complexidade prematura em favor de um monólito modular enxuto. Isso reduziu custos de infraestrutura, mitigou pontos de falha e viabilizou um ciclo completo de validação dentro da janela estipulada de 10 dias.
