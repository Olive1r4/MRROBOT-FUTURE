# 🧪 Guia de Testes e Validação

Este guia detalha como testar o bot de forma segura antes de usar em produção.

## 📋 Checklist de Testes

Antes de usar o bot em modo PROD, complete todos os testes abaixo:

- [ ] Teste 1: Conexões básicas
- [ ] Teste 2: Validação de guardrails
- [ ] Teste 3: Indicadores técnicos
- [ ] Teste 4: Execução de trades simulados
- [ ] Teste 5: Monitoramento e fechamento
- [ ] Teste 6: Circuit breaker
- [ ] Teste 7: Rate limiting
- [ ] Teste 8: Webhook
- [ ] Teste 9: Estresse e recuperação
- [ ] Teste 10: Validação final

---

## ✅ Teste 1: Conexões Básicas

### Objetivo
Verificar se o bot consegue se conectar ao Supabase e à Binance.

### Procedimento

```bash
# 1. Ativar ambiente virtual
source venv/bin/activate

# 2. Iniciar o bot
python -m src.main
```

### Resultado Esperado

```
============================================
🤖 SCALPING BOT INICIADO
============================================
📊 Modo: MOCK
✅ Conectado ao Supabase
✅ Conectado à Binance Futures (MODO SIMULAÇÃO)
INFO: Uvicorn running on http://0.0.0.0:8000
```

### Validação

```bash
# Em outro terminal
curl http://localhost:8000/health
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "mode": "MOCK",
  "exchange_connected": true,
  "circuit_breaker_active": false,
  "today_stats": {
    "total_pnl": 0,
    "total_trades": 0,
    "win_rate": 0
  }
}
```

✅ **Teste passou se:** Status = "healthy" e exchange_connected = true

---

## ✅ Teste 2: Validação de Guardrails

### Objetivo
Verificar se os guardrails de segurança estão funcionando.

### Teste 2.1: Moeda Desativada

```bash
# 1. No Supabase, desative BTCUSDT
# Table Editor > coins_config > BTCUSDT > is_active = false

# 2. Tente executar trade
curl -X POST http://localhost:8000/trade/manual \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT"}'
```

**Resultado esperado:**
```json
{
  "success": false,
  "message": "Trade bloqueado por guardrails de segurança",
  "reasons": ["Moeda: Moeda BTCUSDT desativada"]
}
```

✅ **Teste passou se:** Trade foi bloqueado

### Teste 2.2: Max Open Trades

```bash
# 1. Configure MAX_OPEN_TRADES=1 no .env
# 2. Reinicie o bot
# 3. Execute 2 trades

curl -X POST http://localhost:8000/trade/manual \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT"}'

# Aguarde alguns segundos

curl -X POST http://localhost:8000/trade/manual \
  -H "Content-Type: application/json" \
  -d '{"symbol": "ETHUSDT"}'
```

**Resultado esperado:** Segundo trade deve ser bloqueado com mensagem "Max trades atingido"

✅ **Teste passou se:** Segundo trade foi bloqueado

### Teste 2.3: Cooldown

```bash
# 1. Execute um trade
curl -X POST http://localhost:8000/trade/manual \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT"}'

# 2. Feche o trade imediatamente
curl -X POST http://localhost:8000/trades/1/close

# 3. Tente abrir outro trade da mesma moeda
curl -X POST http://localhost:8000/trade/manual \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT"}'
```

**Resultado esperado:** Trade bloqueado com "Cooldown ativo"

✅ **Teste passou se:** Trade foi bloqueado por cooldown

---

## ✅ Teste 3: Indicadores Técnicos

### Objetivo
Verificar se os indicadores estão sendo calculados corretamente.

### Procedimento

```python
# Crie um arquivo test_indicators.py
from src.indicators import TechnicalIndicators
from src.exchange_manager import ExchangeManager
from src.config import get_config

config = get_config()
exchange = ExchangeManager(config)
indicators = TechnicalIndicators()

# Obter dados
ohlcv = exchange.fetch_ohlcv('BTCUSDT', '5m', limit=500)
close_prices = [candle[4] for candle in ohlcv]

# Calcular indicadores
rsi = indicators.calculate_rsi(close_prices, 14)
bb_upper, bb_middle, bb_lower = indicators.calculate_bollinger_bands(close_prices, 20, 2.0)
ema200 = indicators.calculate_ema(close_prices, 200)
atr = indicators.calculate_atr(ohlcv, 14)

print(f"RSI: {rsi:.2f}")
print(f"Bollinger: [{bb_lower:.2f}, {bb_middle:.2f}, {bb_upper:.2f}]")
print(f"EMA200: {ema200:.2f}")
print(f"ATR: {atr:.2f}")
print(f"Preço atual: {close_prices[-1]:.2f}")
```

```bash
python test_indicators.py
```

**Resultado esperado:**
```
RSI: 45.32
Bollinger: [42100.50, 42500.00, 42899.50]
EMA200: 41800.25
ATR: 180.45
Preço atual: 42350.00
```

### Validação Manual

Compare com TradingView:
1. Abra BTCUSDT no TradingView (5m)
2. Adicione RSI(14), Bollinger(20,2), EMA(200)
3. Compare os valores

✅ **Teste passou se:** Valores estão próximos (diferença < 1%)

---

## ✅ Teste 4: Execução de Trades Simulados

### Objetivo
Executar trades completos em modo MOCK e verificar o fluxo.

### Procedimento

```bash
# 1. Certifique-se de que MODE=MOCK no .env
# 2. Ative BTCUSDT no Supabase (is_active = true)
# 3. Execute trade manual

curl -X POST http://localhost:8000/trade/manual \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT"}'
```

### Acompanhe os Logs

```bash
tail -f logs/scalping_bot.log
```

**Você deve ver:**
```
🚀 INICIANDO TRADE: BTCUSDT
🛡️ Validando entrada de trade...
✅ Todas as validações passaram
📊 Obtendo dados de mercado...
💰 Preço atual: $42,350.00
📈 Analisando indicadores técnicos...
✅ Sinal de entrada CONFIRMADO!
💼 Preparando ordem...
🎯 Take Profit: $42,638.00
🛑 Stop Loss: $42,080.00
🔄 Executando ordem de compra...
🎭 MOCK ORDER: BUY 0.0236 BTCUSDT @ 42350.00
✅ Trade criado com ID: 1
👁️ Monitorando trade 1...
```

### Verificar no Supabase

1. Abra Supabase > Table Editor > trades_history
2. Verifique se o trade foi criado
3. Campos esperados:
   - status = 'open'
   - mode = 'MOCK'
   - entry_price preenchido
   - target_price preenchido
   - stop_loss_price preenchido

✅ **Teste passou se:** Trade foi criado e está sendo monitorado

---

## ✅ Teste 5: Monitoramento e Fechamento

### Objetivo
Verificar se o bot fecha trades automaticamente ao atingir TP ou SL.

### Teste 5.1: Fechamento Manual

```bash
# 1. Abra um trade
curl -X POST http://localhost:8000/trade/manual \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT"}'

# 2. Verifique o ID do trade
curl http://localhost:8000/trades/open

# 3. Feche manualmente
curl -X POST http://localhost:8000/trades/1/close
```

**Resultado esperado:**
```json
{
  "success": true,
  "message": "Trade fechado com sucesso",
  "trade_id": 1,
  "exit_price": 42400.00,
  "pnl": 1.18,
  "pnl_percentage": 0.12
}
```

### Verificar no Supabase

1. Table Editor > trades_history > ID 1
2. Campos esperados:
   - status = 'closed'
   - exit_price preenchido
   - exit_time preenchido
   - pnl preenchido
   - exit_reason = 'Fechamento manual'

✅ **Teste passou se:** Trade foi fechado corretamente

### Teste 5.2: Fechamento Automático (Simulado)

Como estamos em modo MOCK, o fechamento automático por TP/SL não ocorre naturalmente. Para testar:

1. Abra um trade
2. Monitore os logs
3. Aguarde alguns minutos
4. O bot verifica a cada 5 segundos se TP ou SL foi atingido

**Nota:** Em modo MOCK, você precisaria manipular o preço manualmente no código para simular TP/SL.

---

## ✅ Teste 6: Circuit Breaker

### Objetivo
Verificar se o circuit breaker ativa ao atingir o limite de perda diária.

### Procedimento

```sql
-- No Supabase SQL Editor, simule uma perda grande
INSERT INTO daily_pnl (trade_date, total_pnl, total_trades, winning_trades, losing_trades)
VALUES (CURRENT_DATE, -600.00, 10, 2, 8)
ON CONFLICT (trade_date) 
DO UPDATE SET total_pnl = -600.00;
```

```bash
# Tente executar um trade
curl -X POST http://localhost:8000/trade/manual \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT"}'
```

**Resultado esperado:**
```json
{
  "success": false,
  "message": "Trade bloqueado por guardrails de segurança",
  "reasons": ["Daily Stop Loss: Circuit breaker ativado - Perda diária de $600.00"]
}
```

### Verificar no Supabase

```sql
SELECT * FROM daily_pnl WHERE trade_date = CURRENT_DATE;
```

Campo `is_circuit_breaker_active` deve estar `true`.

✅ **Teste passou se:** Circuit breaker foi ativado e bloqueou novos trades

### Limpar Teste

```sql
DELETE FROM daily_pnl WHERE trade_date = CURRENT_DATE;
```

---

## ✅ Teste 7: Rate Limiting

### Objetivo
Verificar se o rate limiter impede excesso de ordens.

### Procedimento

```bash
# Execute 6 trades rapidamente (limite é 5 por minuto)
for i in {1..6}; do
  curl -X POST http://localhost:8000/trade/manual \
    -H "Content-Type: application/json" \
    -d '{"symbol": "BTCUSDT"}' &
done
```

**Resultado esperado:** Pelo menos uma requisição deve ser bloqueada com "Rate limit atingido"

✅ **Teste passou se:** Rate limiter bloqueou requisições excessivas

---

## ✅ Teste 8: Webhook

### Objetivo
Testar recebimento de sinais via webhook.

### Teste 8.1: Webhook Sem Token

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTCUSDT",
    "action": "buy",
    "price": 42500.00
  }'
```

**Resultado esperado:**
```json
{
  "detail": "Token inválido"
}
```

Status HTTP: 401

✅ **Teste passou se:** Webhook rejeitou requisição sem token

### Teste 8.2: Webhook Com Token Correto

```bash
# Pegue o WEBHOOK_SECRET do .env
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "x-webhook-secret: seu_token_aqui" \
  -d '{
    "symbol": "BTCUSDT",
    "action": "buy",
    "price": 42500.00
  }'
```

**Resultado esperado:**
```json
{
  "success": true,
  "message": "Sinal recebido e processamento iniciado",
  "symbol": "BTCUSDT",
  "action": "buy"
}
```

✅ **Teste passou se:** Webhook aceitou e processou o sinal

---

## ✅ Teste 9: Estresse e Recuperação

### Objetivo
Testar comportamento do bot sob carga e após falhas.

### Teste 9.1: Múltiplas Requisições Simultâneas

```bash
# Execute 20 requisições simultâneas
for i in {1..20}; do
  curl -X POST http://localhost:8000/trade/manual \
    -H "Content-Type: application/json" \
    -d '{"symbol": "BTCUSDT"}' &
done

# Aguarde completar
wait
```

**Verificar:**
- Bot não travou
- Logs não mostram erros críticos
- Guardrails funcionaram corretamente

✅ **Teste passou se:** Bot lidou com a carga sem travar

### Teste 9.2: Recuperação Após Reinício

```bash
# 1. Abra alguns trades
# 2. Pare o bot (Ctrl+C)
# 3. Reinicie o bot
python -m src.main
```

**Verificar:**
- Bot reiniciou sem erros
- Conexões foram restabelecidas
- Trades abertos ainda estão no banco

✅ **Teste passou se:** Bot recuperou estado após reinício

### Teste 9.3: Erro de Conexão com Supabase

```bash
# 1. No .env, coloque uma URL inválida do Supabase
SUPABASE_URL=https://invalid.supabase.co

# 2. Tente iniciar o bot
python -m src.main
```

**Resultado esperado:** Bot deve falhar com mensagem clara de erro de conexão.

✅ **Teste passou se:** Erro foi tratado adequadamente

**Restaure a URL correta após o teste!**

---

## ✅ Teste 10: Validação Final

### Checklist Final

Antes de usar em produção, confirme:

#### Configuração
- [ ] Arquivo .env está correto e completo
- [ ] MODE=MOCK (para testes finais)
- [ ] Todas as chaves de API estão corretas
- [ ] WEBHOOK_SECRET é forte e único

#### Banco de Dados
- [ ] Todas as tabelas foram criadas no Supabase
- [ ] Pelo menos 2 moedas estão ativas (is_active = true)
- [ ] Views estão funcionando (daily_stats, performance_by_symbol)

#### Funcionalidades
- [ ] Health check retorna "healthy"
- [ ] Trades podem ser criados e fechados
- [ ] Indicadores técnicos estão corretos
- [ ] Guardrails estão funcionando
- [ ] Circuit breaker ativa corretamente
- [ ] Rate limiter está funcionando
- [ ] Webhook aceita apenas requisições autenticadas

#### Monitoramento
- [ ] Logs estão sendo gerados corretamente
- [ ] Dados estão sendo salvos no Supabase
- [ ] É possível visualizar trades no dashboard do Supabase

#### Segurança
- [ ] .env não está no git (.gitignore configurado)
- [ ] Chaves de API têm permissões mínimas necessárias
- [ ] Webhook requer token secreto
- [ ] Firewall está configurado (se em VPS)

---

## 🎯 Teste em Produção (Com Cautela!)

Após passar em todos os testes acima:

### Fase 1: Produção com Valores Mínimos

```env
# No .env
MODE=PROD
DEFAULT_POSITION_SIZE=10.00  # Apenas $10
DEFAULT_LEVERAGE=5           # Alavancagem baixa
MAX_OPEN_TRADES=1            # Apenas 1 trade por vez
```

**Duração:** 3-7 dias

**Monitorar:**
- Execução real das ordens
- Slippage
- Taxas reais
- Performance vs simulação

### Fase 2: Aumentar Gradualmente

Se tudo estiver OK:

```env
DEFAULT_POSITION_SIZE=50.00  # $50
MAX_OPEN_TRADES=2
```

**Duração:** 7-14 dias

### Fase 3: Valores Normais

Após 2-3 semanas de operação estável:

```env
DEFAULT_POSITION_SIZE=100.00  # $100
DEFAULT_LEVERAGE=10
MAX_OPEN_TRADES=2
```

---

## 📊 Métricas para Acompanhar

### Diariamente

```sql
-- PnL do dia
SELECT * FROM daily_pnl WHERE trade_date = CURRENT_DATE;

-- Trades de hoje
SELECT * FROM trades_history 
WHERE DATE(entry_time) = CURRENT_DATE 
ORDER BY entry_time DESC;

-- Win rate
SELECT 
  COUNT(*) as total,
  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
  ROUND(SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END)::DECIMAL / COUNT(*) * 100, 2) as win_rate
FROM trades_history
WHERE DATE(entry_time) = CURRENT_DATE AND status = 'closed';
```

### Semanalmente

```sql
-- Performance por moeda
SELECT * FROM performance_by_symbol ORDER BY total_pnl DESC;

-- Estatísticas da semana
SELECT 
  SUM(total_pnl) as pnl_semanal,
  SUM(total_trades) as trades_totais,
  ROUND(AVG(total_pnl), 2) as pnl_medio_dia
FROM daily_pnl
WHERE trade_date >= CURRENT_DATE - INTERVAL '7 days';
```

---

## ⚠️ Sinais de Alerta

Pare o bot imediatamente se:

- ❌ Win rate < 40% após 50+ trades
- ❌ Drawdown > 10% em um dia
- ❌ Erros recorrentes nos logs
- ❌ Ordens não estão sendo executadas corretamente
- ❌ Slippage muito alto (> 0.2%)
- ❌ Comportamento inesperado dos indicadores

---

## 📝 Registro de Testes

Mantenha um registro dos seus testes:

```markdown
# Registro de Testes - Bot de Scalping

## Data: 2024-01-19

### Teste 1: Conexões Básicas
- Status: ✅ Passou
- Observações: Conexão estável com Supabase e Binance

### Teste 2: Guardrails
- Status: ✅ Passou
- Observações: Todos os guardrails funcionando corretamente

### Teste 3: Indicadores
- Status: ✅ Passou
- Observações: Valores conferem com TradingView

... (continue para todos os testes)

### Conclusão
- Todos os testes passaram
- Bot pronto para fase 1 de produção
- Próximo passo: Produção com $10 por 7 dias
```

---

## 🎓 Conclusão

Seguir este guia de testes garante que:

1. ✅ O bot está funcionando corretamente
2. ✅ Os guardrails estão protegendo seu capital
3. ✅ Você entende como o bot opera
4. ✅ Está preparado para identificar problemas
5. ✅ Tem confiança para usar em produção

**Nunca pule os testes! Seu capital agradece. 💰**
