# 🚀 Guia Completo de Configuração da VPS

Este guia detalha passo a passo como configurar sua VPS para rodar o Bot de Scalping.

## 📋 Requisitos

- VPS com Ubuntu 20.04+ (recomendado: 2GB RAM, 2 vCPU)
- Acesso root ou sudo
- IP público ou domínio
- Porta 8000 disponível

---

## 1️⃣ Conexão Inicial com a VPS

```bash
# Conecte-se via SSH
ssh root@seu_ip_da_vps

# ou se você já tem um usuário
ssh seu_usuario@seu_ip_da_vps
```

---

## 2️⃣ Atualização do Sistema

```bash
# Atualizar lista de pacotes
sudo apt update

# Atualizar pacotes instalados
sudo apt upgrade -y

# Instalar pacotes essenciais
sudo apt install -y git curl wget build-essential libssl-dev libffi-dev python3-dev
```

---

## 3️⃣ Instalação do Python 3.10+

```bash
# Verificar versão do Python
python3 --version

# Se a versão for menor que 3.10, instalar:
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-dev

# Verificar instalação
python3.10 --version
```

---

## 4️⃣ Configuração do Usuário (Opcional mas Recomendado)

```bash
# Criar usuário dedicado para o bot
sudo adduser ubuntu

# Adicionar ao grupo sudo
sudo usermod -aG sudo ubuntu

# Trocar para o novo usuário
su - ubuntu
```

---

## 5️⃣ Clonar o Repositório

```bash
# Navegar para o diretório home
cd ~

# Clonar o repositório (substitua pela URL do seu repositório)
git clone https://github.com/seu-usuario/MRROBOT-FUTURE.git

# Entrar no diretório
cd MRROBOT-FUTURE
```

---

## 6️⃣ Configurar Ambiente Virtual Python

```bash
# Criar ambiente virtual
python3.10 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

---

## 7️⃣ Configurar Variáveis de Ambiente

```bash
# Copiar template de configuração
cp env.template .env

# Editar arquivo .env
nano .env
```

**Configure as seguintes variáveis:**

```bash
# Modo de operação (MOCK para testes, PROD para real)
MODE=MOCK

# Binance API (obtenha em https://www.binance.com/en/my/settings/api-management)
BINANCE_API_KEY=sua_chave_aqui
BINANCE_SECRET_KEY=sua_secret_aqui

# Supabase (obtenha em https://app.supabase.com/project/_/settings/api)
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_anon_aqui

# Webhook Secret (gere com: openssl rand -hex 32)
WEBHOOK_SECRET=seu_token_secreto_aqui
```

**Salvar e sair:** `Ctrl + X`, depois `Y`, depois `Enter`

---

## 8️⃣ Configurar o Supabase

1. Acesse o [Supabase Dashboard](https://app.supabase.com)
2. Crie um novo projeto
3. Vá em **SQL Editor**
4. Copie todo o conteúdo do arquivo `database/supabase_setup.sql`
5. Cole no SQL Editor e execute (botão Run)
6. Verifique se as tabelas foram criadas em **Table Editor**

---

## 9️⃣ Testar a Aplicação

```bash
# Ativar ambiente virtual (se não estiver ativo)
source venv/bin/activate

# Rodar a aplicação
python -m src.main
```

**Você deve ver:**
```
🤖 SCALPING BOT INICIADO
📊 Modo: MOCK
✅ Conectado ao Supabase
✅ Conectado à Binance Futures (MODO SIMULAÇÃO)
INFO: Started server process
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Teste em outro terminal:**
```bash
curl http://localhost:8000/health
```

**Parar a aplicação:** `Ctrl + C`

---

## 🔟 Configurar Systemd Service

```bash
# Criar diretório de logs
sudo mkdir -p /var/log/scalping-bot
sudo chown $USER:$USER /var/log/scalping-bot

# Copiar arquivo de serviço
sudo cp systemd/scalping-bot.service /etc/systemd/system/

# IMPORTANTE: Editar o arquivo para ajustar o caminho e usuário
sudo nano /etc/systemd/system/scalping-bot.service
```

**Ajuste as seguintes linhas:**
```ini
User=seu_usuario_aqui
Group=seu_usuario_aqui
WorkingDirectory=/caminho/completo/para/MRROBOT-FUTURE
Environment="PATH=/caminho/completo/para/MRROBOT-FUTURE/venv/bin"
ExecStart=/caminho/completo/para/MRROBOT-FUTURE/venv/bin/python -m src.main
```

**Exemplo:**
```ini
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/MRROBOT-FUTURE
Environment="PATH=/home/ubuntu/MRROBOT-FUTURE/venv/bin"
ExecStart=/home/ubuntu/MRROBOT-FUTURE/venv/bin/python -m src.main
```

**Salvar e sair:** `Ctrl + X`, depois `Y`, depois `Enter`

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar serviço para iniciar no boot
sudo systemctl enable scalping-bot

# Iniciar serviço
sudo systemctl start scalping-bot

# Verificar status
sudo systemctl status scalping-bot
```

---

## 1️⃣1️⃣ Configurar Firewall

```bash
# Verificar se UFW está instalado
sudo apt install -y ufw

# Permitir SSH (IMPORTANTE - não bloqueie o SSH!)
sudo ufw allow 22/tcp

# Permitir porta do webhook
sudo ufw allow 8000/tcp

# Habilitar firewall
sudo ufw enable

# Verificar status
sudo ufw status
```

**Saída esperada:**
```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
8000/tcp                   ALLOW       Anywhere
```

---

## 1️⃣2️⃣ Configurar Nginx como Reverse Proxy (Opcional)

Se você quiser usar um domínio e HTTPS:

```bash
# Instalar Nginx
sudo apt install -y nginx

# Criar configuração
sudo nano /etc/nginx/sites-available/scalping-bot
```

**Conteúdo do arquivo:**
```nginx
server {
    listen 80;
    server_name seu.dominio.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Ativar configuração:**
```bash
sudo ln -s /etc/nginx/sites-available/scalping-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Instalar SSL com Let's Encrypt:**
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d seu.dominio.com
```

---

## 1️⃣3️⃣ Configurar Deploy Automático via GitHub Actions

### Na VPS:

```bash
# Gerar chave SSH para o GitHub Actions
ssh-keygen -t rsa -b 4096 -C "github-actions" -f ~/.ssh/github_actions_rsa

# Adicionar chave pública ao authorized_keys
cat ~/.ssh/github_actions_rsa.pub >> ~/.ssh/authorized_keys

# Exibir chave PRIVADA (para copiar)
cat ~/.ssh/github_actions_rsa
```

**Copie TODA a saída, incluindo:**
```
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

### No GitHub:

1. Vá ao seu repositório no GitHub
2. **Settings** > **Secrets and variables** > **Actions**
3. Clique em **New repository secret**
4. Adicione os seguintes secrets:

| Nome | Valor | Exemplo |
|------|-------|---------|
| `VPS_SSH_KEY` | Chave privada SSH (copiada acima) | -----BEGIN OPENSSH... |
| `VPS_HOST` | IP ou domínio da VPS | 192.168.1.100 |
| `VPS_USER` | Usuário da VPS | ubuntu |
| `VPS_PATH` | Caminho do projeto na VPS | /home/ubuntu/MRROBOT-FUTURE |

### Configurar sudo sem senha para systemctl:

```bash
sudo visudo
```

**Adicione ao final do arquivo:**
```
ubuntu ALL=(ALL) NOPASSWD: /bin/systemctl start scalping-bot, /bin/systemctl stop scalping-bot, /bin/systemctl restart scalping-bot, /bin/systemctl status scalping-bot
```

**Substitua `ubuntu` pelo seu usuário**

---

## 1️⃣4️⃣ Comandos Úteis

### Gerenciar serviço:
```bash
# Ver status
sudo systemctl status scalping-bot

# Iniciar
sudo systemctl start scalping-bot

# Parar
sudo systemctl stop scalping-bot

# Reiniciar
sudo systemctl restart scalping-bot

# Ver logs em tempo real
sudo journalctl -u scalping-bot -f

# Ver últimas 100 linhas de log
sudo journalctl -u scalping-bot -n 100
```

### Monitorar aplicação:
```bash
# Ver logs da aplicação
tail -f logs/scalping_bot.log

# Ver logs do sistema
tail -f /var/log/scalping-bot/output.log
tail -f /var/log/scalping-bot/error.log

# Verificar saúde da API
curl http://localhost:8000/health

# Ver trades abertos
curl http://localhost:8000/trades/open

# Ver estatísticas
curl http://localhost:8000/stats
```

### Atualizar código manualmente:
```bash
cd ~/MRROBOT-FUTURE
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart scalping-bot
```

---

## 1️⃣5️⃣ Monitoramento e Manutenção

### Configurar rotação de logs:

```bash
sudo nano /etc/logrotate.d/scalping-bot
```

**Conteúdo:**
```
/var/log/scalping-bot/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 ubuntu ubuntu
    sharedscripts
    postrotate
        systemctl reload scalping-bot > /dev/null 2>&1 || true
    endscript
}
```

### Criar script de backup:

```bash
nano ~/backup_bot.sh
```

**Conteúdo:**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=~/backups
mkdir -p $BACKUP_DIR

# Backup do .env
cp ~/MRROBOT-FUTURE/.env $BACKUP_DIR/.env_$DATE

# Backup dos logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz ~/MRROBOT-FUTURE/logs

# Manter apenas últimos 7 backups
ls -t $BACKUP_DIR/.env_* | tail -n +8 | xargs rm -f
ls -t $BACKUP_DIR/logs_* | tail -n +8 | xargs rm -f

echo "Backup concluído: $DATE"
```

```bash
chmod +x ~/backup_bot.sh
```

**Adicionar ao cron para rodar diariamente:**
```bash
crontab -e
```

**Adicionar linha:**
```
0 2 * * * /home/ubuntu/backup_bot.sh >> /home/ubuntu/backup.log 2>&1
```

---

## ⚠️ Checklist de Segurança

- [ ] Troque a senha do usuário root
- [ ] Configure autenticação SSH com chave (desabilite senha)
- [ ] Configure firewall (UFW)
- [ ] Mantenha o sistema atualizado (`sudo apt update && sudo apt upgrade`)
- [ ] Use HTTPS se expor a API publicamente
- [ ] Configure backup automático
- [ ] Monitore logs regularmente
- [ ] Use um token forte para WEBHOOK_SECRET
- [ ] Nunca commite o arquivo .env
- [ ] Configure notificações (Telegram/Discord) para alertas

---

## 🆘 Troubleshooting

### Bot não inicia:
```bash
# Ver logs detalhados
sudo journalctl -u scalping-bot -n 100 --no-pager

# Verificar arquivo .env
cat .env

# Testar manualmente
source venv/bin/activate
python -m src.main
```

### Erro de conexão com Supabase:
```bash
# Verificar se SUPABASE_URL e SUPABASE_KEY estão corretos
# Testar conexão
curl -I https://seu-projeto.supabase.co
```

### Erro de API da Binance:
```bash
# Verificar se chaves estão corretas
# Verificar se IP da VPS está na whitelist da Binance
# Testar em modo MOCK primeiro
```

### Deploy do GitHub Actions falha:
```bash
# Verificar se chave SSH está configurada corretamente
# Testar conexão SSH manualmente:
ssh -i ~/.ssh/github_actions_rsa ubuntu@seu_ip

# Verificar secrets no GitHub
```

---

## 📞 Suporte

Se você encontrar problemas:

1. Verifique os logs: `sudo journalctl -u scalping-bot -f`
2. Consulte a seção de Troubleshooting acima
3. Abra uma issue no GitHub

---

## ✅ Próximos Passos

Após configurar tudo:

1. ✅ Teste em modo MOCK primeiro
2. ✅ Monitore os logs por alguns dias
3. ✅ Ajuste os parâmetros conforme necessário
4. ✅ Só então mude para modo PROD
5. ✅ Comece com valores pequenos
6. ✅ Configure alertas/notificações

---

**Boa sorte com seu bot de scalping! 🚀📈**
