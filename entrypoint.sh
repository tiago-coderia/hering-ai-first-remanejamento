#!/bin/sh
set -e

# Inicia o FastAPI / Uvicorn em background
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Inicia a interface Streamlit em foreground
exec streamlit run app/ui.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.headless=true
