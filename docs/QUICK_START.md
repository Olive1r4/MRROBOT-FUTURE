# 🚀 Quick Start - Comece em 5 Minutos

Guia rápido para colocar o bot funcionando em modo simulação.

## Pré-requisitos

- Python 3.10+ instalado
- Conta no [Supabase](https://supabase.com) (gratuita)
- Chaves de API da [Binance](https://www.binance.com/en/my/settings/api-management)

---

## Passo 1: Clone e Instale

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/MRROBOT-FUTURE.git
cd MRROBOT-FUTURE

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt
```

---

## Passo 2: Configure o Supabase

1. Acesse [app.supabase.com](https://app.supabase.com)
2. Clique em **"New Project"**
3. Preencha:
   - **Name:** mrrobot-scalping
   - **Database Password:** (escolha uma senha forte)
   - **Region:** Escolha o mais próximo de você
4. Aguarde a criação (1-2 minutos)
5. Vá em **SQL Editor** (menu lateral)
6. Clique em **"New Query"**
7. Copie TODO o conteúdo de `database/supabase_setup.sql`
8. Cole no editor e clique em **"Run"**
9. Verifique se apareceu "Success" ✅

### Obter Credenciais do Supabase

1. Vá em **Settings** > **API**
2. Copie:
   - **Project URL** (ex: https://xxxxx.supabase.co)
   - **anon public** key (a chave longa que começa com "eyJ...")

---

## Passo 3: Configure as Chaves da Binance

1. Acesse [Binance API Management](https://www.binance.com/en/my/settings/api-management)
2. Clique em **"Create API"**
3. Escolha **"System generated"**
4. Preencha o nome: `ScalpingBot`
5. Complete a verificação 2FA
6. **IMPORTANTE:** Configure as permissões:
   - ✅ Enable Reading
   - ✅ Enable Futures
   - ❌ NÃO habilite "Enable Withdrawals"
7. Copie:
   - **API Key**
   - **Secret Key**

⚠️ **NUNCA compartilhe suas chaves!**

---

## Passo 4: Configure o Arquivo .env

```bash
# Copie o template
cp env.template .env

# Edite o arquivo
nano .env  # ou use seu editor preferido
```

**Preencha com suas credenciais:**

```env
# Modo simulação (não executa ordens reais)
MODE=MOCK

# Binance (cole suas chaves aqui)
BINANCE_API_KEY=sua_api_key_aqui
BINANCE_SECRET_KEY=sua_secret_key_aqui
BINANCE_TESTNET=false

# Supabase (cole suas credenciais aqui)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...sua_chave_aqui

# Webhook Secret (gere um token)
# Execute: openssl rand -hex 32
WEBHOOK_SECRET=seu_token_secreto_aqui

# Deixe o resto como está por enquanto
```

**Salvar:** `Ctrl + X`, depois `Y`, depois `Enter`

---

## Passo 5: Execute o Bot

```bash
# Certifique-se de que o ambiente virtual está ativo
source venv/bin/activate

# Execute o bot
python -m src.main
```

**Você deve ver:**

```
============================================
🤖 SCALPING BOT INICIADO
============================================
📊 Modo: MOCK
🎯 Lucro alvo: 0.60%
📈 Timeframe: 5m
🛡️ Stop loss diário: 5.0%
============================================
✅ Conectado ao Supabase
✅ Conectado à Binance Futures (MODO SIMULAÇÃO)
⚠️ Ordens NÃO serão executadas - apenas simuladas!
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Pronto! O bot está rodando!**

---

## Passo 6: Teste o Bot

### Abra outro terminal e teste:

```bash
# 1. Health Check
curl http://localhost:8000/health

# 2. Ver moedas ativas
curl http://localhost:8000/config/coins

# 3. Executar um trade manual de teste
curl -X POST http://localhost:8000/trade/manual \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT"}'

# 4. Ver trades abertos
curl http://localhost:8000/trades/open

# 5. Ver estatísticas
curl http://localhost:8000/stats
```

---

## Passo 7: Monitore os Logs

```bash
# Ver logs em tempo real
tail -f logs/scalping_bot.log
```

Você verá algo como:

```
2024-01-19 10:30:00 - INFO - 🚀 INICIANDO TRADE: BTCUSDT
2024-01-19 10:30:01 - INFO - 📊 Obtendo dados de mercado...
2024-01-19 10:30:02 - INFO - 💰 Preço atual: $42,500.00
2024-01-19 10:30:03 - INFO - 📈 Analisando indicadores técnicos...
2024-01-19 10:30:04 - INFO - ✅ Sinal de entrada CONFIRMADO!
2024-01-19 10:30:05 - INFO - 🎭 MOCK ORDER: BUY 0.0023 BTCUSDT @ 42500.00
2024-01-19 10:30:06 - INFO - ✅ Trade criado com ID: 1
```

---

## Passo 8: Visualize no Supabase

1. Volte ao [Supabase Dashboard](https://app.supabase.com)
2. Vá em **Table Editor**
3. Explore as tabelas:
   - **trades_history:** Veja seus trades
   - **bot_logs:** Veja os logs
   - **daily_pnl:** Veja o PnL diário
   - **coins_config:** Gerencie moedas ativas

---

## 🎯 Próximos Passos

### 1. Ativar/Desativar Moedas

No Supabase, vá em **Table Editor** > **coins_config**:

- ✅ **is_active = true:** Moeda habilitada para trading
- ❌ **is_active = false:** Moeda desabilitada

Ou via API:

```bash
# Ativar/desativar ETHUSDT
curl -X POST http://localhost:8000/config/coins/ETHUSDT/toggle
```

### 2. Ajustar Parâmetros

Edite o `.env` para ajustar:

```env
# Lucro alvo (0.006 = 0.6%)
TARGET_PROFIT=0.008  # Aumentar para 0.8%

# Timeframe
TIMEFRAME=3m  # Mudar para 3 minutos

# Max trades simultâneos
MAX_OPEN_TRADES=3  # Permitir 3 trades ao mesmo tempo
```

**Reinicie o bot após alterar:**

```bash
# Ctrl+C para parar
# Depois execute novamente:
python -m src.main
```

### 3. Integrar com TradingView

Configure um alerta no TradingView:

**Webhook URL:** `http://seu-ip:8000/webhook`

**Message:**
```json
{
  "symbol": "{{ticker}}",
  "action": "buy",
  "price": {{close}}
}
```

**Headers:**
```
x-webhook-secret: seu_token_do_env
```

### 4. Testar por Alguns Dias

- ✅ Deixe rodando em modo MOCK por 3-7 dias
- ✅ Monitore os logs diariamente
- ✅ Verifique se os sinais fazem sentido
- ✅ Ajuste parâmetros conforme necessário

### 5. Só Então Considere Modo PROD

⚠️ **ATENÇÃO:** Modo PROD executa ordens REAIS!

Quando estiver confiante:

1. Mude `MODE=PROD` no `.env`
2. **Comece com valores PEQUENOS**
3. Configure `DEFAULT_POSITION_SIZE=10.00` (apenas $10)
4. Monitore ATIVAMENTE por alguns dias
5. Aumente gradualmente se tudo estiver OK

---

## ❓ Problemas Comuns

### Bot não conecta ao Supabase

- ✅ Verifique se SUPABASE_URL está correto
- ✅ Verifique se SUPABASE_KEY está correto (é a chave "anon public")
- ✅ Teste no navegador: abra a URL do Supabase

### Bot não conecta à Binance

- ✅ Verifique se as API keys estão corretas
- ✅ Verifique se "Enable Futures" está marcado na Binance
- ✅ Verifique se não há espaços extras nas chaves

### "Trade bloqueado" nas mensagens

Isso é normal! O bot tem vários guardrails:

- ❌ Moeda não está ativa no banco
- ❌ Indicadores técnicos não confirmaram entrada
- ❌ Circuit breaker ativo
- ❌ Máximo de trades atingido
- ❌ Cooldown ativo

Verifique os logs para entender o motivo específico.

### Porta 8000 já está em uso

```bash
# Encontre o processo usando a porta
lsof -i :8000

# Mate o processo
kill -9 <PID>

# Ou mude a porta no .env
WEBHOOK_PORT=8001
```

---

## 📚 Documentação Completa

- [README.md](../README.md) - Documentação completa
- [VPS_SETUP.md](VPS_SETUP.md) - Como configurar na VPS
- [Supabase Dashboard](https://app.supabase.com) - Gerenciar banco de dados

---

## 🆘 Precisa de Ajuda?

1. Verifique os logs: `tail -f logs/scalping_bot.log`
2. Consulte o [README.md](../README.md)
3. Abra uma issue no GitHub

---

**🎉 Parabéns! Seu bot está funcionando!**

Agora é só monitorar, ajustar e otimizar. Boa sorte! 🚀📈
