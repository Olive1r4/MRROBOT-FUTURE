# 🚀 Checklist de Migração para Produção (MRROBOT)

Este documento lista todas as verificações e alterações necessárias para migrar o bot do modo Simulação (`MOCK`) para Produção Real (`PROD`) na VPS.

## 1. Alterações no Arquivo `.env` (VPS)

As seguintes variáveis devem ser revisadas e alteradas no arquivo `.env` da VPS:

| Variável                | Valor Atual (VPS) | Ação Necessária         | Observação                                                                                            |
| :---------------------- | :---------------- | :---------------------- | :---------------------------------------------------------------------------------------------------- |
| `MODE`                  | `MOCK`            | **ALTERAR para `PROD`** | Isso ativará a execução real de ordens na Binance.                                                    |
| `BINANCE_API_KEY`       | `sMvDww...`       | **VERIFICAR**           | Confirme se esta API Key tem permissões de "Futures Trading" habilitadas na Binance.                  |
| `BINANCE_SECRET_KEY`    | `R9DXnn...`       | **VERIFICAR**           | Confirme se o Secret corresponde à API Key acima.                                                     |
| `BINANCE_TESTNET`       | `false`           | **MANTER `false`**      | Garante conexão com a Binance Real, não Testnet.                                                      |
| `DEFAULT_POSITION_SIZE` | `100.00`          | **REVISAR**             | O bot tentará abrir ordens de $100 USDT. Garanta que você tenha saldo suficiente (min $200 + margem). |
| `DEFAULT_LEVERAGE`      | `5`               | **REVISAR**             | Alavancagem de 5x. Isso significa que uma ordem de $100 usa ~$20 de margem.                           |
| `DAILY_STOP_LOSS`       | `0.10` (10%)      | **ALTERAR p/ `0.03`**   | **CRÍTICO:** O usuário solicitou voltar para 3% (0.03). Verifique se está correto.                    |
| `TARGET_PROFIT`         | `0.006` (0.6%)    | **VALIDAR**             | Alvo de lucro líquido por trade. Lembre-se das taxas (~0.04% a 0.08%).                                |

## 2. Verificações de Segurança e Saldo

### ✅ Saldo na Binance Futures

- [ ] O saldo em USDT está na carteira de **Futuros (USDⓈ-M)** e não na Spot?
- [ ] O saldo disponível cobre o `DEFAULT_POSITION_SIZE` \* `MAX_OPEN_TRADES`?
  - Exemplo Atual: 2 trades \* $20 margem (5x) = ~$40 livres necessários no mínimo. Recomendado margem de segurança maior.

### ✅ Permissões da API Key

- [ ] A API Key tem a opção **"Enable Futures"** marcada?
- [ ] A restrição de IP está configurada? (Recomendado adicionar o IP da VPS: `49.13.1.177` para segurança).

## 3. Alterações Críticas no Código (OBRIGATÓRIO)

Para que o bot opere com saldo real e respeite a regra de 20% da banca, é **necessário alterar o código** em `src/risk_manager.py`. Atualmente, está configurado com valores fixos para simulação.

### 🚨 `src/risk_manager.py`

**Problema:** O código atual define capital fixo de $100.00 e não consulta a Binance.

**Alteração Necessária:**
Localizar a função `calculate_position_size` (aprox. linha 360) e alterar:

```python
# DE:
total_capital = 100.0

# PARA:
if self.config.MODE == "PROD":
    # Obter saldo da Binance (USDT Livre)
    # Assumindo que risk_manager tem acesso ao exchange_manager
    # Se não tiver, precisará passar o exchange_manager para o risk_manager
    # balance = self.db.get_balance() ... (precisa verificar a arquitetura)
    pass
else:
    total_capital = 100.0
```

> **NOTA TÉCNICA:** O `RiskManager` atualmente não recebe a instância de `ExchangeManager` em seu construtor (`__init__`), apenas `config` e `database`.
> **SOLUÇÃO NECESSÁRIA:**
>
> 1. Alterar `src/main.py` para passar `exchange` ao instanciar `RiskManager`.
> 2. Alterar `src/risk_manager.py` para receber e armazenar `exchange`.
> 3. Implementar a chamada `self.exchange.fetch_balance()['USDT']['free']` no cálculo.

## 4. Limpeza e Preparação (CRÍTICO)

Antes de virar a chave para `PROD`, é **FUDAMENTAL** limpar todos os dados de testes para evitar contaminação das estatísticas e logs.

### 🗑️ Executar Script de Limpeza Total

Criei um script automatizado para isso na raiz do projeto: `reset_database.py`.

**Comando para rodar na VPS:**

```bash
# Navegar para o diretório
cd /root/MRROBOT-FUTURE

# Executar o script de reset (dentro do container ou com python direto se tiver env configurado)
# Recomendado rodar via Docker para garantir acesso às libs:
docker compose run --rm scalping-bot python scripts/reset_database.py
# OU se o arquivo estiver na raiz mapeada:
docker compose run --rm scalping-bot python reset_database.py
```

**O que será apagado:**

- ✅ Tabela `trades_mrrobot` (Histórico de trades)
- ✅ Tabela `logs_mrrobot` (Logs de operação)
- ✅ Tabela `cooldown_mrrobot` (Timers de espera)
- ✅ Tabela `daily_stats_mrrobot` (Estatísticas de PnL diário)
- ✅ View `performance_by_symbol_mrrobot` (Resetada automaticamente)

> **⚠️ Atenção:** Certifique-se de não ter trades REAIS abertos na Binance que não estejam no banco, ou vice-versa. O reset apaga apenas o banco de dados do bot, não fecha posições na Binance.

## 5. Plano de Ação para Virada de Chave (SOFT LAUNCH)

Para garantir segurança total, faremos um "Soft Launch" (Lançamento Suave): iniciar o bot conectado na Binance Real, mas **SEM abrir trades** inicialmente.

### Passo 1: Configuração Inicial Segura

Edite o `.env` na VPS:

```bash
nano .env
```

Altere:

- `MODE=PROD`
- `ENABLE_SCANNER=False` <-- **IMPORTANTE:** Isso impede o bot de abrir novas posições!

### Passo 2: Reinício e Verificação

Reinicie o bot e acompanhe os logs:

```bash
docker compose down
docker compose up -d --build
docker logs -f mrrobot-scalping-bot
```

**O que verificar nos logs:**

1.  ✅ `Conectado à Binance Futures (MODO PRODUÇÃO)` (Sem erros de API Key)
2.  ✅ `Saldo disponível: $XXXX.XX` (Confirme se ele leu o saldo correto da Binance)
3.  ✅ `Trade Monitor WebSocket conectado`
4.  ❌ Garantir que **NÃO** apareça `Market Scanner iniciado`

### Passo 3: Ativação Total

Se tudo estiver correto (saldo lido, conexão OK, sem erros), ative o trading:

1.  Edite o `.env` novamente:

    ```bash
    nano .env
    ```

    - Mude `ENABLE_SCANNER=True`

2.  Reinicie levemente (apenas recriando o container):

    ```bash
    docker compose up -d --force-recreate
    ```

3.  Agora o bot está 100% operacional em Produção! 🚀

## 6. Monitoramento Pós-Ativação

Nas primeiras horas de operação real:

1.  Fique atento aos logs de `✅ Ordem Executada`.
2.  Confira no App da Binance se a ordem abriu corretamente.
3.  Verifique se o Stop Loss e Take Profit foram cadastrados na Binance.

---

**⚠️ AVISO DE RISCO:** O modo `PROD` envolve dinheiro real. Certifique-se de que a estratégia foi validada suficientemente no modo `MOCK` antes de prosseguir.
