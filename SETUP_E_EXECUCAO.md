# Guia de Setup e Execução Local

Este guia orienta a configuração e execução da Prova de Conceito (PoC) da **Engine de Remanejamento Preditivo AI First - Cia. Hering**.

---

## 📋 Pré-requisitos

- **Python 3.10+** instalado (ou Docker Desktop)
- **VS Code** instalado
- Terminal (PowerShell, CMD ou Bash)

---

## 🚀 Método 1: Execução Local Rápida com Python (Recomendado)

### 1. Abrir o projeto no VS Code

Abra a pasta do projeto:

```powershell
cd "C:\Users\Tiago\Desktop\Desafio Tecnico Hering - PremiereSoft\hering-ai-first-remanejamento"
code .
```

### 2. Criar e Ativar o Ambiente Virtual

No terminal integrado do VS Code (`Ctrl + '` ou `Terminal > New Terminal`):

**No Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

_(Se houver erro de permissão no PowerShell, execute: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` e tente ativar novamente)._

**No Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as Dependências

Com o ambiente ativado `(venv)`:

```bash
pip install -r requirements.txt
```

### 4. Executar a Interface Interativa (Streamlit)

```bash
streamlit run app/ui.py
```

O navegador abrirá automaticamente no endereço: `http://localhost:8501`.

### 5. (Opcional) Executar a API FastAPI em paralelo

Em um novo terminal com a `venv` ativada:

```bash
uvicorn app.main:app --reload --port 8000
```

- **Swagger / Documentação da API:** Acesse `http://localhost:8000/docs`.

---

## 🐳 Método 2: Execução via Docker Compose

Se preferir rodar em contêineres isolados sem configurar Python localmente:

```bash
docker compose up --build
```

- **Interface Streamlit:** `http://localhost:8501`
- **API FastAPI / Swagger:** `http://localhost:8000/docs`

Para parar os contêineres:

```bash
docker compose down
```

---

## 🧪 Roteiro de Teste do Avaliador

1. Acesse `http://localhost:8501`.
2. No painel à esquerda, selecione a loja **"Hering Store - Shopping Neumarkt (Blumenau)"**.
3. Deixe a mensagem de simulação de ruptura de grade (Camiseta Básica Branca M).
4. Clique em **"🤖 Acionar Agente Preditivo"**.
5. Observe a resposta:
   - Diagnóstico autônomo da ruptura.
   - Sugestão de remanejamento priorizando a loja mais próxima com estoque folgado (_Norte Shopping_).
   - Formatação pronta para consumo via Teams/Chat.
   - Botão de execução direta simulando a emissão da ordem no WMS/ERP em 1 clique.
