# 📱 Telegram - Configuração Rápida

## ⚡ 3 Passos para Configurar

### 1️⃣ Criar Bot (2 minutos)

No Telegram, procure: **@BotFather**

```
/start
/newbot
Nome: Meu Bot Scalping
Username: meu_scalping_bot
```

✅ **Copie o TOKEN que aparece**

---

### 2️⃣ Obter Chat ID (1 minuto)

No Telegram, procure: **@userinfobot**

```
/start
```

✅ **Copie o ID que aparece**

---

### 3️⃣ Configurar no Bot (1 minuto)

```bash
nano .env
```

Adicione:

```env
TELEGRAM_BOT_TOKEN=seu_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
```

**Salvar:** `Ctrl + X`, `Y`, `Enter`

---

## ✅ Testar

```bash
# Reinicie o bot
docker-compose restart

# ou
python -m src.main
```

**Você deve receber no Telegram:**

```
🤖 BOT DE SCALPING INICIADO

🎭 Modo: SIMULAÇÃO
🎯 Lucro alvo: 0.60%
...
```

---

## 📊 Notificações que Você Receberá

✅ **Inicialização** - Quando bot liga  
✅ **Compras** - Com preço, quantidade, indicadores  
✅ **Vendas** - Com lucro/prejuízo e duração  
✅ **Circuit Breaker** - Quando stop diário ativa  

---

## 📚 Guia Completo

Veja: [docs/TELEGRAM_SETUP.md](docs/TELEGRAM_SETUP.md)

---

**🎉 Pronto em 3 passos! Receba todas as notificações! 📱**
