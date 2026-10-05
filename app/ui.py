import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "app"))

import streamlit as st
import pandas as pd
import datetime

try:
    from app.agent import analisar_remanejamento_inteligente
    from app.models import SolicitacaoLojista
    from app.database import LOJAS, ESTOQUE_ATUAL
except ImportError:
    from agent import analisar_remanejamento_inteligente
    from models import SolicitacaoLojista
    from database import LOJAS, ESTOQUE_ATUAL

st.set_page_config(page_title="Hering AI First - Remanejamento", page_icon="👕", layout="wide")

# Inicializa o estoque e estados na sessão do Streamlit
if "estoque" not in st.session_state:
    st.session_state.estoque = [item.copy() for item in ESTOQUE_ATUAL]

if "resultado_analise" not in st.session_state:
    st.session_state.resultado_analise = None

if "ordem_executada" not in st.session_state:
    st.session_state.ordem_executada = False

if "historico_ordens" not in st.session_state:
    st.session_state.historico_ordens = []

st.title("👕 Cia. Hering - Gestão e Remanejamento AI First")
st.caption("Protótipo Funcional (PoC) | Desafio Técnico de Desenvolvedor IA")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Simular Solicitação da Loja")
    loja_selecionada = st.selectbox(
        "Selecione a Loja Solicitante:",
        options=list(LOJAS.keys()),
        format_func=lambda k: LOJAS[k]["nome"]
    )
    
    msg_padrao = "Identificamos alta procura por camisetas básicas brancas M e nosso estoque zerou esta tarde. Precisamos de reposição urgente."
    mensagem = st.text_area("Mensagem enviada pelo Gerente via Teams/Chat:", value=msg_padrao, height=120)
    
    if st.button("🤖 Acionar Agente Preditivo", type="primary"):
        st.session_state.ordem_executada = False
        solicitacao = SolicitacaoLojista(loja_origem_id=loja_selecionada, mensagem_usuario=mensagem)
        st.session_state.resultado_analise = analisar_remanejamento_inteligente(solicitacao)

with col2:
    st.subheader("2. Resposta do Agente Autônomo & RAG")
    resultado = st.session_state.resultado_analise
    
    if resultado:
        st.success(f"**Diagnóstico:** {resultado.diagnostico_problema}")
        
        st.markdown("### Sugestão Estruturada para o Teams:")
        st.info(resultado.resumo_executivo_teams)
        
        st.markdown("### Detalhes Técnicos dos Remanejamentos Propostos:")
        for r in resultado.remanejamentos_propostos:
            with st.expander(f"📦 Transferência: {r.produto} ({r.quantidade_sugerida} unidades)", expanded=True):
                st.write(f"**Origem:** {r.origem_nome}")
                st.write(f"**Destino:** {r.destino_nome}")
                st.write(f"**Motivo Preditivo:** {r.motivo_estrategico}")
                
        if resultado.requer_aprovacao_humana_hitl:
            st.warning("⚠️ Esta solicitação exige validação humana (HITL) de acordo com os limites de alçada financeira.")
        elif resultado.remanejamentos_propostos:
            if not st.session_state.ordem_executada:
                if st.button("✅ Executar Remanejamento em 1 Clique (Simular ERP/WMS)"):
                    # Processa a transferência física no estoque da sessão
                    for acao in resultado.remanejamentos_propostos:
                        for item in st.session_state.estoque:
                            if item["loja_id"] == acao.origem_id and item["sku"] == acao.sku:
                                item["saldo"] -= acao.quantidade_sugerida
                            elif item["loja_id"] == acao.destino_id and item["sku"] == acao.sku:
                                item["saldo"] += acao.quantidade_sugerida
                    
                    st.session_state.ordem_executada = True
                    num_ordem = f"WMS-HRG-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                    st.session_state.historico_ordens.append(num_ordem)
                    st.rerun()
            else:
                st.balloons()
                ordem_id = st.session_state.historico_ordens[-1]
                st.success(f"🚀 **Ordem {ordem_id} emitida com sucesso no WMS!**")
                st.markdown("""
                * **Status:** Separação Logística Notificada
                * **Tempo de ciclo:** < 2 segundos (vs. 2 a 3 dias no fluxo AS-IS)
                * **Eliminado:** Nenhuma planilha manual ou e-mail de triagem foi necessário.
                """)
    else:
        st.info("👈 Selecione a loja e clique em 'Acionar Agente Preditivo' para iniciar a simulação.")

st.divider()
st.subheader("📊 Base Operacional de Estoque Atualizado (Visão Omnichannel)")
st.caption("🔴 *Linhas destacadas em vermelho indicam ruptura ou estoque abaixo do mínimo de segurança.*")

# Cria o DataFrame e mapeia o nome da unidade e tipo de loja
df_estoque = pd.DataFrame(st.session_state.estoque)
df_estoque["unidade"] = df_estoque["loja_id"].apply(lambda lid: LOJAS.get(lid, {}).get("nome", lid))
df_estoque["tipo_unidade"] = df_estoque["loja_id"].apply(lambda lid: LOJAS.get(lid, {}).get("tipo", "-"))

# Reorganiza a ordem das colunas
colunas_ordenadas = [
    "loja_id",
    "unidade",
    "tipo_unidade",
    "sku",
    "produto",
    "cor",
    "tam",
    "saldo",
    "min_seguranca",
    "media_venda_dia"
]
df_estoque = df_estoque[colunas_ordenadas]

# Renomeia para exibição amigável
df_display = df_estoque.rename(columns={
    "loja_id": "Cód.",
    "unidade": "Unidade / Loja",
    "tipo_unidade": "Tipo",
    "sku": "SKU",
    "produto": "Produto",
    "cor": "Cor",
    "tam": "Tam",
    "saldo": "Saldo Atual",
    "min_seguranca": "Estoque Mínimo",
    "media_venda_dia": "Média Vendas/Dia"
})

# Função para colorir linhas com estoque baixo
def destacar_estoque_baixo(row):
    if row["Saldo Atual"] < row["Estoque Mínimo"]:
        # Fundo vermelho escuro translúcido com texto destacado (compatível com tema escuro e claro)
        return ['background-color: rgba(239, 68, 68, 0.25); color: #fca5a5; font-weight: 500;'] * len(row)
    return [''] * len(row)

# Aplica o estilo na tabela
df_styled = df_display.style.apply(destacar_estoque_baixo, axis=1)

st.dataframe(df_styled, use_container_width=True, hide_index=True)