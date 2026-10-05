from pydantic import BaseModel, Field
from typing import List, Optional

class SolicitacaoLojista(BaseModel):
    loja_origem_id: str = Field(..., example="LOJA_01")
    mensagem_usuario: str = Field(..., example="Estou com ruptura crítica de Camiseta Básica Branca M. Clientes procurando e não tenho na loja.")

class AcaoRemanejamento(BaseModel):
    origem_id: str
    origem_nome: str
    destino_id: str
    destino_nome: str
    sku: str
    produto: str
    quantidade_sugerida: int
    motivo_estrategico: str

class RespostaAgente(BaseModel):
    status: str
    diagnostico_problema: str
    requer_aprovacao_humana_hitl: bool
    remanejamentos_propostos: List[AcaoRemanejamento]
    resumo_executivo_teams: str