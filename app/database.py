"""
Mock de dados operacionais e de estoque para lojas Hering em Blumenau/SC e CD Central.
"""

LOJAS = {
    "LOJA_01": {"nome": "Hering Store - Shopping Neumarkt (Blumenau)", "tipo": "Franquia", "distancia_cd_km": 6},
    "LOJA_02": {"nome": "Hering Store - Norte Shopping (Blumenau)", "tipo": "Franquia", "distancia_cd_km": 12},
    "LOJA_03": {"nome": "Hering Outlet - Garcia (Blumenau)", "tipo": "Própria", "distancia_cd_km": 8},
    "CD_MATRIZ": {"nome": "Centro de Distribuição Matriz Hering (Blumenau)", "tipo": "CD", "distancia_cd_km": 0}
}

# Saldo de estoque por SKU e Loja
# SKU padrão: HRG-{PRODUTO}-{COR}-{TAMANHO}
ESTOQUE_ATUAL = [
    # Camiseta Básica 100% Algodão - Branca
    {"loja_id": "LOJA_01", "sku": "HRG-BASIC-WHT-M", "produto": "Camiseta Básica Masculina", "cor": "Branca", "tam": "M", "saldo": 2, "min_seguranca": 15, "media_venda_dia": 4.5},
    {"loja_id": "LOJA_01", "sku": "HRG-BASIC-WHT-G", "produto": "Camiseta Básica Masculina", "cor": "Branca", "tam": "G", "saldo": 38, "min_seguranca": 10, "media_venda_dia": 1.2},
    {"loja_id": "LOJA_02", "sku": "HRG-BASIC-WHT-M", "produto": "Camiseta Básica Masculina", "cor": "Branca", "tam": "M", "saldo": 26, "min_seguranca": 10, "media_venda_dia": 1.5},
    {"loja_id": "LOJA_03", "sku": "HRG-BASIC-WHT-M", "produto": "Camiseta Básica Masculina", "cor": "Branca", "tam": "M", "saldo": 18, "min_seguranca": 8, "media_venda_dia": 1.0},
    {"loja_id": "CD_MATRIZ", "sku": "HRG-BASIC-WHT-M", "produto": "Camiseta Básica Masculina", "cor": "Branca", "tam": "M", "saldo": 450, "min_seguranca": 50, "media_venda_dia": 25.0},

    # Camiseta Básica 100% Algodão - Preta
    {"loja_id": "LOJA_01", "sku": "HRG-BASIC-BLK-M", "produto": "Camiseta Básica Masculina", "cor": "Preta", "tam": "M", "saldo": 1, "min_seguranca": 12, "media_venda_dia": 3.8},
    {"loja_id": "LOJA_02", "sku": "HRG-BASIC-BLK-M", "produto": "Camiseta Básica Masculina", "cor": "Preta", "tam": "M", "saldo": 22, "min_seguranca": 8, "media_venda_dia": 1.1},
    {"loja_id": "CD_MATRIZ", "sku": "HRG-BASIC-BLK-M", "produto": "Camiseta Básica Masculina", "cor": "Preta", "tam": "M", "saldo": 620, "min_seguranca": 50, "media_venda_dia": 30.0},
]

POLITICA_REMANEJAMENTO = """
Regras de Negócio de Remanejamento:
1. Priorizar remanejamento entre lojas da mesma praça (raio < 15km) se o doador possuir excedente (> 2x estoque mínimo).
2. Se nenhuma loja vizinha tiver excedente seguro, acionar separação no CD Central.
3. Não transferir itens onde o doador ficará com saldo inferior ao estoque mínimo.
4. Ordens acima de R$ 5.000,00 ou > 50 peças exigem aprovação humana de supervisor (HITL).
"""