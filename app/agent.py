import os
import json
import re

try:
    from app.database import LOJAS, ESTOQUE_ATUAL, POLITICA_REMANEJAMENTO
    from app.models import SolicitacaoLojista, RespostaAgente, AcaoRemanejamento
except ImportError:
    from database import LOJAS, ESTOQUE_ATUAL, POLITICA_REMANEJAMENTO
    from models import SolicitacaoLojista, RespostaAgente, AcaoRemanejamento


def extrair_filtros_da_mensagem(texto: str):
    """
    Extrai intenção de cor e tamanho da mensagem em linguagem natural do usuário.
    """
    texto_lower = texto.lower()
    
    # Detecção de cor
    cor = None
    if "branc" in texto_lower:
        cor = "Branca"
    elif "pret" in texto_lower:
        cor = "Preta"
    elif "azul" in texto_lower:
        cor = "Azul"
        
    # Detecção de tamanho
    tamanho = None
    match_tam = re.search(r'\b(p|m|g|gg|xg)\b', texto_lower)
    if match_tam:
        tamanho = match_tam.group(1).upper()
        
    return cor, tamanho


def analisar_remanejamento_inteligente(solicitacao: SolicitacaoLojista) -> RespostaAgente:
    loja_solicitante = LOJAS.get(solicitacao.loja_origem_id, {"nome": "Loja Desconhecida"})
    
    # 1. Extrair filtros da mensagem (NLU simples / Intent Recognition)
    cor_filtro, tam_filtro = extrair_filtros_da_mensagem(solicitacao.mensagem_usuario)
    
    # 2. Filtrar os itens da loja solicitante
    itens_loja = [item for item in ESTOQUE_ATUAL if item["loja_id"] == solicitacao.loja_origem_id]
    
    # Se o lojista especificou cor ou tamanho, prioriza estritamente esses itens
    if cor_filtro or tam_filtro:
        itens_em_risco = [
            item for item in itens_loja
            if (not cor_filtro or item["cor"] == cor_filtro) and 
               (not tam_filtro or item["tam"] == tam_filtro) and
               item["saldo"] <= (item["min_seguranca"] * 0.5)
        ]
    else:
        # Se for uma pergunta genérica, avalia todos os itens em ruptura crítica
        itens_em_risco = [
            item for item in itens_loja 
            if item["saldo"] <= (item["min_seguranca"] * 0.3)
        ]
        
    if not itens_em_risco:
        return RespostaAgente(
            status="OK",
            diagnostico_problema=f"Não foram encontradas rupturas críticas para os critérios informados na {loja_solicitante['nome']}.",
            requer_aprovacao_humana_hitl=False,
            remanejamentos_propostos=[],
            resumo_executivo_teams=f"Olá! O estoque para os itens consultados na {loja_solicitante['nome']} encontra-se em níveis aceitáveis."
        )

    acoes: list[AcaoRemanejamento] = []
    
    for item in itens_em_risco:
        sku = item["sku"]
        qtd_necessaria = item["min_seguranca"] - item["saldo"]
        
        # Busca loja vizinha mais próxima com folga de estoque
        doador_encontrado = None
        for candidato in ESTOQUE_ATUAL:
            if candidato["sku"] == sku and candidato["loja_id"] != solicitacao.loja_origem_id:
                folga = candidato["saldo"] - candidato["min_seguranca"]
                if folga >= qtd_necessaria:
                    doador_encontrado = candidato
                    break
        
        if doador_encontrado:
            loja_doadora = LOJAS[doador_encontrado["loja_id"]]
            acoes.append(AcaoRemanejamento(
                origem_id=doador_encontrado["loja_id"],
                origem_nome=loja_doadora["nome"],
                destino_id=solicitacao.loja_origem_id,
                destino_nome=loja_solicitante["nome"],
                sku=sku,
                produto=f"{item['produto']} ({item['cor']} - Tam {item['tam']})",
                quantidade_sugerida=qtd_necessaria,
                motivo_estrategico=f"Loja doadora possui cobertura confortável ({doador_encontrado['saldo']} peças) e distância de apenas {loja_doadora['distancia_cd_km']} km."
            ))
        else:
            # Caso contrário, solicita ao CD Matriz
            cd_info = LOJAS["CD_MATRIZ"]
            acoes.append(AcaoRemanejamento(
                origem_id="CD_MATRIZ",
                origem_nome=cd_info["nome"],
                destino_id=solicitacao.loja_origem_id,
                destino_nome=loja_solicitante["nome"],
                sku=sku,
                produto=f"{item['produto']} ({item['cor']} - Tam {item['tam']})",
                quantidade_sugerida=qtd_necessaria + 10,
                motivo_estrategico="Sem excedente em lojas próximas. Acionamento direto do CD Matriz para reabastecimento."
            ))

    total_pecas = sum(a.quantidade_sugerida for a in acoes)
    precisa_hitl = total_pecas > 50

    diagnostico = f"Detectada ruptura crítica em {len(itens_em_risco)} SKU(s) correspondente(s) à solicitação na {loja_solicitante['nome']}."
    
    detalhes_msg = "\n".join([f"• Transferir **{a.quantidade_sugerida} un** de `{a.produto}` partindo de *{a.origem_nome}*" for a in acoes])
    resumo_teams = (
        f"🤖 **Sugestão de Remanejamento Preditivo Hering**\n\n"
        f"Olá, Gerente! Atendendo à sua solicitação sobre `{cor_filtro or 'Geral'}` (Tam {tam_filtro or 'Geral'}):\n\n"
        f"{detalhes_msg}\n\n"
        f"👉 **Ação recomendada:** Clique no botão abaixo para aprovar a ordem de remanejamento no ERP em 1 clique."
    )
    
    return RespostaAgente(
        status="SUCESSO",
        diagnostico_problema=diagnostico,
        requer_aprovacao_humana_hitl=precisa_hitl,
        remanejamentos_propostos=acoes,
        resumo_executivo_teams=resumo_teams
    )