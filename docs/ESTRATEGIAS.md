# 📊 Estratégias de Trading Implementadas

Este documento detalha as estratégias e indicadores técnicos utilizados pelo bot.

## 🎯 Visão Geral

O bot utiliza uma estratégia de **Scalping Long** com múltiplos indicadores técnicos para identificar pontos de entrada de alta probabilidade em mercados de tendência de alta.

### Objetivo

- **Lucro alvo:** 0.6% por trade (configurável)
- **Timeframe:** 5 minutos (configurável: 1m, 3m, 5m, 15m)
- **Tipo:** Long apenas (compra para vender mais caro)
- **Estilo:** Scalping (trades rápidos, múltiplas operações por dia)

---

## 📈 Indicadores Técnicos

### 1. RSI (Relative Strength Index)

**O que é:** Indicador de momentum que mede a força relativa de movimentos de preço.

**Como usamos:**
- **Período:** 14 candles (configurável)
- **Sobrevenda:** RSI < 30
- **Sobrecompra:** RSI > 70

**Lógica de entrada:**
```
✅ RSI < 30 → Ativo está sobrevendido, possível reversão para cima
❌ RSI > 30 → Ativo não está sobrevendido suficiente
```

**Cálculo:**
```python
def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gain = pd.Series(gains).ewm(span=period).mean()
    avg_loss = pd.Series(losses).ewm(span=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi
```

---

### 2. Bandas de Bollinger

**O que é:** Indicador de volatilidade que cria bandas ao redor de uma média móvel.

**Como usamos:**
- **Período:** 20 candles (configurável)
- **Desvio padrão:** 2.0 (configurável)
- **Componentes:**
  - Banda superior = SMA + (2 × desvio padrão)
  - Banda média = SMA de 20 períodos
  - Banda inferior = SMA - (2 × desvio padrão)

**Lógica de entrada:**
```
✅ Preço < Banda Inferior → Ativo está sobrevendido, possível reversão
❌ Preço > Banda Inferior → Ativo não está sobrevendido
```

**Interpretação:**
- Quando o preço toca a banda inferior, indica sobrevenda
- Quando o preço toca a banda superior, indica sobrecompra
- Bandas estreitas = baixa volatilidade
- Bandas largas = alta volatilidade

**Cálculo:**
```python
def calculate_bollinger_bands(prices, period=20, std_dev=2.0):
    sma = np.mean(prices[-period:])
    std = np.std(prices[-period:])
    
    upper_band = sma + (std_dev * std)
    lower_band = sma - (std_dev * std)
    
    return upper_band, sma, lower_band
```

---

### 3. EMA 200 (Exponential Moving Average)

**O que é:** Média móvel exponencial que dá mais peso aos preços recentes.

**Como usamos:**
- **Período:** 200 candles (configurável)
- **Função:** Filtro de tendência

**Lógica de entrada:**
```
✅ Preço > EMA 200 → Tendência de alta, permitir operações long
❌ Preço < EMA 200 → Tendência de baixa, BLOQUEAR operações long
```

**Razão:** Evitamos operar contra a tendência principal. Se o preço está abaixo da EMA 200, o mercado está em tendência de baixa e scalping long tem menor probabilidade de sucesso.

**Cálculo:**
```python
def calculate_ema(prices, period=200):
    ema = pd.Series(prices).ewm(span=period, adjust=False).mean()
    return ema.iloc[-1]
```

---

### 4. ATR (Average True Range)

**O que é:** Indicador de volatilidade que mede a amplitude média dos movimentos de preço.

**Como usamos:**
- **Período:** 14 candles (configurável)
- **Função:** Calcular stop loss dinâmico
- **Multiplicador:** 1.5x (configurável)

**Lógica:**
```python
stop_loss = preço_entrada - (ATR × 1.5)
```

**Razão:** 
- Mercado volátil (ATR alto) → Stop loss mais largo
- Mercado calmo (ATR baixo) → Stop loss mais apertado

Isso evita stops prematuros em mercados voláteis e protege melhor em mercados calmos.

**Cálculo:**
```python
def calculate_atr(ohlcv, period=14):
    high = ohlcv['high']
    low = ohlcv['low']
    close = ohlcv['close']
    
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr.iloc[-1]
```

---

## 🎲 Lógica de Entrada

O bot só abre uma posição quando **TODAS** as condições são satisfeitas:

### Condições Técnicas

```python
entrada_permitida = (
    preco_atual < banda_inferior AND  # Sobrevenda (Bollinger)
    rsi < 30 AND                       # Sobrevenda (RSI)
    preco_atual > ema_200              # Tendência de alta (EMA)
)
```

### Condições de Risco (Guardrails)

Além dos indicadores técnicos, o bot verifica:

1. ✅ **Moeda ativa:** Símbolo está habilitado no banco de dados
2. ✅ **Circuit breaker:** PnL diário não atingiu o limite de perda
3. ✅ **Max trades:** Número de trades abertos < limite configurado
4. ✅ **Cooldown:** Passou o período de espera desde o último trade desta moeda
5. ✅ **Rate limit:** Não excedeu o limite de ordens por minuto

**Todas essas condições devem ser TRUE para o trade ser executado.**

---

## 💰 Cálculo de Preços

### Take Profit

```python
take_profit = preco_entrada × (1 + TARGET_PROFIT + (TRADING_FEE × 2))
```

**Exemplo:**
- Preço de entrada: $42,500.00
- TARGET_PROFIT: 0.006 (0.6%)
- TRADING_FEE: 0.0004 (0.04%)

```
take_profit = 42,500 × (1 + 0.006 + 0.0008)
take_profit = 42,500 × 1.0068
take_profit = $42,789.00
```

**Lucro líquido:** $289.00 (0.68%)

### Stop Loss Dinâmico

```python
atr = calculate_atr(ohlcv_data)
stop_loss_distance = atr × ATR_MULTIPLIER
stop_loss = preco_entrada - stop_loss_distance
```

**Exemplo:**
- Preço de entrada: $42,500.00
- ATR: $150.00
- ATR_MULTIPLIER: 1.5

```
stop_loss_distance = 150 × 1.5 = 225
stop_loss = 42,500 - 225 = $42,275.00
```

**Perda máxima:** $225.00 (0.53%)

---

## 🔄 Lógica de Saída

O bot monitora continuamente os trades abertos e fecha quando:

### 1. Take Profit Atingido

```python
if preco_atual >= take_profit:
    fechar_trade("Take profit atingido")
```

### 2. Stop Loss Atingido

```python
if preco_atual <= stop_loss:
    fechar_trade("Stop loss atingido")
```

### 3. Fechamento Manual

Via API ou dashboard.

---

## 📊 Exemplo Prático

### Cenário: BTC/USDT em 5 minutos

**Dados do mercado:**
- Preço atual: $42,350
- RSI(14): 28
- Bollinger Inferior: $42,400
- Bollinger Média: $42,600
- Bollinger Superior: $42,800
- EMA(200): $41,800
- ATR(14): $180

**Análise:**

1. ✅ **RSI = 28 < 30** → Sobrevendido
2. ✅ **Preço ($42,350) < Banda Inferior ($42,400)** → Sobrevenda
3. ✅ **Preço ($42,350) > EMA 200 ($41,800)** → Tendência de alta
4. ✅ **Todos os guardrails passaram**

**Decisão: ENTRAR**

**Cálculo da ordem:**
- **Entrada:** $42,350
- **Quantidade:** 0.0236 BTC (para $1,000 com 10x leverage)
- **Take Profit:** $42,350 × 1.0068 = $42,638
- **Stop Loss:** $42,350 - (180 × 1.5) = $42,080

**Resultado possível:**

**Cenário 1 - Take Profit atingido:**
- Preço sobe para $42,638
- Lucro: $288 (0.68%)
- ✅ Trade vencedor

**Cenário 2 - Stop Loss atingido:**
- Preço cai para $42,080
- Perda: $270 (0.64%)
- ❌ Trade perdedor

**Cenário 3 - Reversão antes do TP:**
- Preço sobe para $42,500 mas não atinge TP
- Depois cai para $42,080
- Perda: $270 (0.64%)
- ❌ Trade perdedor

---

## 🎯 Otimizações Implementadas

### 1. Filtro de Tendência (EMA 200)

**Problema:** Scalping long em tendência de baixa tem baixa taxa de sucesso.

**Solução:** Só operar quando preço > EMA 200.

**Resultado:** Aumenta win rate ao operar apenas a favor da tendência.

### 2. Stop Loss Dinâmico (ATR)

**Problema:** Stop loss fixo não se adapta à volatilidade.

**Solução:** Usar ATR para ajustar o stop dinamicamente.

**Resultado:** 
- Menos stops prematuros em mercados voláteis
- Melhor proteção em mercados calmos

### 3. Dupla Confirmação de Sobrevenda

**Problema:** Um único indicador pode dar falsos sinais.

**Solução:** Exigir RSI < 30 E preço < banda inferior.

**Resultado:** Maior precisão nos sinais de entrada.

---

## 📉 Gestão de Risco

### Risk/Reward Ratio

```
Risk: ~0.64% (stop loss)
Reward: ~0.68% (take profit)
Ratio: 1:1.06
```

**Interpretação:** Para cada $1 arriscado, esperamos ganhar $1.06.

Com uma win rate de 55%, o resultado esperado é positivo:

```
Expectativa = (0.55 × 0.68) - (0.45 × 0.64) = 0.374 - 0.288 = 0.086%
```

**Resultado esperado: +0.086% por trade**

Com 20 trades por dia:
```
0.086% × 20 = 1.72% ao dia
```

### Position Sizing

```python
posicao_usdt = DEFAULT_POSITION_SIZE  # Ex: $100
alavancagem = DEFAULT_LEVERAGE        # Ex: 10x
exposicao_real = posicao_usdt × alavancagem  # $1,000
```

**Importante:** Com alavancagem 10x:
- Lucro de 0.68% = $6.80 em $1,000 expostos
- Perda de 0.64% = $6.40 em $1,000 expostos

---

## 🔧 Parâmetros Ajustáveis

Todos os parâmetros podem ser ajustados no arquivo `.env`:

```env
# Lucro alvo
TARGET_PROFIT=0.006  # 0.6%

# Indicadores
RSI_PERIOD=14
RSI_OVERSOLD=30
BB_PERIOD=20
BB_STD_DEV=2.0
EMA_PERIOD=200
ATR_PERIOD=14
ATR_MULTIPLIER=1.5

# Timeframe
TIMEFRAME=5m

# Alavancagem
DEFAULT_LEVERAGE=10
```

---

## 📚 Sugestões de Melhorias Futuras

### 1. Adicionar Volume Profile

Identificar zonas de suporte/resistência baseadas em volume.

### 2. Implementar Trailing Stop

Stop loss que acompanha o preço quando em lucro.

### 3. Machine Learning

Otimizar parâmetros automaticamente baseado em performance histórica.

### 4. Múltiplos Timeframes

Confirmar sinais em timeframes maiores (ex: 15m, 1h).

### 5. Suporte a Shorts

Implementar lógica para vendas a descoberto em tendências de baixa.

---

## ⚠️ Limitações Conhecidas

1. **Mercados laterais:** Estratégia funciona melhor em tendências claras
2. **Notícias:** Bot não considera eventos fundamentais
3. **Liquidez:** Pode ter dificuldade em moedas de baixa liquidez
4. **Slippage:** Não considera slippage em execução real
5. **Fees:** Fees altas podem consumir o lucro em trades muito rápidos

---

## 📖 Referências

- [RSI - Investopedia](https://www.investopedia.com/terms/r/rsi.asp)
- [Bollinger Bands - Investopedia](https://www.investopedia.com/terms/b/bollingerbands.asp)
- [EMA - Investopedia](https://www.investopedia.com/terms/e/ema.asp)
- [ATR - Investopedia](https://www.investopedia.com/terms/a/atr.asp)

---

**💡 Lembre-se:** Nenhuma estratégia é 100% eficaz. Sempre teste em modo MOCK antes de usar em produção!
