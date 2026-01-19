# ============================================
# DOCKERFILE - BOT DE SCALPING
# ============================================

# Imagem base Python
FROM python:3.10-slim

# Metadata
LABEL maintainer="MRROBOT-FUTURE"
LABEL description="Bot de Scalping para Binance Futures"
LABEL version="1.0.0"

# Definir diretório de trabalho
WORKDIR /app

# Variáveis de ambiente para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (cache de layers)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar código fonte
COPY src/ ./src/
COPY database/ ./database/
COPY scripts/ ./scripts/
COPY .env .env

# Criar usuário não-root para segurança e configurar permissões
RUN useradd -m -u 1000 botuser && \
    mkdir -p logs && \
    chmod 777 logs && \
    chown -R botuser:botuser /app

# Mudar para usuário não-root
USER botuser

# Expor porta da API
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando padrão
CMD ["python", "-m", "src.main"]
