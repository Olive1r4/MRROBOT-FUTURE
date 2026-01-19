# 📱 Configuração de Notificações Telegram

Guia completo para configurar notificações do bot via Telegram.

## 🎯 O que Você Vai Receber

O bot enviará notificações para seu Telegram sobre:

✅ **Inicialização do bot** - Quando o bot inicia  
✅ **Compras executadas** - Com preço, quantidade, indicadores  
✅ **Vendas executadas** - Com lucro/prejuízo e duração  
✅ **Circuit breaker** - Quando o stop loss diário é atingido  
✅ **Erros críticos** - Para você ficar ciente  

---

## 📋 Pré-requisitos

- Conta no Telegram
- 5 minutos para configuração

---

## 🚀 Passo a Passo

### 1️⃣ Criar um Bot no Telegram

1. Abra o Telegram
2. Procure por: **@BotFather**
3. Inicie uma conversa: `/start`
4. Crie um novo bot: `/newbot`
5. Escolha um nome (ex: "Meu Bot de Scalping")
6. Escolha um username (ex: "meu_scalping_bot")

**Você receberá:**
```
Done! Congratulations on your new bot...

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
```

✅ **Copie este token!** Este é o `TELEGRAM_BOT_TOKEN`

---

### 2️⃣ Obter seu Chat ID

#### Opção 1: Usando @userinfobot (Mais Fácil)

1. No Telegram, procure por: **@userinfobot**
2. Inicie uma conversa: `/start`
3. O bot mostrará suas informações
4. Copie o número que aparece em **"Id:"**

Exemplo:
```
Id: 123456789
```

✅ **Este é o seu `TELEGRAM_CHAT_ID`**

#### Opção 2: Usando a API do Telegram

1. Envie uma mensagem para o seu bot (o que você criou no passo 1)
2. Abra no navegador:
```
https://api.telegram.org/bot<SEU_TOKEN>/getUpdates
```

Substitua `<SEU_TOKEN>` pelo token que você copiou.

3. Procure por `"chat":{"id":123456789}`
4. O número após `"id":` é o seu Chat ID

---

### 3️⃣ Configurar no Bot

Edite o arquivo `.env`:

```bash
nano .env
```

Adicione ou descomente as linhas:

```env
# Notificações Telegram
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
TELEGRAM_CHAT_ID=123456789
```

**Salvar:** `Ctrl + X`, `Y`, `Enter`

---

### 4️⃣ Testar

Reinicie o bot:

```bash
# Local
python -m src.main

# Docker
docker-compose restart
```

**Você deve receber uma mensagem no Telegram:**

```
🤖 BOT DE SCALPING INICIADO

🎭 Modo: SIMULAÇÃO
🎯 Lucro alvo: 0.60%
📈 Timeframe: 5m
🛡️ Stop loss diário: 5.0%
🔢 Max trades: 2
⚡ Alavancagem: 10x

🎭 Ordens serão SIMULADAS

⏰ 19/01/2024 15:30:00
```

✅ **Funcionou!** Agora você receberá todas as notificações!

---

## 📊 Exemplos de Notificações

### Compra Executada

```
🎭 COMPRA EXECUTADA

💎 Moeda: BTCUSDT
💰 Preço entrada: $42,350.0000
📊 Quantidade: 0.0236
⚡ Alavancagem: 10x
💵 Valor posição: $10,000.00

🎯 Take Profit: $42,638.0000 (+0.68%)
🛑 Stop Loss: $42,080.0000 (-0.64%)

📈 Indicadores:
  • RSI: 28.5
  • Preço: $42,350.0000

🎭 Ordem SIMULADA

⏰ 19/01/2024 15:35:00
```

### Venda com Lucro

```
✅ VENDA EXECUTADA - LUCRO

💎 Moeda: BTCUSDT
💰 Preço entrada: $42,350.0000
💰 Preço saída: $42,638.0000
📊 Quantidade: 0.0236
⚡ Alavancagem: 10x
💵 Valor posição: $10,000.00

✅ Resultado:
  • PnL: $6.80
  • PnL %: +0.68%
  • Duração: 12 min

🎭 Ordem SIMULADA

⏰ 19/01/2024 15:47:00
```

### Venda com Prejuízo

```
❌ VENDA EXECUTADA - PREJUÍZO

💎 Moeda: ETHUSDT
💰 Preço entrada: $2,250.0000
💰 Preço saída: $2,235.0000
📊 Quantidade: 0.444
⚡ Alavancagem: 10x
💵 Valor posição: $10,000.00

❌ Resultado:
  • PnL: -$6.66
  • PnL %: -0.67%
  • Duração: 8 min

🎭 Ordem SIMULADA

⏰ 19/01/2024 16:15:00
```

### Circuit Breaker

```
🔴 CIRCUIT BREAKER ATIVADO!

⚠️ O limite de perda diária foi atingido!

📉 PnL do dia: -$50.00
🛑 Limite: $50.00

🚫 Trading bloqueado até amanhã!

⏰ 19/01/2024 18:00:00
```

---

## ⚙️ Configurações Avançadas

### Desabilitar Notificações Temporariamente

Remova ou comente as linhas no `.env`:

```env
# TELEGRAM_BOT_TOKEN=
# TELEGRAM_CHAT_ID=
```

### Notificações para Grupo

1. Crie um grupo no Telegram
2. Adicione o bot ao grupo
3. Obtenha o Chat ID do grupo (geralmente negativo, ex: -123456789)
4. Use este Chat ID no `.env`

### Múltiplos Destinatários

Para enviar para múltiplas pessoas, crie um grupo e adicione todos.

---

## 🔐 Segurança

### ⚠️ Importante

- **Nunca compartilhe** seu `TELEGRAM_BOT_TOKEN`
- **Não commite** o arquivo `.env` no git
- **Use apenas** com pessoas de confiança se for grupo

### Dicas

✅ Use um bot exclusivo para o scalping bot  
✅ Mantenha o token seguro  
✅ Restrinja acesso ao grupo (se usar)  
✅ Monitore quem tem acesso  

---

## 🐛 Troubleshooting

### Não recebo notificações

**Verificar configuração:**

```bash
# Ver valores configurados
cat .env | grep TELEGRAM
```

**Testar manualmente:**

```bash
# Substituir valores
TOKEN="seu_token_aqui"
CHAT_ID="seu_chat_id_aqui"
TEXT="Teste do bot"

curl -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\":\"${CHAT_ID}\",\"text\":\"${TEXT}\"}"
```

**Se retornar erro:**
- Verifique se o token está correto
- Verifique se o chat_id está correto
- Certifique-se de que iniciou conversa com o bot

### Erro: "Chat not found"

- Você precisa iniciar uma conversa com o bot primeiro
- Envie `/start` para o bot no Telegram

### Erro: "Unauthorized"

- Token inválido
- Verifique se copiou o token completo do BotFather

### Notificações atrasadas

- Normal em modo MOCK (não há urgência)
- Em PROD, as notificações são quase instantâneas

---

## 📱 Recursos do Telegram

### Comandos Futuros (Para Implementar)

Você pode adicionar comandos ao bot:

- `/status` - Ver status do bot
- `/stats` - Ver estatísticas
- `/pause` - Pausar trading
- `/resume` - Resumir trading
- `/help` - Ajuda

**Para implementar:** Veja documentação da [python-telegram-bot](https://python-telegram-bot.org/)

---

## 🎓 Resumo Rápido

```bash
# 1. Criar bot
# Telegram > @BotFather > /newbot
# Copiar TOKEN

# 2. Obter Chat ID
# Telegram > @userinfobot > /start
# Copiar ID

# 3. Configurar
nano .env

# Adicionar:
TELEGRAM_BOT_TOKEN=seu_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui

# 4. Reiniciar bot
docker-compose restart

# 5. Testar
# Você deve receber mensagem de inicialização
```

---

## ✅ Checklist

- [ ] Bot criado no @BotFather
- [ ] Token copiado
- [ ] Chat ID obtido
- [ ] Valores configurados no .env
- [ ] Bot reiniciado
- [ ] Mensagem de inicialização recebida
- [ ] Testado com trade manual

---

## 📚 Referências

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [BotFather Documentation](https://core.telegram.org/bots#botfather)
- [python-telegram-bot](https://python-telegram-bot.org/)

---

**🎉 Pronto! Agora você receberá todas as notificações do bot!**

**📱 Fique sempre informado sobre suas operações! 🚀**
