#!/bin/bash

# ============================================
# SCRIPT DE DEPLOY DOCKER
# ============================================

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "============================================"
echo "🐳 DEPLOY DOCKER - BOT DE SCALPING"
echo "============================================"
echo -e "${NC}"

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker não está instalado!${NC}"
    echo "Instale Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose não está instalado!${NC}"
    echo "Instale Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✅ Docker instalado${NC}"
echo -e "${GREEN}✅ Docker Compose instalado${NC}"
echo ""

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Arquivo .env não encontrado!${NC}"
    echo "Criando a partir do template..."
    cp env.template .env
    echo -e "${GREEN}✅ Arquivo .env criado${NC}"
    echo -e "${YELLOW}⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais antes de continuar!${NC}"
    echo "Execute: nano .env"
    exit 1
fi

# Perguntar qual ambiente
echo -e "${BLUE}Escolha o ambiente:${NC}"
echo "1) Desenvolvimento (docker-compose.yml)"
echo "2) Produção (docker-compose.prod.yml)"
read -p "Opção [1]: " ENV_CHOICE
ENV_CHOICE=${ENV_CHOICE:-1}

if [ "$ENV_CHOICE" = "1" ]; then
    COMPOSE_FILE="docker-compose.yml"
    ENV_NAME="DESENVOLVIMENTO"
else
    COMPOSE_FILE="docker-compose.prod.yml"
    ENV_NAME="PRODUÇÃO"
fi

echo ""
echo -e "${BLUE}📦 Ambiente selecionado: ${ENV_NAME}${NC}"
echo ""

# Verificar MODE no .env
MODE=$(grep "^MODE=" .env | cut -d '=' -f2)
echo -e "${BLUE}📊 Modo configurado: ${MODE}${NC}"

if [ "$MODE" = "PROD" ]; then
    echo -e "${RED}⚠️  ATENÇÃO: Modo PRODUÇÃO ativo - Operações REAIS serão executadas!${NC}"
    read -p "Deseja continuar? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Operação cancelada."
        exit 0
    fi
fi

echo ""
echo -e "${BLUE}🔨 Construindo imagem Docker...${NC}"
docker-compose -f $COMPOSE_FILE build

echo ""
echo -e "${BLUE}🚀 Iniciando container...${NC}"
docker-compose -f $COMPOSE_FILE up -d

echo ""
echo -e "${BLUE}⏳ Aguardando inicialização (30s)...${NC}"
sleep 30

echo ""
echo -e "${BLUE}✅ Verificando status...${NC}"
docker-compose -f $COMPOSE_FILE ps

echo ""
echo -e "${BLUE}🏥 Testando health check...${NC}"
if curl -f -s http://localhost:${WEBHOOK_PORT:-8000}/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Bot está saudável e respondendo!${NC}"
else
    echo -e "${YELLOW}⚠️  Bot ainda está inicializando ou há um problema${NC}"
    echo "Verifique os logs: docker-compose -f $COMPOSE_FILE logs -f"
fi

echo ""
echo -e "${GREEN}"
echo "============================================"
echo "✅ DEPLOY CONCLUÍDO COM SUCESSO!"
echo "============================================"
echo -e "${NC}"

echo "📊 Comandos úteis:"
echo ""
echo "  Ver logs em tempo real:"
echo "    docker-compose -f $COMPOSE_FILE logs -f"
echo ""
echo "  Ver status:"
echo "    docker-compose -f $COMPOSE_FILE ps"
echo ""
echo "  Parar:"
echo "    docker-compose -f $COMPOSE_FILE down"
echo ""
echo "  Reiniciar:"
echo "    docker-compose -f $COMPOSE_FILE restart"
echo ""
echo "  Entrar no container:"
echo "    docker-compose -f $COMPOSE_FILE exec scalping-bot /bin/bash"
echo ""
echo "  Ver métricas:"
echo "    docker stats mrrobot-scalping-bot"
echo ""
echo "  Health check:"
echo "    curl http://localhost:${WEBHOOK_PORT:-8000}/health"
echo ""

echo -e "${BLUE}🌐 API disponível em: http://localhost:${WEBHOOK_PORT:-8000}${NC}"
echo ""
