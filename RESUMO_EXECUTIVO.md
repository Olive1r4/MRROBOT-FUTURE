# 📊 RESUMO EXECUTIVO - Bot de Scalping Binance Futures

## 🎯 Visão Geral

Bot profissional de trading automatizado para Binance Futures, especializado em estratégia de **Scalping Long** com análise técnica avançada e múltiplos guardrails de segurança.

---

## ✨ Características Principais

### 🎲 Estratégia de Trading

- **Tipo:** Scalping Long (compra para venda rápida)
- **Lucro alvo:** 0.6% por trade (configurável)
- **Timeframe:** 5 minutos (configurável: 1m, 3m, 5m, 15m, 30m)
- **Alavancagem:** 10x (configurável: 1-125x)

### 📈 Indicadores Técnicos

1. **RSI (14)** - Identifica sobrevenda/sobrecompra
2. **Bandas de Bollinger (20, 2.0)** - Detecta volatilidade
3. **EMA 200** - Filtro de tendência
4. **ATR (14)** - Stop loss dinâmico baseado em volatilidade

### 🛡️ Guardrails de Segurança

1. **Daily Stop Loss (Circuit Breaker)** - Para o bot se perda diária atingir 5%
2. **Max Open Trades** - Limita a 2 trades simultâneos
3. **Anti-Whipsaw (Cooldown)** - 5 minutos entre trades da mesma moeda
4. **Rate Limiter** - Máximo 5 ordens por minuto
5. **Validação de Moedas** - Sistema de whitelist no banco de dados

### 🔄 Modos de Operação

- **MOCK:** Simulação completa (lê dados reais, NÃO executa ordens)
- **PROD:** Produção real (executa ordens na Binance)

---

## 🏗️ Arquitetura Técnica

### Stack Tecnológico

- **Backend:** Python 3.10+ com FastAPI
- **Exchange:** CCXT (suporta 100+ exchanges)
- **Banco de Dados:** Supabase (PostgreSQL)
- **Deploy:** GitHub Actions + SSH
- **Gerenciamento:** Systemd
- **Monitoramento:** Logs estruturados + Dashboard Supabase

### Estrutura do Projeto

```
MRROBOT-FUTURE/
├── src/
│   ├── main.py              # Aplicação FastAPI
│   ├── config.py            # Configurações e validações
│   ├── database.py          # Integração Supabase
│   ├── exchange_manager.py  # Gerenciador de exchange (Mock/Prod)
│   ├── indicators.py        # Indicadores técnicos
│   └── risk_manager.py      # Guardrails de segurança
├── database/
│   └── supabase_setup.sql   # Schema do banco de dados
├── docs/
│   ├── VPS_SETUP.md         # Guia de configuração da VPS
│   ├── QUICK_START.md       # Início rápido
│   ├── ESTRATEGIAS.md       # Detalhes das estratégias
│   ├── TESTES.md            # Guia de testes
│   └── API_EXAMPLES.md      # Exemplos de uso da API
├── scripts/
│   ├── start_bot.sh         # Script de inicialização
│   └── check_health.sh      # Script de verificação
├── systemd/
│   └── scalping-bot.service # Serviço systemd
├── .github/workflows/
│   └── deploy.yml           # Deploy automatizado
├── env.template             # Template de configuração
├── requirements.txt         # Dependências Python
└── README.md                # Documentação principal
```

---

## 📊 Lógica de Entrada

O bot só abre posição quando **TODAS** as condições são satisfeitas:

### Condições Técnicas
```
✅ Preço atual < Banda Inferior de Bollinger (sobrevenda)
✅ RSI < 30 (sobrevenda)
✅ Preço atual > EMA 200 (tendência de alta)
```

### Condições de Risco
```
✅ Moeda está ativa no banco de dados
✅ Circuit breaker NÃO está ativo
✅ Número de trades abertos < limite (2)
✅ Cooldown expirado (5 min desde último trade)
✅ Rate limit OK (< 5 ordens/min)
```

---

## 💰 Gestão de Risco

### Cálculo de Preços

**Take Profit:**
```
TP = Preço Entrada × (1 + 0.006 + 0.0008)
TP = Preço Entrada × 1.0068
```

**Stop Loss Dinâmico:**
```
SL = Preço Entrada - (ATR × 1.5)
```

### Exemplo Prático

**Entrada:** $42,350.00
- **Take Profit:** $42,638.00 (+0.68%)
- **Stop Loss:** $42,080.00 (-0.64%)
- **Risk/Reward:** 1:1.06

### Expectativa Matemática

Com **win rate de 55%**:
```
Expectativa = (0.55 × 0.68%) - (0.45 × 0.64%) = +0.086% por trade
```

Com **20 trades/dia**:
```
0.086% × 20 = 1.72% ao dia
```

**Importante:** Estes são valores teóricos. Performance real varia.

---

## 🚀 Instalação Rápida

### 1. Pré-requisitos

- Python 3.10+
- Conta Binance com API (Futures habilitado)
- Conta Supabase (gratuita)
- VPS Linux (opcional, para produção)

### 2. Instalação Local

```bash
# Clone
git clone https://github.com/seu-usuario/MRROBOT-FUTURE.git
cd MRROBOT-FUTURE

# Ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Dependências
pip install -r requirements.txt

# Configuração
cp env.template .env
nano .env  # Preencha suas credenciais

# Banco de dados
# Execute database/supabase_setup.sql no Supabase

# Iniciar
python -m src.main
```

### 3. Deploy em VPS

Veja guia completo: [docs/VPS_SETUP.md](docs/VPS_SETUP.md)

**Resumo:**
```bash
# Na VPS
git clone https://github.com/seu-usuario/MRROBOT-FUTURE.git
cd MRROBOT-FUTURE
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp env.template .env
nano .env

# Systemd
sudo cp systemd/scalping-bot.service /etc/systemd/system/
sudo systemctl enable scalping-bot
sudo systemctl start scalping-bot
```

---

## 📡 API Endpoints

### Monitoramento

- `GET /health` - Status do bot
- `GET /stats?days=30` - Estatísticas de performance

### Trading

- `POST /webhook` - Receber sinais (TradingView, etc)
- `POST /trade/manual` - Executar trade manual
- `GET /trades/open` - Listar trades abertos
- `GET /trades/{id}` - Detalhes de um trade
- `POST /trades/{id}/close` - Fechar trade manualmente

### Configuração

- `GET /config/coins` - Listar moedas configuradas
- `POST /config/coins/{symbol}/toggle` - Ativar/desativar moeda

Veja exemplos completos: [docs/API_EXAMPLES.md](docs/API_EXAMPLES.md)

---

## 🔐 Segurança

### Implementado

✅ Credenciais em variáveis de ambiente  
✅ Token secreto para webhook  
✅ `.gitignore` configurado  
✅ Modo Mock para testes  
✅ Múltiplos guardrails  
✅ Rate limiting  
✅ Circuit breaker automático  

### Recomendações

- Use HTTPS em produção
- Configure firewall (UFW)
- Use autenticação SSH por chave
- API Keys com permissões mínimas
- Backup automático do banco
- Monitore logs regularmente

---

## 📊 Banco de Dados (Supabase)

### Tabelas Principais

1. **coins_config** - Configuração de moedas
2. **trades_history** - Histórico de trades
3. **bot_logs** - Logs do bot
4. **daily_pnl** - PnL diário (circuit breaker)
5. **trade_cooldown** - Cooldown entre trades
6. **rate_limiter** - Controle de rate limiting

### Views

- **daily_stats** - Estatísticas diárias
- **open_trades** - Trades abertos
- **performance_by_symbol** - Performance por moeda

---

## 🧪 Testes

Antes de usar em produção, execute:

1. ✅ Teste de conexões (Supabase + Binance)
2. ✅ Teste de guardrails (todos os 5)
3. ✅ Teste de indicadores técnicos
4. ✅ Teste de execução (modo MOCK)
5. ✅ Teste de monitoramento
6. ✅ Teste de circuit breaker
7. ✅ Teste de rate limiting
8. ✅ Teste de webhook
9. ✅ Teste de estresse
10. ✅ Validação final

Guia completo: [docs/TESTES.md](docs/TESTES.md)

---

## 📈 Roadmap de Produção

### Fase 1: Simulação (3-7 dias)
```
MODE=MOCK
Monitorar performance
Ajustar parâmetros
```

### Fase 2: Produção Mínima (7-14 dias)
```
MODE=PROD
DEFAULT_POSITION_SIZE=10.00  # $10
DEFAULT_LEVERAGE=5
MAX_OPEN_TRADES=1
```

### Fase 3: Produção Gradual (14-30 dias)
```
DEFAULT_POSITION_SIZE=50.00  # $50
DEFAULT_LEVERAGE=10
MAX_OPEN_TRADES=2
```

### Fase 4: Produção Normal (após 30 dias)
```
DEFAULT_POSITION_SIZE=100.00  # $100
DEFAULT_LEVERAGE=10
MAX_OPEN_TRADES=2
```

---

## ⚠️ Limitações e Riscos

### Limitações Conhecidas

- Funciona melhor em tendências claras (não em mercados laterais)
- Não considera eventos fundamentais (notícias)
- Pode ter dificuldade em moedas de baixa liquidez
- Não considera slippage em simulação
- Fees altas podem consumir lucro em trades muito rápidos

### Riscos

⚠️ **ATENÇÃO:** Trading de criptomoedas envolve risco significativo de perda.

- ❌ Você pode perder TODO o capital investido
- ❌ Alavancagem amplifica perdas
- ❌ Mercado 24/7 pode gerar perdas enquanto você dorme
- ❌ Bugs no código podem causar perdas
- ❌ Problemas de conexão podem impedir fechamento de trades

### Recomendações

✅ SEMPRE teste em modo MOCK primeiro  
✅ SEMPRE comece com valores pequenos  
✅ NUNCA invista mais do que pode perder  
✅ SEMPRE monitore o bot ativamente  
✅ SEMPRE tenha um plano de saída  

---

## 📚 Documentação Completa

- **[README.md](README.md)** - Documentação principal
- **[QUICK_START.md](docs/QUICK_START.md)** - Comece em 5 minutos
- **[VPS_SETUP.md](docs/VPS_SETUP.md)** - Configuração da VPS
- **[ESTRATEGIAS.md](docs/ESTRATEGIAS.md)** - Detalhes das estratégias
- **[TESTES.md](docs/TESTES.md)** - Guia de testes
- **[API_EXAMPLES.md](docs/API_EXAMPLES.md)** - Exemplos de API

---

## 💡 Melhorias Futuras

- [ ] Suporte a Shorts (venda a descoberto)
- [ ] Machine Learning para otimização
- [ ] Dashboard web em tempo real
- [ ] Notificações Telegram/Discord
- [ ] Backtesting integrado
- [ ] Suporte a múltiplas exchanges
- [ ] Trailing stop loss
- [ ] Volume profile
- [ ] Múltiplos timeframes

---

## 📞 Suporte

- **Documentação:** Veja os arquivos em `/docs`
- **Issues:** Abra uma issue no GitHub
- **Logs:** `tail -f logs/scalping_bot.log`

---

## 📄 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.

**DISCLAIMER:** Este software é fornecido "como está", sem garantias. Use por sua conta e risco.

---

## 🎓 Conclusão

Este bot foi desenvolvido seguindo as melhores práticas de:

✅ **Engenharia de Software** - Código limpo, modular e testável  
✅ **DevOps** - Deploy automatizado, monitoramento, logs  
✅ **Segurança** - Múltiplos guardrails, validações, proteções  
✅ **Trading Quantitativo** - Indicadores técnicos, gestão de risco  

**Está pronto para uso, mas lembre-se:**

> "Nenhum sistema de trading é 100% eficaz. Sempre teste extensivamente antes de usar capital real."

---

**🤖 Desenvolvido com ❤️ para a comunidade de trading quantitativo**

**📈 Happy Trading! 🚀**

---

## 📊 Checklist Final

Antes de colocar em produção:

- [ ] Todas as dependências instaladas
- [ ] Arquivo .env configurado corretamente
- [ ] Banco de dados Supabase criado e populado
- [ ] API Keys da Binance configuradas (Futures habilitado)
- [ ] Testado em modo MOCK por pelo menos 3 dias
- [ ] Todos os guardrails testados e funcionando
- [ ] Logs sendo gerados corretamente
- [ ] Monitoramento configurado
- [ ] Backup configurado
- [ ] Firewall configurado (se em VPS)
- [ ] Plano de ação para emergências definido
- [ ] Capital de teste separado (não use dinheiro que não pode perder)

**Só marque todos os itens se REALMENTE estiver pronto! ✅**
