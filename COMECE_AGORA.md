# 🚀 COMECE AGORA - Tudo Pronto para Testar!

## ✅ Status da Configuração

Você já completou:

- [x] ✅ Banco de dados Supabase criado e configurado
- [x] ✅ Query SQL executada (tabelas criadas)
- [x] ✅ API Keys da Binance (PRODUÇÃO) configuradas
- [x] ✅ Dados do Supabase configurados
- [x] ✅ MODE=MOCK configurado (SEGURO!)

## 🛡️ GARANTIA DE SEGURANÇA

### Sua configuração atual é 100% SEGURA! ✅

```env
MODE=MOCK  ← Ordens são SIMULADAS
BINANCE_API_KEY=sua_chave_real  ← API real (para dados reais)
BINANCE_SECRET_KEY=sua_secret_real  ← API real (para dados reais)
```

### O que acontece:

✅ **Dados REAIS** - Preços, candles, indicadores  
✅ **Análise REAL** - Sinais baseados no mercado real  
🎭 **Ordens SIMULADAS** - Compra/venda NÃO executadas  
🎭 **Saldo SIMULADO** - Seu USDT real NUNCA é tocado  

**RESULTADO:** Teste realista com ZERO risco! 🛡️

---

## 🎯 Próximos Passos (3 Comandos)

### Opção 1: Rodar Localmente

```bash
# 1. Ativar ambiente virtual
cd ~/Projetos/MRROBOT-FUTURE
source venv/bin/activate

# 2. Iniciar o bot
python -m src.main

# Você verá:
# ✅ Conectado à Binance Futures (MODO SIMULAÇÃO)
# ⚠️ Ordens NÃO serão executadas - apenas simuladas!
```

### Opção 2: Rodar com Docker (Recomendado)

```bash
# 1. Copiar .env (se ainda não fez)
cd ~/Projetos/MRROBOT-FUTURE
cp env.template .env

# 2. Deploy
chmod +x scripts/docker-deploy.sh
./scripts/docker-deploy.sh

# Escolha: 1) Desenvolvimento
```

---

## 🧪 Testar o Bot (Após Iniciar)

### 1. Verificar Health

```bash
curl http://localhost:8000/health | jq
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "mode": "MOCK",  ← Confirme que está MOCK
  "exchange_connected": true,
  "circuit_breaker_active": false
}
```

### 2. Executar Trade de Teste

```bash
curl -X POST http://localhost:8000/trade/manual \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT"}'
```

**Resposta esperada:**
```json
{
  "success": true,
  "message": "Trade manual iniciado",
  "symbol": "BTCUSDT"
}
```

### 3. Ver Trades Abertos

```bash
curl http://localhost:8000/trades/open | jq
```

### 4. Ver Logs em Tempo Real

```bash
# Local
tail -f logs/scalping_bot.log

# Docker
docker-compose logs -f
```

**Você verá:**
```
🚀 INICIANDO TRADE: BTCUSDT
💰 Preço atual: $42,350.00  ← Preço REAL
📈 RSI: 28.5  ← Dados REAIS
✅ Sinal de entrada CONFIRMADO!
🎭 MOCK ORDER: BUY 0.0236 BTCUSDT @ 42350.00  ← SIMULADO!
✅ Trade criado com ID: 1
```

---

## 📊 Verificar no Supabase

1. Acesse: https://app.supabase.com
2. Vá em **Table Editor**
3. Abra a tabela **trades_history**
4. Você verá seus trades com `mode = 'MOCK'`

---

## 📱 (OPCIONAL) Configurar Telegram

Receba notificações em tempo real no seu Telegram:

### Configuração Rápida (3 minutos)

```bash
# 1. Criar bot no Telegram
# Procure por: @BotFather
# Comando: /newbot
# Copie o TOKEN

# 2. Obter seu Chat ID
# Procure por: @userinfobot
# Comando: /start
# Copie o ID

# 3. Adicionar no .env
nano .env

# Adicione:
TELEGRAM_BOT_TOKEN=seu_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui

# 4. Reiniciar bot
docker-compose restart
# ou
python -m src.main
```

**Você receberá notificações de:**
- ✅ Inicialização do bot
- ✅ Cada compra (com indicadores e preços)
- ✅ Cada venda (com lucro/prejuízo)
- ✅ Circuit breaker (se atingir stop diário)

**Guias:**
- 📱 [TELEGRAM_QUICKSTART.md](TELEGRAM_QUICKSTART.md) - Configuração detalhada
- 📖 [docs/TELEGRAM_SETUP.md](docs/TELEGRAM_SETUP.md) - Guia completo
- 📊 [TELEGRAM_EXEMPLO.txt](TELEGRAM_EXEMPLO.txt) - Exemplos

---

## 🎮 Comandos Úteis

### Ver Estatísticas

```bash
curl http://localhost:8000/stats | jq
```

### Ver Moedas Ativas

```bash
curl http://localhost:8000/config/coins | jq
```

### Fechar Trade Manualmente

```bash
curl -X POST http://localhost:8000/trades/1/close
```

### Ativar/Desativar Moeda

```bash
curl -X POST http://localhost:8000/config/coins/ETHUSDT/toggle
```

---

## 🔍 Monitoramento Contínuo

### Script de Monitoramento

Crie `monitor.sh`:

```bash
#!/bin/bash

while true; do
  clear
  echo "=========================================="
  echo "🤖 BOT DE SCALPING - MONITORAMENTO"
  echo "=========================================="
  echo ""
  
  echo "🏥 SAÚDE:"
  curl -s http://localhost:8000/health | jq -r '.status, .mode'
  echo ""
  
  echo "📊 TRADES ABERTOS:"
  curl -s http://localhost:8000/trades/open | jq -r '.count'
  echo ""
  
  echo "📈 ESTATÍSTICAS HOJE:"
  curl -s http://localhost:8000/stats?days=1 | jq -r '.statistics.total_pnl, .statistics.total_trades, .statistics.win_rate'
  echo ""
  
  sleep 10
done
```

```bash
chmod +x monitor.sh
./monitor.sh
```

---

## ⚠️ Sinais de que Está Funcionando

### ✅ Logs Corretos

```
✅ Conectado à Binance Futures (MODO SIMULAÇÃO)
⚠️ Ordens NÃO serão executadas - apenas simuladas!
📊 Obtendo dados de mercado...
💰 Preço atual: $XX,XXX.XX
🎭 MOCK ORDER: ...
```

### ✅ Health Check OK

```json
{
  "status": "healthy",
  "mode": "MOCK"
}
```

### ✅ Trades no Banco

```sql
SELECT * FROM trades_history WHERE mode = 'MOCK';
-- Mostra trades simulados
```

---

## 🐛 Troubleshooting

### Erro: "Erro ao conectar ao Supabase"

```bash
# Verificar URL e KEY no .env
cat .env | grep SUPABASE
```

### Erro: "Erro ao conectar à Binance"

```bash
# Testar API
curl https://api.binance.com/api/v3/ping

# Verificar keys
cat .env | grep BINANCE_API_KEY
```

### Bot não inicia

```bash
# Ver logs de erro
tail -n 50 logs/scalping_bot.log

# Verificar dependências
pip list | grep -E "fastapi|ccxt|supabase"
```

### Porta 8000 em uso

```bash
# Verificar o que está usando
lsof -i :8000

# Ou mudar porta no .env
WEBHOOK_PORT=8001
```

---

## 📈 Análise de Resultados

### Após 24 horas de teste:

```sql
-- No Supabase SQL Editor

-- PnL total
SELECT SUM(pnl) as total_pnl 
FROM trades_history 
WHERE mode = 'MOCK' AND status = 'closed';

-- Win rate
SELECT 
  COUNT(*) as total,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END)::DECIMAL / COUNT(*) * 100, 2) as win_rate
FROM trades_history 
WHERE mode = 'MOCK' AND status = 'closed';

-- Performance por moeda
SELECT 
  symbol,
  COUNT(*) as trades,
  SUM(pnl) as total_pnl,
  AVG(pnl_percentage) as avg_pnl_pct
FROM trades_history 
WHERE mode = 'MOCK' AND status = 'closed'
GROUP BY symbol
ORDER BY total_pnl DESC;
```

---

## 🎯 Checklist de Teste (7 Dias)

### Dia 1
- [ ] Bot iniciado com sucesso
- [ ] Health check OK
- [ ] Primeiro trade executado (simulado)
- [ ] Logs mostram "MOCK ORDER"
- [ ] Trade aparece no Supabase com mode='MOCK'

### Dia 2-3
- [ ] Bot rodando 24/7 sem erros
- [ ] Múltiplos trades executados
- [ ] Indicadores calculando corretamente
- [ ] Guardrails funcionando (cooldown, max trades, etc)

### Dia 4-5
- [ ] Analisar win rate
- [ ] Analisar PnL simulado
- [ ] Verificar qualidade dos sinais
- [ ] Ajustar parâmetros se necessário

### Dia 6-7
- [ ] Resultados consistentes
- [ ] Entendimento completo do funcionamento
- [ ] Confiança no sistema
- [ ] Decisão: continuar testando ou considerar PROD

---

## 🚦 Quando Considerar PROD

**APENAS se TODOS forem verdadeiros:**

- [ ] Testou por **mínimo 7 dias** em MOCK
- [ ] Win rate > 50%
- [ ] PnL simulado positivo
- [ ] Entende 100% como funciona
- [ ] Está preparado para perder dinheiro
- [ ] Vai começar com **$10-20 apenas**
- [ ] Vai monitorar 24/7 inicialmente

**Se algum for falso, continue em MOCK!**

---

## 📞 Suporte

### Documentação
- [TESTE_SEGURO.md](TESTE_SEGURO.md) - Explicação detalhada
- [README.md](README.md) - Documentação completa
- [docs/TESTES.md](docs/TESTES.md) - Guia de testes

### Logs
```bash
tail -f logs/scalping_bot.log
```

### Supabase
- Dashboard: https://app.supabase.com
- Table Editor: Ver trades em tempo real

---

## 🎉 Pronto para Começar!

Execute agora:

```bash
# Local
cd ~/Projetos/MRROBOT-FUTURE
source venv/bin/activate
python -m src.main

# Docker
cd ~/Projetos/MRROBOT-FUTURE
./scripts/docker-deploy.sh
```

**Em outro terminal:**

```bash
# Teste
curl -X POST http://localhost:8000/trade/manual \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT"}'

# Monitore
tail -f logs/scalping_bot.log
```

---

**🛡️ Lembre-se: MODE=MOCK = 100% SEGURO!**

**Seu saldo NUNCA será tocado em modo MOCK!**

**📈 Happy Testing! 🚀**
