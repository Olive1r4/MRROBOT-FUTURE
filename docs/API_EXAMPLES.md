# 📡 Exemplos de Uso da API

Guia prático com exemplos de todas as chamadas da API do bot.

## 🔧 Configuração Inicial

### Variáveis de Ambiente

```bash
# Defina estas variáveis para facilitar os testes
export BOT_URL="http://localhost:8000"
export WEBHOOK_SECRET="seu_token_secreto_aqui"
```

---

## 📊 Endpoints de Monitoramento

### 1. Health Check

Verifica se o bot está funcionando.

**Request:**
```bash
curl -X GET ${BOT_URL}/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "mode": "MOCK",
  "exchange_connected": true,
  "circuit_breaker_active": false,
  "today_stats": {
    "total_pnl": 125.50,
    "total_trades": 15,
    "win_rate": 60.0
  },
  "timestamp": "2024-01-19T10:30:00"
}
```

**Uso:**
- Monitoramento de saúde
- Verificar se bot está online
- Integração com ferramentas de monitoramento

---

### 2. Estatísticas

Obtém estatísticas de performance.

**Request:**
```bash
# Últimos 30 dias (padrão)
curl -X GET ${BOT_URL}/stats

# Últimos 7 dias
curl -X GET "${BOT_URL}/stats?days=7"
```

**Response (200 OK):**
```json
{
  "success": true,
  "period_days": 30,
  "statistics": {
    "total_pnl": 1250.75,
    "total_trades": 150,
    "winning_trades": 95,
    "losing_trades": 55,
    "win_rate": 63.33,
    "daily_stats": [
      {
        "trade_date": "2024-01-19",
        "total_pnl": 125.50,
        "total_trades": 15,
        "winning_trades": 10,
        "losing_trades": 5,
        "win_rate_percentage": 66.67,
        "is_circuit_breaker_active": false
      }
    ],
    "performance_by_symbol": [
      {
        "symbol": "BTCUSDT",
        "total_trades": 80,
        "winning_trades": 52,
        "losing_trades": 28,
        "avg_pnl_percentage": 0.45,
        "total_pnl": 650.25
      }
    ]
  }
}
```

**Uso:**
- Dashboard de performance
- Análise de resultados
- Identificar melhores moedas

---

## 🎯 Endpoints de Trading

### 3. Trade Manual

Executa um trade manualmente.

**Request:**
```bash
curl -X POST ${BOT_URL}/trade/manual \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTCUSDT",
    "usdt_amount": 100.00
  }'
```

**Parâmetros:**
- `symbol` (obrigatório): Símbolo da moeda (ex: BTCUSDT)
- `usdt_amount` (opcional): Valor em USDT (usa DEFAULT_POSITION_SIZE se omitido)

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Trade manual iniciado",
  "symbol": "BTCUSDT"
}
```

**Response (Bloqueado):**
```json
{
  "success": false,
  "message": "Trade bloqueado por guardrails de segurança",
  "reasons": [
    "Moeda: Moeda ativa",
    "Daily Stop Loss: Dentro do limite de perda diária",
    "Open Trades: Max trades atingido (2/2): ETHUSDT, BNBUSDT",
    "Cooldown: Primeira operação desta moeda",
    "Rate Limit: Rate limit OK (3/5)"
  ]
}
```

**Uso:**
- Executar trades manualmente
- Testar sinais específicos
- Operação manual em situações especiais

---

### 4. Webhook (Receber Sinais)

Recebe sinais de sistemas externos (TradingView, etc).

**Request:**
```bash
curl -X POST ${BOT_URL}/webhook \
  -H "Content-Type: application/json" \
  -H "x-webhook-secret: ${WEBHOOK_SECRET}" \
  -d '{
    "symbol": "BTCUSDT",
    "action": "buy",
    "price": 42500.00,
    "timestamp": "2024-01-19T10:30:00Z"
  }'
```

**Headers:**
- `x-webhook-secret` (obrigatório): Token de autenticação

**Body:**
- `symbol` (obrigatório): Símbolo da moeda
- `action` (obrigatório): Ação (apenas "buy" é suportado)
- `price` (opcional): Preço sugerido
- `timestamp` (opcional): Timestamp do sinal

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Sinal recebido e processamento iniciado",
  "symbol": "BTCUSDT",
  "action": "buy",
  "received_at": "2024-01-19T10:30:00"
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Token inválido"
}
```

**Uso:**
- Integração com TradingView
- Receber sinais de bots externos
- Automação completa

**Exemplo TradingView:**

No alerta do TradingView, configure:

**Webhook URL:**
```
https://seu-vps.com:8000/webhook
```

**Message:**
```json
{
  "symbol": "{{ticker}}",
  "action": "buy",
  "price": {{close}},
  "timestamp": "{{time}}"
}
```

**Headers:**
```
x-webhook-secret: seu_token_secreto
```

---

## 📋 Endpoints de Gerenciamento de Trades

### 5. Listar Trades Abertos

Lista todos os trades atualmente abertos.

**Request:**
```bash
curl -X GET ${BOT_URL}/trades/open
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 2,
  "trades": [
    {
      "id": 15,
      "symbol": "BTCUSDT",
      "entry_price": 42350.00,
      "quantity": 0.0236,
      "leverage": 10,
      "target_price": 42638.00,
      "stop_loss_price": 42080.00,
      "entry_reason": "✅ Preço acima da EMA200 | ✅ Preço abaixo da banda inferior | ✅ RSI em sobrevenda",
      "mode": "MOCK",
      "entry_time": "2024-01-19T10:30:00",
      "minutes_open": 15.5
    },
    {
      "id": 16,
      "symbol": "ETHUSDT",
      "entry_price": 2250.00,
      "quantity": 0.444,
      "leverage": 10,
      "target_price": 2265.30,
      "stop_loss_price": 2220.00,
      "entry_reason": "✅ Preço acima da EMA200 | ✅ Preço abaixo da banda inferior | ✅ RSI em sobrevenda",
      "mode": "MOCK",
      "entry_time": "2024-01-19T10:35:00",
      "minutes_open": 10.5
    }
  ]
}
```

**Uso:**
- Monitorar trades ativos
- Dashboard em tempo real
- Verificar exposição atual

---

### 6. Obter Trade Específico

Obtém detalhes de um trade por ID.

**Request:**
```bash
curl -X GET ${BOT_URL}/trades/15
```

**Response (200 OK):**
```json
{
  "success": true,
  "trade": {
    "id": 15,
    "symbol": "BTCUSDT",
    "side": "buy",
    "entry_price": 42350.00,
    "exit_price": 42638.00,
    "quantity": 0.0236,
    "leverage": 10,
    "target_price": 42638.00,
    "stop_loss_price": 42080.00,
    "pnl": 6.80,
    "pnl_percentage": 0.68,
    "status": "closed",
    "entry_reason": "✅ Preço acima da EMA200 | ✅ Preço abaixo da banda inferior | ✅ RSI em sobrevenda",
    "exit_reason": "Take profit atingido",
    "order_id_entry": "MOCK_1001",
    "order_id_exit": "MOCK_1002",
    "mode": "MOCK",
    "entry_time": "2024-01-19T10:30:00",
    "exit_time": "2024-01-19T10:45:00"
  }
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Trade não encontrado"
}
```

**Uso:**
- Análise de trade específico
- Auditoria
- Debugging

---

### 7. Fechar Trade Manualmente

Fecha um trade aberto antes de atingir TP ou SL.

**Request:**
```bash
curl -X POST ${BOT_URL}/trades/15/close
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Trade fechado com sucesso",
  "trade_id": 15,
  "exit_price": 42500.00,
  "pnl": 3.54,
  "pnl_percentage": 0.35
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Trade não está aberto"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Trade não encontrado"
}
```

**Uso:**
- Fechar trade em situações especiais
- Emergências
- Ajustes manuais

---

## ⚙️ Endpoints de Configuração

### 8. Listar Moedas Configuradas

Lista todas as moedas e suas configurações.

**Request:**
```bash
curl -X GET ${BOT_URL}/config/coins
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 5,
  "coins": [
    {
      "id": 1,
      "symbol": "BTCUSDT",
      "is_active": true,
      "min_pnl": 0.006,
      "max_position_size": 500.00,
      "leverage": 10,
      "created_at": "2024-01-19T10:00:00",
      "updated_at": "2024-01-19T10:00:00"
    },
    {
      "id": 2,
      "symbol": "ETHUSDT",
      "is_active": true,
      "min_pnl": 0.006,
      "max_position_size": 300.00,
      "leverage": 10,
      "created_at": "2024-01-19T10:00:00",
      "updated_at": "2024-01-19T10:00:00"
    },
    {
      "id": 3,
      "symbol": "BNBUSDT",
      "is_active": false,
      "min_pnl": 0.006,
      "max_position_size": 200.00,
      "leverage": 10,
      "created_at": "2024-01-19T10:00:00",
      "updated_at": "2024-01-19T10:00:00"
    }
  ]
}
```

**Uso:**
- Verificar moedas ativas
- Gerenciar configurações
- Dashboard de configuração

---

### 9. Ativar/Desativar Moeda

Alterna o status de uma moeda (ativa/inativa).

**Request:**
```bash
# Ativar ou desativar BNBUSDT
curl -X POST ${BOT_URL}/config/coins/BNBUSDT/toggle
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Moeda BNBUSDT ativada",
  "symbol": "BNBUSDT",
  "is_active": true
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Moeda não encontrada"
}
```

**Uso:**
- Ativar/desativar moedas rapidamente
- Pausar trading de moedas específicas
- Gerenciamento dinâmico

---

## 🔍 Exemplos de Uso Completos

### Exemplo 1: Monitoramento Contínuo

Script bash para monitorar o bot:

```bash
#!/bin/bash

BOT_URL="http://localhost:8000"

while true; do
  clear
  echo "=========================================="
  echo "BOT DE SCALPING - MONITORAMENTO"
  echo "=========================================="
  echo ""
  
  # Health check
  echo "🏥 SAÚDE:"
  curl -s ${BOT_URL}/health | jq '.status, .mode, .today_stats'
  echo ""
  
  # Trades abertos
  echo "📊 TRADES ABERTOS:"
  curl -s ${BOT_URL}/trades/open | jq '.count, .trades[] | {id, symbol, entry_price, minutes_open}'
  echo ""
  
  # Aguardar 30 segundos
  sleep 30
done
```

**Executar:**
```bash
chmod +x monitor.sh
./monitor.sh
```

---

### Exemplo 2: Fechar Todos os Trades

Script para fechar todos os trades abertos:

```bash
#!/bin/bash

BOT_URL="http://localhost:8000"

# Obter IDs dos trades abertos
TRADE_IDS=$(curl -s ${BOT_URL}/trades/open | jq -r '.trades[].id')

# Fechar cada trade
for ID in $TRADE_IDS; do
  echo "Fechando trade $ID..."
  curl -X POST ${BOT_URL}/trades/${ID}/close
  echo ""
done

echo "Todos os trades foram fechados."
```

---

### Exemplo 3: Integração Python

Cliente Python para interagir com o bot:

```python
import requests
import os

class ScalpingBotClient:
    def __init__(self, base_url, webhook_secret=None):
        self.base_url = base_url
        self.webhook_secret = webhook_secret
    
    def health_check(self):
        """Verifica saúde do bot"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def get_open_trades(self):
        """Lista trades abertos"""
        response = requests.get(f"{self.base_url}/trades/open")
        return response.json()
    
    def execute_trade(self, symbol, usdt_amount=None):
        """Executa trade manual"""
        data = {"symbol": symbol}
        if usdt_amount:
            data["usdt_amount"] = usdt_amount
        
        response = requests.post(
            f"{self.base_url}/trade/manual",
            json=data
        )
        return response.json()
    
    def close_trade(self, trade_id):
        """Fecha um trade"""
        response = requests.post(f"{self.base_url}/trades/{trade_id}/close")
        return response.json()
    
    def get_statistics(self, days=30):
        """Obtém estatísticas"""
        response = requests.get(f"{self.base_url}/stats?days={days}")
        return response.json()
    
    def send_webhook_signal(self, symbol, action="buy", price=None):
        """Envia sinal via webhook"""
        headers = {"x-webhook-secret": self.webhook_secret}
        data = {
            "symbol": symbol,
            "action": action
        }
        if price:
            data["price"] = price
        
        response = requests.post(
            f"{self.base_url}/webhook",
            json=data,
            headers=headers
        )
        return response.json()

# Uso
if __name__ == "__main__":
    client = ScalpingBotClient(
        base_url="http://localhost:8000",
        webhook_secret=os.getenv("WEBHOOK_SECRET")
    )
    
    # Health check
    health = client.health_check()
    print(f"Status: {health['status']}")
    print(f"Modo: {health['mode']}")
    
    # Trades abertos
    trades = client.get_open_trades()
    print(f"Trades abertos: {trades['count']}")
    
    # Executar trade
    result = client.execute_trade("BTCUSDT")
    print(f"Trade executado: {result}")
    
    # Estatísticas
    stats = client.get_statistics(days=7)
    print(f"PnL 7 dias: {stats['statistics']['total_pnl']}")
```

---

### Exemplo 4: Dashboard HTML Simples

```html
<!DOCTYPE html>
<html>
<head>
    <title>Scalping Bot Dashboard</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .trade { background: #f9f9f9; margin: 5px 0; padding: 10px; }
        .profit { color: green; }
        .loss { color: red; }
    </style>
</head>
<body>
    <h1>🤖 Scalping Bot Dashboard</h1>
    
    <div class="card">
        <h2>Status</h2>
        <div id="status"></div>
    </div>
    
    <div class="card">
        <h2>Trades Abertos</h2>
        <div id="trades"></div>
    </div>
    
    <div class="card">
        <h2>Estatísticas Hoje</h2>
        <div id="stats"></div>
    </div>
    
    <script>
        const BOT_URL = 'http://localhost:8000';
        
        async function updateDashboard() {
            // Health
            const health = await fetch(`${BOT_URL}/health`).then(r => r.json());
            document.getElementById('status').innerHTML = `
                <p>Status: ${health.status}</p>
                <p>Modo: ${health.mode}</p>
                <p>Circuit Breaker: ${health.circuit_breaker_active ? '🔴 ATIVO' : '🟢 Inativo'}</p>
            `;
            
            // Trades
            const trades = await fetch(`${BOT_URL}/trades/open`).then(r => r.json());
            document.getElementById('trades').innerHTML = trades.trades.map(t => `
                <div class="trade">
                    <strong>${t.symbol}</strong> - 
                    Entry: $${t.entry_price} - 
                    TP: $${t.target_price} - 
                    SL: $${t.stop_loss_price}
                </div>
            `).join('');
            
            // Stats
            const stats = health.today_stats;
            document.getElementById('stats').innerHTML = `
                <p>PnL: <span class="${stats.total_pnl >= 0 ? 'profit' : 'loss'}">$${stats.total_pnl.toFixed(2)}</span></p>
                <p>Trades: ${stats.total_trades}</p>
                <p>Win Rate: ${stats.win_rate.toFixed(2)}%</p>
            `;
        }
        
        // Atualizar a cada 10 segundos
        updateDashboard();
        setInterval(updateDashboard, 10000);
    </script>
</body>
</html>
```

---

## 🔐 Autenticação e Segurança

### Headers Necessários

Apenas o endpoint `/webhook` requer autenticação:

```bash
-H "x-webhook-secret: seu_token_secreto"
```

### Boas Práticas

1. **Nunca exponha o WEBHOOK_SECRET**
2. **Use HTTPS em produção**
3. **Configure firewall para limitar acesso**
4. **Monitore logs de acesso**
5. **Rotacione o WEBHOOK_SECRET periodicamente**

---

## 📚 Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [cURL Manual](https://curl.se/docs/manual.html)
- [jq Manual](https://stedolan.github.io/jq/manual/)

---

**🎉 Agora você está pronto para integrar e automatizar seu bot!**
