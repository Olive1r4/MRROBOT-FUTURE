#!/bin/bash

# ============================================
# SCRIPT DE VERIFICAÇÃO DE SAÚDE DO BOT
# ============================================

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

HOST="localhost"
PORT="8000"

echo -e "${BLUE}"
echo "============================================"
echo "🏥 VERIFICAÇÃO DE SAÚDE DO BOT"
echo "============================================"
echo -e "${NC}"

# Verificar se serviço está rodando
echo -e "${BLUE}🔍 Verificando serviço...${NC}"
if systemctl is-active --quiet scalping-bot; then
    echo -e "${GREEN}✅ Serviço está rodando${NC}"
else
    echo -e "${RED}❌ Serviço NÃO está rodando${NC}"
    echo "Para iniciar: sudo systemctl start scalping-bot"
    exit 1
fi

# Verificar se porta está aberta
echo -e "${BLUE}🔍 Verificando porta ${PORT}...${NC}"
if netstat -tuln 2>/dev/null | grep -q ":${PORT} " || ss -tuln 2>/dev/null | grep -q ":${PORT} "; then
    echo -e "${GREEN}✅ Porta ${PORT} está aberta${NC}"
else
    echo -e "${RED}❌ Porta ${PORT} NÃO está respondendo${NC}"
    exit 1
fi

# Verificar endpoint de saúde
echo -e "${BLUE}🔍 Verificando API...${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" http://${HOST}:${PORT}/health 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ API está saudável (HTTP $HTTP_CODE)${NC}"
    
    # Extrair informações do JSON
    MODE=$(echo "$BODY" | grep -o '"mode":"[^"]*"' | cut -d'"' -f4)
    STATUS=$(echo "$BODY" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    
    echo ""
    echo -e "${BLUE}📊 INFORMAÇÕES:${NC}"
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
else
    echo -e "${RED}❌ API retornou erro (HTTP $HTTP_CODE)${NC}"
    echo "$BODY"
    exit 1
fi

# Verificar trades abertos
echo ""
echo -e "${BLUE}🔍 Verificando trades abertos...${NC}"
TRADES_RESPONSE=$(curl -s http://${HOST}:${PORT}/trades/open 2>/dev/null)
TRADES_COUNT=$(echo "$TRADES_RESPONSE" | grep -o '"count":[0-9]*' | cut -d':' -f2)

if [ ! -z "$TRADES_COUNT" ]; then
    if [ "$TRADES_COUNT" -eq 0 ]; then
        echo -e "${YELLOW}⚠️  Nenhum trade aberto${NC}"
    else
        echo -e "${GREEN}✅ $TRADES_COUNT trade(s) aberto(s)${NC}"
        echo "$TRADES_RESPONSE" | python3 -m json.tool 2>/dev/null
    fi
else
    echo -e "${RED}❌ Não foi possível obter trades${NC}"
fi

# Verificar logs recentes
echo ""
echo -e "${BLUE}📋 ÚLTIMAS LINHAS DO LOG:${NC}"
echo "-------------------------------------------"
if [ -f "logs/scalping_bot.log" ]; then
    tail -n 5 logs/scalping_bot.log
else
    sudo journalctl -u scalping-bot -n 5 --no-pager 2>/dev/null || echo "Logs não disponíveis"
fi

echo ""
echo -e "${GREEN}"
echo "============================================"
echo "✅ VERIFICAÇÃO CONCLUÍDA"
echo "============================================"
echo -e "${NC}"
