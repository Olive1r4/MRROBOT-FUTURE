#!/bin/bash

# ============================================
# SCRIPT DE INICIALIZAÇÃO DO BOT DE SCALPING
# ============================================

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "============================================"
echo "🤖 BOT DE SCALPING - BINANCE FUTURES"
echo "============================================"
echo -e "${NC}"

# Verificar se está no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ Erro: Execute este script a partir do diretório raiz do projeto${NC}"
    exit 1
fi

# Verificar se arquivo .env existe
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Arquivo .env não encontrado!${NC}"
    echo "Criando a partir do template..."
    if [ -f "env.template" ]; then
        cp env.template .env
        echo -e "${GREEN}✅ Arquivo .env criado${NC}"
        echo -e "${YELLOW}⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais antes de continuar!${NC}"
        echo "Execute: nano .env"
        exit 1
    else
        echo -e "${RED}❌ Template não encontrado!${NC}"
        exit 1
    fi
fi

# Verificar Python
echo -e "${BLUE}🐍 Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 não está instalado${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python ${PYTHON_VERSION} encontrado${NC}"

# Verificar/criar ambiente virtual
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 Criando ambiente virtual...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Ambiente virtual criado${NC}"
fi

# Ativar ambiente virtual
echo -e "${BLUE}🔄 Ativando ambiente virtual...${NC}"
source venv/bin/activate

# Atualizar pip
echo -e "${BLUE}⬆️  Atualizando pip...${NC}"
pip install --upgrade pip -q

# Instalar dependências
echo -e "${BLUE}📦 Instalando dependências...${NC}"
pip install -r requirements.txt -q
echo -e "${GREEN}✅ Dependências instaladas${NC}"

# Criar diretório de logs
mkdir -p logs
echo -e "${GREEN}✅ Diretório de logs criado${NC}"

# Verificar variáveis de ambiente críticas
echo -e "${BLUE}🔍 Verificando configurações...${NC}"

source .env

MISSING_VARS=0

if [ -z "$BINANCE_API_KEY" ] || [ "$BINANCE_API_KEY" = "your_binance_api_key_here" ]; then
    echo -e "${RED}❌ BINANCE_API_KEY não configurada${NC}"
    MISSING_VARS=1
fi

if [ -z "$BINANCE_SECRET_KEY" ] || [ "$BINANCE_SECRET_KEY" = "your_binance_secret_key_here" ]; then
    echo -e "${RED}❌ BINANCE_SECRET_KEY não configurada${NC}"
    MISSING_VARS=1
fi

if [ -z "$SUPABASE_URL" ] || [ "$SUPABASE_URL" = "https://your-project.supabase.co" ]; then
    echo -e "${RED}❌ SUPABASE_URL não configurada${NC}"
    MISSING_VARS=1
fi

if [ -z "$SUPABASE_KEY" ] || [ "$SUPABASE_KEY" = "your_supabase_anon_key_here" ]; then
    echo -e "${RED}❌ SUPABASE_KEY não configurada${NC}"
    MISSING_VARS=1
fi

if [ -z "$WEBHOOK_SECRET" ] || [ "$WEBHOOK_SECRET" = "your_webhook_secret_token_here" ]; then
    echo -e "${RED}❌ WEBHOOK_SECRET não configurada${NC}"
    MISSING_VARS=1
fi

if [ $MISSING_VARS -eq 1 ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Configure as variáveis de ambiente no arquivo .env antes de iniciar${NC}"
    echo "Execute: nano .env"
    exit 1
fi

echo -e "${GREEN}✅ Configurações válidas${NC}"

# Exibir configurações
echo ""
echo -e "${BLUE}📊 CONFIGURAÇÕES ATUAIS:${NC}"
echo -e "   Modo: ${YELLOW}${MODE:-MOCK}${NC}"
echo -e "   Lucro alvo: ${TARGET_PROFIT:-0.006}"
echo -e "   Alavancagem: ${DEFAULT_LEVERAGE:-10}x"
echo -e "   Max trades: ${MAX_OPEN_TRADES:-2}"
echo -e "   Timeframe: ${TIMEFRAME:-5m}"
echo ""

# Perguntar se deseja continuar
if [ "$MODE" = "PROD" ]; then
    echo -e "${RED}⚠️  ATENÇÃO: Modo PRODUÇÃO ativo - Operações REAIS serão executadas!${NC}"
    read -p "Deseja continuar? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Operação cancelada."
        exit 0
    fi
fi

# Iniciar bot
echo ""
echo -e "${GREEN}"
echo "============================================"
echo "🚀 INICIANDO BOT DE SCALPING"
echo "============================================"
echo -e "${NC}"
echo ""
echo "Para parar o bot, pressione Ctrl+C"
echo ""

# Iniciar aplicação
python -m src.main
