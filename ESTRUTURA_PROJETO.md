# 📁 Estrutura do Projeto - MRROBOT-FUTURE

Visão detalhada da organização do projeto e responsabilidades de cada componente.

---

## 🌳 Árvore de Diretórios

```
MRROBOT-FUTURE/
│
├── 📂 .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions - Deploy automatizado
│
├── 📂 database/
│   └── supabase_setup.sql          # Schema completo do banco de dados
│
├── 📂 docs/
│   ├── API_EXAMPLES.md             # Exemplos práticos de uso da API
│   ├── ESTRATEGIAS.md              # Detalhamento das estratégias de trading
│   ├── QUICK_START.md              # Guia rápido de início
│   ├── TESTES.md                   # Guia completo de testes
│   └── VPS_SETUP.md                # Configuração detalhada da VPS
│
├── 📂 logs/                         # Diretório de logs (criado automaticamente)
│   └── scalping_bot.log            # Log principal da aplicação
│
├── 📂 scripts/
│   ├── start_bot.sh                # Script de inicialização com validações
│   └── check_health.sh             # Script de verificação de saúde
│
├── 📂 src/
│   ├── __init__.py                 # Inicialização do pacote
│   ├── main.py                     # 🚀 Aplicação FastAPI principal
│   ├── config.py                   # ⚙️ Configurações e validações
│   ├── database.py                 # 💾 Integração com Supabase
│   ├── exchange_manager.py         # 🔄 Gerenciador de exchange (Mock/Prod)
│   ├── indicators.py               # 📈 Indicadores técnicos
│   └── risk_manager.py             # 🛡️ Guardrails de segurança
│
├── 📂 systemd/
│   └── scalping-bot.service        # Arquivo de serviço systemd
│
├── 📄 .gitignore                    # Arquivos ignorados pelo git
├── 📄 env.template                  # Template de configuração
├── 📄 LICENSE                       # Licença MIT
├── 📄 README.md                     # 📚 Documentação principal
├── 📄 RESUMO_EXECUTIVO.md          # 📊 Resumo executivo do projeto
├── 📄 ESTRUTURA_PROJETO.md         # 📁 Este arquivo
└── 📄 requirements.txt              # Dependências Python
```

---

## 🔍 Detalhamento dos Componentes

### 📂 src/ - Código Fonte Principal

#### 🚀 main.py (596 linhas)
**Responsabilidade:** Aplicação FastAPI e orquestração

**Componentes principais:**
- Inicialização da aplicação FastAPI
- Endpoints da API (webhook, trades, config, stats)
- Função `execute_trade()` - Orquestra todo o fluxo de trading
- Função `monitor_trade()` - Monitora trades abertos em background
- Logging estruturado

**Endpoints:**
```python
GET  /                          # Raiz
GET  /health                    # Health check
POST /webhook                   # Receber sinais
POST /trade/manual              # Trade manual
GET  /trades/open               # Listar trades abertos
GET  /trades/{id}               # Obter trade específico
POST /trades/{id}/close         # Fechar trade
GET  /stats                     # Estatísticas
GET  /config/coins              # Listar moedas
POST /config/coins/{symbol}/toggle  # Ativar/desativar moeda
```

**Fluxo de execução de trade:**
```
1. Validar guardrails de risco
2. Obter dados do mercado (preço, OHLCV)
3. Analisar indicadores técnicos
4. Calcular tamanho da posição
5. Configurar exchange (leverage, margin mode)
6. Executar ordem de entrada
7. Salvar no banco de dados
8. Iniciar monitoramento em background
```

---

#### ⚙️ config.py (189 linhas)
**Responsabilidade:** Configurações e validações

**Classe principal:**
```python
class Config(BaseSettings):
    # Modo de operação
    MODE: str = "MOCK"
    
    # Binance API
    BINANCE_API_KEY: str
    BINANCE_SECRET_KEY: str
    BINANCE_TESTNET: bool = False
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # Webhook
    WEBHOOK_PORT: int = 8000
    WEBHOOK_SECRET: str
    
    # Trading
    TARGET_PROFIT: float = 0.006
    TRADING_FEE: float = 0.0004
    DEFAULT_LEVERAGE: int = 10
    DEFAULT_POSITION_SIZE: float = 100.00
    
    # Indicadores
    RSI_PERIOD: int = 14
    RSI_OVERSOLD: float = 30
    BB_PERIOD: int = 20
    EMA_PERIOD: int = 200
    ATR_PERIOD: int = 14
    TIMEFRAME: str = "5m"
    
    # Guardrails
    DAILY_STOP_LOSS: float = 0.05
    MAX_OPEN_TRADES: int = 2
    TRADE_COOLDOWN_SECONDS: int = 300
    MAX_ORDERS_PER_MINUTE: int = 5
```

**Validadores:**
- Valida MODE (MOCK ou PROD)
- Valida TARGET_PROFIT (0-10%)
- Valida LEVERAGE (1-125)
- Valida RSI_LEVELS (0-100)
- Valida TIMEFRAME (1m, 3m, 5m, etc)
- E mais...

---

#### 💾 database.py (394 linhas)
**Responsabilidade:** Integração com Supabase

**Métodos principais:**

**Coins Config:**
```python
get_coin_config(symbol)          # Obter config de uma moeda
get_active_coins()                # Listar moedas ativas
update_coin_status(symbol, is_active)  # Ativar/desativar
```

**Trades History:**
```python
create_trade(trade_data)          # Criar novo trade
update_trade(trade_id, data)      # Atualizar trade
close_trade(trade_id, exit_price, reason)  # Fechar trade
get_open_trades()                 # Listar trades abertos
get_trade_by_id(trade_id)         # Obter trade específico
get_trades_by_symbol(symbol)      # Trades de uma moeda
```

**Bot Logs:**
```python
log(level, message, details, symbol, trade_id)  # Registrar log
```

**Daily PnL:**
```python
get_daily_pnl(date)               # Obter PnL de um dia
update_daily_pnl(pnl, is_win)     # Atualizar PnL diário
activate_circuit_breaker(date)    # Ativar circuit breaker
```

**Trade Cooldown:**
```python
get_trade_cooldown(symbol)        # Obter cooldown
set_trade_cooldown(symbol, last_time, until)  # Definir cooldown
```

**Estatísticas:**
```python
get_statistics(days)              # Estatísticas dos últimos N dias
```

---

#### 🔄 exchange_manager.py (377 linhas)
**Responsabilidade:** Gerenciamento de exchange (Mock/Prod)

**Classes:**

**MockExecutor:**
```python
create_market_order(symbol, side, amount)  # Simular ordem
create_limit_order(symbol, side, amount, price)
cancel_order(order_id, symbol)
fetch_order(order_id, symbol)
```

**ExchangeManager:**
```python
# Leitura de dados (sempre real)
get_ticker(symbol)                # Obter ticker
get_current_price(symbol)         # Obter preço atual
fetch_ohlcv(symbol, timeframe, limit)  # Obter candles
get_market_info(symbol)           # Informações do mercado
is_market_open(symbol)            # Verificar se mercado está aberto

# Configuração
set_leverage(symbol, leverage)    # Definir alavancagem
set_margin_mode(symbol, mode)     # Definir modo de margem

# Execução (Mock ou Real baseado em MODE)
create_market_buy_order(symbol, amount, price)
create_market_sell_order(symbol, amount, price)
create_limit_order(symbol, side, amount, price)
create_stop_loss_order(symbol, side, amount, stop_price)
cancel_order(order_id, symbol)

# Utilidades
fetch_balance()                   # Obter saldo
get_position(symbol)              # Obter posição aberta
calculate_order_size(symbol, usdt_amount, price)
```

**Diferença Mock vs Prod:**
- **Mock:** Lê dados reais, mas simula execução de ordens
- **Prod:** Lê dados reais e executa ordens reais na Binance

---

#### 📈 indicators.py (336 linhas)
**Responsabilidade:** Cálculo de indicadores técnicos

**Classe TechnicalIndicators:**
```python
calculate_rsi(prices, period=14)
    # Retorna: float (0-100)
    
calculate_bollinger_bands(prices, period=20, std_dev=2.0)
    # Retorna: (upper_band, middle_band, lower_band)
    
calculate_ema(prices, period=200)
    # Retorna: float
    
calculate_atr(ohlcv, period=14)
    # Retorna: float
    
calculate_sma(prices, period=20)
    # Retorna: float
```

**Classe SignalAnalyzer:**
```python
analyze_entry_signal(symbol, ohlcv_data, current_price)
    # Retorna: {
    #   'should_enter': bool,
    #   'reason': str,
    #   'indicators': dict,
    #   'stop_loss': float,
    #   'take_profit': float
    # }

check_exit_conditions(entry_price, current_price, stop_loss, take_profit)
    # Retorna: (should_exit: bool, reason: str)
```

**Lógica de entrada:**
```python
should_enter = (
    current_price < bb_lower AND      # Sobrevenda (Bollinger)
    rsi < RSI_OVERSOLD AND             # Sobrevenda (RSI)
    current_price > ema200             # Tendência de alta (EMA)
)
```

---

#### 🛡️ risk_manager.py (327 linhas)
**Responsabilidade:** Guardrails de segurança

**Métodos de validação:**

```python
check_daily_stop_loss()
    # Verifica se circuit breaker está ativo
    # Retorna: (is_allowed: bool, reason: str)

check_max_open_trades()
    # Verifica se atingiu limite de trades simultâneos
    # Retorna: (is_allowed: bool, reason: str)

check_trade_cooldown(symbol)
    # Verifica se passou o cooldown de 5 minutos
    # Retorna: (is_allowed: bool, reason: str)

check_rate_limit()
    # Verifica se não excedeu 5 ordens/minuto
    # Retorna: (is_allowed: bool, reason: str)

check_symbol_is_active(symbol)
    # Verifica se moeda está ativa no banco
    # Retorna: (is_active: bool, reason: str, config: dict)
```

**Método principal:**
```python
validate_trade_entry(symbol)
    # Executa TODAS as validações
    # Retorna: {
    #   'allowed': bool,
    #   'reasons': list,
    #   'coin_config': dict
    # }
```

**Outros métodos:**
```python
set_trade_cooldown(symbol)        # Define cooldown após fechar trade
register_order()                  # Registra ordem no rate limiter
calculate_position_size(symbol, price, config)  # Calcula tamanho da posição
```

---

### 📂 database/ - Banco de Dados

#### supabase_setup.sql (254 linhas)
**Responsabilidade:** Schema completo do banco

**Tabelas:**

1. **coins_config** - Configuração de moedas
```sql
- id, symbol, is_active, min_pnl, max_position_size, leverage
```

2. **trades_history** - Histórico de trades
```sql
- id, symbol, side, entry_price, exit_price, quantity, leverage
- target_price, stop_loss_price, pnl, pnl_percentage, status
- entry_reason, exit_reason, order_id_entry, order_id_exit
- mode, entry_time, exit_time
```

3. **bot_logs** - Logs do bot
```sql
- id, level, message, details (JSONB), symbol, trade_id
```

4. **daily_pnl** - PnL diário
```sql
- id, trade_date, total_pnl, total_trades
- winning_trades, losing_trades
- is_circuit_breaker_active, circuit_breaker_activated_at
```

5. **trade_cooldown** - Cooldown entre trades
```sql
- id, symbol, last_trade_time, cooldown_until
```

6. **rate_limiter** - Rate limiting (opcional)
```sql
- id, minute_timestamp, request_count
```

**Views:**
- `daily_stats` - Estatísticas diárias com win rate
- `open_trades` - Trades abertos com tempo decorrido
- `performance_by_symbol` - Performance agregada por moeda

**Functions:**
- `update_updated_at_column()` - Atualiza timestamp automaticamente
- `cleanup_old_logs()` - Limpa logs antigos

---

### 📂 scripts/ - Scripts Auxiliares

#### start_bot.sh
**Responsabilidade:** Inicialização com validações

**Fluxo:**
1. Verificar se está no diretório correto
2. Verificar se .env existe (criar se não)
3. Verificar Python instalado
4. Criar/ativar ambiente virtual
5. Instalar/atualizar dependências
6. Criar diretório de logs
7. Validar variáveis de ambiente críticas
8. Exibir configurações atuais
9. Pedir confirmação se MODE=PROD
10. Iniciar bot

#### check_health.sh
**Responsabilidade:** Verificação de saúde

**Verificações:**
1. Serviço systemd está rodando?
2. Porta 8000 está aberta?
3. API responde ao /health?
4. Quantos trades estão abertos?
5. Últimas linhas do log

---

### 📂 docs/ - Documentação

#### README.md (533 linhas)
Documentação principal completa

#### QUICK_START.md
Guia para começar em 5 minutos

#### VPS_SETUP.md
Configuração detalhada da VPS passo a passo

#### ESTRATEGIAS.md
Detalhamento matemático das estratégias

#### TESTES.md
Guia completo de testes (10 testes)

#### API_EXAMPLES.md
Exemplos práticos de uso da API

#### RESUMO_EXECUTIVO.md
Visão geral executiva do projeto

---

### 📂 .github/workflows/ - CI/CD

#### deploy.yml
**Responsabilidade:** Deploy automatizado via GitHub Actions

**Fluxo:**
1. Checkout do código
2. Configurar chave SSH
3. Conectar na VPS via SSH
4. Parar serviço
5. Backup do .env
6. Git pull
7. Restaurar .env
8. Instalar dependências
9. Reiniciar serviço
10. Verificar status
11. Health check

**Secrets necessários:**
- `VPS_SSH_KEY` - Chave privada SSH
- `VPS_HOST` - IP/domínio da VPS
- `VPS_USER` - Usuário SSH
- `VPS_PATH` - Caminho do projeto

---

### 📂 systemd/ - Gerenciamento de Serviço

#### scalping-bot.service
**Responsabilidade:** Configuração do serviço systemd

**Configurações:**
- Inicia automaticamente no boot
- Reinicia automaticamente em caso de falha
- Logs em `/var/log/scalping-bot/`
- Executa como usuário específico
- WorkingDirectory configurado

---

## 🔄 Fluxo de Dados

### 1. Recebimento de Sinal (Webhook)

```
TradingView/Externo
    ↓ POST /webhook
FastAPI (main.py)
    ↓ Validar token
    ↓ Adicionar à fila de background
execute_trade()
```

### 2. Execução de Trade

```
execute_trade()
    ↓
RiskManager.validate_trade_entry()
    ├─ check_symbol_is_active()
    ├─ check_daily_stop_loss()
    ├─ check_max_open_trades()
    ├─ check_trade_cooldown()
    └─ check_rate_limit()
    ↓
ExchangeManager.get_current_price()
ExchangeManager.fetch_ohlcv()
    ↓
SignalAnalyzer.analyze_entry_signal()
    ├─ calculate_rsi()
    ├─ calculate_bollinger_bands()
    ├─ calculate_ema()
    └─ calculate_atr()
    ↓
RiskManager.calculate_position_size()
    ↓
ExchangeManager.set_leverage()
ExchangeManager.set_margin_mode()
ExchangeManager.create_market_buy_order()
    ↓
Database.create_trade()
Database.log()
    ↓
monitor_trade() [background]
```

### 3. Monitoramento de Trade

```
monitor_trade() [loop infinito]
    ↓ A cada 5 segundos
Database.get_trade_by_id()
    ↓
ExchangeManager.get_current_price()
    ↓
SignalAnalyzer.check_exit_conditions()
    ├─ Preço >= Take Profit?
    └─ Preço <= Stop Loss?
    ↓ Se sim
ExchangeManager.create_market_sell_order()
    ↓
Database.close_trade()
Database.update_daily_pnl()
RiskManager.set_trade_cooldown()
Database.log()
```

---

## 📊 Estatísticas do Projeto

### Código Python

- **Total de arquivos:** 7
- **Total de linhas:** ~2.500+
- **Cobertura de testes:** Manual (guia completo em docs/TESTES.md)

### Documentação

- **Arquivos de documentação:** 8
- **Total de linhas:** ~3.000+
- **Idioma:** Português (BR)

### Banco de Dados

- **Tabelas:** 6
- **Views:** 3
- **Functions:** 2
- **Triggers:** 2

---

## 🎯 Pontos de Entrada

### Para Desenvolvedores

1. **Início:** `src/main.py` - Entenda o fluxo principal
2. **Configuração:** `src/config.py` - Veja todas as opções
3. **Estratégia:** `src/indicators.py` - Entenda a lógica de trading
4. **Segurança:** `src/risk_manager.py` - Veja os guardrails

### Para Usuários

1. **Início rápido:** `docs/QUICK_START.md`
2. **Configuração:** `env.template`
3. **Deploy:** `docs/VPS_SETUP.md`
4. **Testes:** `docs/TESTES.md`

### Para Operadores

1. **Monitoramento:** `scripts/check_health.sh`
2. **Logs:** `logs/scalping_bot.log`
3. **API:** `docs/API_EXAMPLES.md`
4. **Dashboard:** Supabase Table Editor

---

## 🔧 Manutenção

### Arquivos que você pode modificar:

✅ `.env` - Suas configurações  
✅ `database/supabase_setup.sql` - Adicionar moedas  
✅ `src/indicators.py` - Ajustar estratégias  
✅ `src/config.py` - Adicionar parâmetros  

### Arquivos que NÃO deve modificar (sem conhecimento):

❌ `src/main.py` - Lógica principal  
❌ `src/database.py` - Integração com banco  
❌ `src/exchange_manager.py` - Integração com exchange  
❌ `src/risk_manager.py` - Guardrails de segurança  

---

## 📚 Próximos Passos

1. Leia o [QUICK_START.md](docs/QUICK_START.md)
2. Configure seu ambiente
3. Execute os testes em [TESTES.md](docs/TESTES.md)
4. Rode em modo MOCK por alguns dias
5. Só então considere modo PROD

---

**🎓 Agora você entende a estrutura completa do projeto!**

**📖 Continue explorando a documentação para se aprofundar.**
