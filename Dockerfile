# Imagem base oficial leve do Python
FROM python:3.11-slim

# Evita criação de arquivos .pyc e garante logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Instala dependências do sistema necessárias (curl para healthcheck, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python aproveitando o cache de camadas do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação e o script de inicialização
COPY app/ ./app/
COPY entrypoint.sh .

# Permissão de execução no entrypoint
RUN chmod +x entrypoint.sh

# Portas expostas:
# 8000: API FastAPI / Swagger (/docs)
# 8501: Dashboard Streamlit
EXPOSE 8000 8501

# Healthcheck do container
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
