# 🛡️ TESTE SEGURO - API Real com Ordens Simuladas

## ✅ Configuração Atual (SEGURA)

Você configurou perfeitamente! Aqui está o que acontece:

### 📊 MODE=MOCK (RECOMENDADO PARA TESTES)

```env
MODE=MOCK  # ← Este é o modo SEGURO
```

## 🔐 Como Funciona MODE=MOCK

### ✅ O que é REAL (Leitura de Dados)

Quando `MODE=MOCK`, o bot **USA API REAL da Binance** para:

✅ **Obter preços atuais** - Preço real de mercado  
✅ **Obter dados OHLCV** - Candles reais para indicadores  
✅ **Calcular indicadores** - RSI, Bollinger, EMA, ATR com dados reais  
✅ **Verificar mercado** - Status real de moedas  
✅ **Análise técnica** - Sinais baseados em dados reais  

### 🎭 O que é SIMULADO (Execução)

Mas **TODAS AS ORDENS são SIMULADAS**:

🎭 **Ordens de compra** - Simuladas (não gasta USDT real)  
🎭 **Ordens de venda** - Simuladas (não vende moedas reais)  
🎭 **Modificação de posições** - Simulada  
🎭 **Cancelamento de ordens** - Simulado  

## 🧪 Exemplo Prático

### Quando você executa um trade em MODE=MOCK:

```python
# 1. Bot obtém PREÇO REAL da Binance
preço_real = 42,350.00  # ← Preço real do mercado

# 2. Bot calcula indicadores com DADOS REAIS
rsi_real = 28.5  # ← RSI calculado com dados reais
bollinger_real = [42100, 42500, 42900]  # ← Bollinger com dados reais

# 3. Bot decide entrar (baseado em DADOS REAIS)
"✅ Sinal de entrada confirmado"

# 4. Bot SIMULA a ordem (NÃO EXECUTA NA BINANCE)
ordem = {
    'id': 'MOCK_1001',  # ← ID simulado
    'symbol': 'BTCUSDT',
    'side': 'buy',
    'amount': 0.0236,
    'price': 42350.00,
    'status': 'closed',
    'info': {'mock': True}  # ← IMPORTANTE: Ordem simulada!
}

# 5. Bot salva no banco (para análise)
# Mas NÃO executa na Binance!
```

## 📝 Logs em MODE=MOCK

Você verá logs assim:

```
✅ Conectado à Binance Futures (MODO SIMULAÇÃO)
⚠️ Ordens NÃO serão executadas - apenas simuladas!

💰 Preço atual: $42,350.00  ← Preço REAL
📈 RSI: 28.5  ← Calculado com dados REAIS
✅ Sinal de entrada CONFIRMADO!

🎭 MOCK ORDER: BUY 0.0236 BTCUSDT @ 42350.00  ← SIMULADO
✅ Trade criado com ID: 1

👁️ Monitorando trade 1...
💰 Preço atual: $42,638.00  ← Preço REAL sendo monitorado
🎭 MOCK ORDER: SELL 0.0236 BTCUSDT @ 42638.00  ← SIMULADO
✅ Trade fechado - PnL: $6.80 (+0.68%)  ← Lucro SIMULADO
```

## 🔒 Garantias de Segurança

### ✅ Seu Saldo NUNCA é Tocado

```python
# No código (exchange_manager.py):

if self.mode == "PROD":
    # Executa ordem REAL na Binance
    order = self.exchange.create_market_buy_order(symbol, amount)
else:
    # Executa ordem SIMULADA (MockExecutor)
    order = self.mock_executor.create_market_order(
        symbol, 'buy', amount, price=price
    )
```

### ✅ Verificação Visual

Quando o bot inicia, você vê:

```
============================================
🤖 SCALPING BOT INICIADO
============================================
📊 Modo: MOCK  ← Confirme que está MOCK
✅ Conectado à Binance Futures (MODO SIMULAÇÃO)
⚠️ Ordens NÃO serão executadas - apenas simuladas!
============================================
```

### ✅ Verificação no Banco

No Supabase, trades têm:

```sql
SELECT mode FROM trades_history WHERE id = 1;
-- Resultado: 'MOCK'  ← Confirmação que foi simulado
```

## 🎯 Como Testar Agora

### 1. Verifique o .env

```bash
cat .env | grep MODE
# Deve mostrar: MODE=MOCK
```

### 2. Inicie o Bot

```bash
# Local
source venv/bin/activate
python -m src.main

# Docker
./scripts/docker-deploy.sh
```

### 3. Execute um Trade de Teste

```bash
# Trade manual
curl -X POST http://localhost:8000/trade/manual \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT"}'
```

### 4. Verifique os Logs

```bash
# Local
tail -f logs/scalping_bot.log

# Docker
docker-compose logs -f
```

### 5. Verifique no Supabase

```sql
-- Ver trades simulados
SELECT * FROM trades_history 
WHERE mode = 'MOCK' 
ORDER BY entry_time DESC;

-- Deve mostrar trades com mode='MOCK'
```

## 🔄 Quando Mudar para PROD

**APENAS** quando:

1. ✅ Testou em MOCK por **pelo menos 7 dias**
2. ✅ Analisou os resultados e está satisfeito
3. ✅ Entende completamente como funciona
4. ✅ Está pronto para usar dinheiro real
5. ✅ Começa com **valores MUITO pequenos** ($10-20)

**Mudar para PROD:**

```env
# No .env
MODE=PROD  # ⚠️ CUIDADO: Ordens REAIS!
DEFAULT_POSITION_SIZE=10.00  # Comece PEQUENO
```

## 📊 Comparação MODE=MOCK vs MODE=PROD

| Aspecto | MODE=MOCK | MODE=PROD |
|---------|-----------|-----------|
| **Preços** | ✅ Reais | ✅ Reais |
| **Indicadores** | ✅ Reais | ✅ Reais |
| **Análise** | ✅ Real | ✅ Real |
| **Ordens** | 🎭 Simuladas | ⚠️ **REAIS** |
| **Saldo** | 🎭 Simulado | ⚠️ **REAL** |
| **Risco** | ✅ Zero | ⚠️ **Alto** |
| **Ideal para** | ✅ Testes | Produção |

## 🎓 Exemplo de Teste Completo

### Dia 1-7: MOCK com API Real

```bash
# .env
MODE=MOCK
BINANCE_API_KEY=sua_chave_real_aqui  # ← API Real
BINANCE_SECRET_KEY=sua_secret_real_aqui  # ← API Real

# Resultado:
# - Dados 100% reais
# - Análise 100% real
# - Ordens 100% simuladas
# - Saldo NUNCA é tocado
```

**Monitore:**
- Win rate
- PnL simulado
- Frequência de trades
- Qualidade dos sinais

### Dia 8+: Se tudo OK, considere PROD

```bash
# .env
MODE=PROD  # ⚠️ Apenas se confiante!
DEFAULT_POSITION_SIZE=10.00  # COMECE PEQUENO!
```

## ✅ Checklist Antes de Iniciar

- [x] API Keys da Binance configuradas (PRODUÇÃO) ✅
- [x] Supabase configurado e query executada ✅
- [x] MODE=MOCK no .env ✅
- [ ] Bot iniciado e logs verificados
- [ ] Trade de teste executado
- [ ] Logs mostram "MOCK ORDER"
- [ ] Supabase mostra mode='MOCK'
- [ ] Entendeu completamente o funcionamento

## 🆘 Se Tiver Dúvidas

**Pergunta:** "O bot vai gastar meu dinheiro?"  
**Resposta:** NÃO! Em MODE=MOCK, ordens são 100% simuladas.

**Pergunta:** "Por que usar API real então?"  
**Resposta:** Para testar com dados reais de mercado, não simulados. Melhor teste!

**Pergunta:** "Como sei que está simulado?"  
**Resposta:** Veja logs: "🎭 MOCK ORDER" e banco: mode='MOCK'

**Pergunta:** "Posso deixar rodando 24/7 em MOCK?"  
**Resposta:** SIM! É 100% seguro. Zero risco.

**Pergunta:** "Quando mudar para PROD?"  
**Resposta:** Após 7+ dias de testes e começar com $10-20.

## 🎉 Pronto!

Você está **100% seguro** para testar!

**Comandos para começar:**

```bash
# 1. Verificar configuração
cat .env | grep MODE
# Deve mostrar: MODE=MOCK

# 2. Iniciar bot
python -m src.main

# 3. Em outro terminal, executar trade teste
curl -X POST http://localhost:8000/trade/manual \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT"}'

# 4. Ver logs
tail -f logs/scalping_bot.log
```

**Veja nos logs:**
```
✅ Conectado à Binance Futures (MODO SIMULAÇÃO)
⚠️ Ordens NÃO serão executadas - apenas simuladas!
🎭 MOCK ORDER: ...
```

---

**🛡️ Seu saldo está 100% SEGURO em MODE=MOCK!**

**📈 Teste tranquilo e Happy Trading! 🚀**
