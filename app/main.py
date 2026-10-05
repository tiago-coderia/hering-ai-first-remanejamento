from fastapi import FastAPI, HTTPException
from .models import SolicitacaoLojista, RespostaAgente
from .agent import analisar_remanejamento_inteligente

app = FastAPI(
    title="Hering AI First - Engine de Remanejamento de Grade",
    description="Micro-serviço e Agente Preditivo para resolução de ruptura de estoque no varejo.",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {"status": "online", "projeto": "Hering AI First - Desafio Tecnico"}

@app.post("/api/v1/remanejamento/analisar", response_model=RespostaAgente)
def endpoint_analisar_remanejamento(solicitacao: SolicitacaoLojista):
    try:
        return analisar_remanejamento_inteligente(solicitacao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/remanejamento/aprovar-1-clique")
def endpoint_aprovar_ordem(ordem_id: str = "ORD-2026-HERING-001"):
    # Simula integração imediata com ERP/WMS
    return {
        "status": "APROVADO",
        "ordem_id": ordem_id,
        "mensagem": "Ordem de remanejamento emitida com sucesso no WMS! Separação iniciada automaticamente.",
        "notificacao_teams_enviada": True
    }