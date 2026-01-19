# 🐳 Guia Completo de Deploy com Docker

Este guia detalha como executar o Bot de Scalping usando Docker e Docker Compose.

## 📋 Índice

- [Vantagens do Docker](#-vantagens-do-docker)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação Rápida](#-instalação-rápida)
- [Configuração](#️-configuração)
- [Deploy](#-deploy)
- [Gerenciamento](#-gerenciamento)
- [Monitoramento](#-monitoramento)
- [Troubleshooting](#-troubleshooting)
- [GitHub Actions com Docker](#-github-actions-com-docker)

---

## 🎯 Vantagens do Docker

### Por que usar Docker?

✅ **Portabilidade** - Funciona em qualquer servidor com Docker  
✅ **Isolamento** - Não interfere com outros serviços  
✅ **Consistência** - Mesmo ambiente em dev e produção  
✅ **Facilidade** - Deploy em segundos  
✅ **Segurança** - Container isolado e restrito  
✅ **Recursos** - Controle de CPU e memória  
✅ **Logs** - Centralizados e rotacionados  
✅ **Updates** - Rebuild e restart rápidos  

---

## 📦 Pré-requisitos

### 1. Docker

**Ubuntu/Debian:**
```bash
# Atualizar sistema
sudo apt update

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Relogar ou executar
newgrp docker

# Verificar instalação
docker --version
```

**CentOS/RHEL:**
```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
```

**Verificar:**
```bash
docker run hello-world
```

### 2. Docker Compose

```bash
# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Dar permissão
sudo chmod +x /usr/local/bin/docker-compose

# Verificar
docker-compose --version
```

---

## 🚀 Instalação Rápida

### Método 1: Script Automatizado (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/MRROBOT-FUTURE.git
cd MRROBOT-FUTURE

# 2. Configure o .env
cp env.template .env
nano .env  # Preencha suas credenciais

# 3. Execute o script de deploy
chmod +x scripts/docker-deploy.sh
./scripts/docker-deploy.sh
```

### Método 2: Manual

```bash
# 1. Clone
git clone https://github.com/seu-usuario/MRROBOT-FUTURE.git
cd MRROBOT-FUTURE

# 2. Configure
cp env.template .env
nano .env

# 3. Build e start
docker-compose up -d --build

# 4. Verificar
docker-compose ps
docker-compose logs -f
```

---

## ⚙️ Configuração

### Arquivo .env

O arquivo `.env` é compartilhado com o container. Configure todas as variáveis:

```env
# Modo
MODE=MOCK  # ou PROD

# Binance
BINANCE_API_KEY=sua_chave_aqui
BINANCE_SECRET_KEY=sua_secret_aqui

# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_aqui

# Webhook
WEBHOOK_PORT=8000
WEBHOOK_SECRET=seu_token_aqui

# ... outras configurações
```

### Recursos do Container

Edite `docker-compose.yml` para ajustar recursos:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'      # Máximo de CPUs
      memory: 1G     # Máximo de RAM
    reservations:
      cpus: '0.5'    # CPUs reservados
      memory: 512M   # RAM reservada
```

---

## 🎮 Deploy

### Desenvolvimento

```bash
# Build e iniciar
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

### Produção

```bash
# Usar arquivo de produção
docker-compose -f docker-compose.prod.yml up -d --build

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f scalping-bot

# Parar
docker-compose -f docker-compose.prod.yml down
```

---

## 🔧 Gerenciamento

### Comandos Essenciais

```bash
# Status dos containers
docker-compose ps

# Logs em tempo real
docker-compose logs -f

# Logs das últimas 100 linhas
docker-compose logs --tail=100

# Reiniciar
docker-compose restart

# Parar
docker-compose stop

# Iniciar
docker-compose start

# Parar e remover
docker-compose down

# Parar, remover e limpar volumes
docker-compose down -v
```

### Entrar no Container

```bash
# Bash interativo
docker-compose exec scalping-bot /bin/bash

# Executar comando único
docker-compose exec scalping-bot python -c "from src.config import get_config; print(get_config().MODE)"
```

### Atualizar o Bot

```bash
# Opção 1: Pull + Rebuild
git pull origin main
docker-compose up -d --build

# Opção 2: Rebuild sem cache
docker-compose build --no-cache
docker-compose up -d

# Opção 3: Recrear container
docker-compose up -d --force-recreate
```

---

## 📊 Monitoramento

### Health Check

```bash
# Via curl
curl http://localhost:8000/health

# Via Docker
docker inspect --format='{{json .State.Health}}' mrrobot-scalping-bot | jq
```

### Logs

```bash
# Logs do container
docker-compose logs -f scalping-bot

# Logs da aplicação (dentro do container)
docker-compose exec scalping-bot tail -f /app/logs/scalping_bot.log

# Logs do Docker daemon
sudo journalctl -u docker.service -f
```

### Métricas de Recursos

```bash
# Uso em tempo real
docker stats mrrobot-scalping-bot

# Uma vez
docker stats --no-stream mrrobot-scalping-bot

# Todos os containers
docker stats
```

### API Endpoints

```bash
# Health
curl http://localhost:8000/health | jq

# Trades abertos
curl http://localhost:8000/trades/open | jq

# Estatísticas
curl http://localhost:8000/stats | jq
```

---

## 🐛 Troubleshooting

### Container não inicia

```bash
# Ver logs de erro
docker-compose logs scalping-bot

# Verificar se porta está em uso
sudo lsof -i :8000
sudo netstat -tulpn | grep 8000

# Verificar configuração
docker-compose config
```

### Erro de conexão com Supabase

```bash
# Testar dentro do container
docker-compose exec scalping-bot curl https://seu-projeto.supabase.co

# Verificar variáveis de ambiente
docker-compose exec scalping-bot env | grep SUPABASE
```

### Erro de conexão com Binance

```bash
# Testar API Binance
docker-compose exec scalping-bot curl https://api.binance.com/api/v3/ping

# Verificar API keys
docker-compose exec scalping-bot env | grep BINANCE
```

### Container reinicia constantemente

```bash
# Ver logs do último crash
docker logs mrrobot-scalping-bot --tail 100

# Verificar health check
docker inspect mrrobot-scalping-bot | jq '.[0].State.Health'

# Desabilitar restart temporariamente
docker update --restart=no mrrobot-scalping-bot
```

### Problemas de permissão com logs

```bash
# Ajustar permissões do diretório logs
sudo chown -R 1000:1000 logs/

# Ou tornar público (menos seguro)
sudo chmod 777 logs/
```

### Rebuild completo

```bash
# Parar tudo
docker-compose down

# Remover imagens
docker rmi mrrobot-scalping-bot

# Limpar build cache
docker builder prune -a

# Rebuild do zero
docker-compose build --no-cache
docker-compose up -d
```

---

## 🚀 GitHub Actions com Docker

### Atualizar workflow para Docker

Edite `.github/workflows/deploy.yml`:

```yaml
name: Deploy Bot com Docker

on:
  push:
    branches: [main, master]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd ${{ secrets.VPS_PATH }}
            
            # Backup do .env
            cp .env .env.backup
            
            # Atualizar código
            git pull origin main
            
            # Restaurar .env
            mv .env.backup .env
            
            # Rebuild e restart
            docker-compose down
            docker-compose up -d --build
            
            # Aguardar inicialização
            sleep 30
            
            # Health check
            curl -f http://localhost:8000/health || exit 1
            
            echo "Deploy concluído com sucesso!"
```

---

## 📈 Otimizações Avançadas

### Build Multi-stage (Otimizar tamanho)

Crie `Dockerfile.optimized`:

```dockerfile
# Stage 1: Build
FROM python:3.10-slim as builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
COPY database/ ./database/

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

RUN mkdir -p logs && \
    useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

USER botuser
EXPOSE 8000

CMD ["python", "-m", "src.main"]
```

### Docker Compose com Watchtower (Auto-update)

```yaml
version: '3.8'

services:
  scalping-bot:
    # ... configuração normal ...
    labels:
      - "com.centurylinklabs.watchtower.enable=true"
  
  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_POLL_INTERVAL=3600  # Verificar a cada hora
      - WATCHTOWER_LABEL_ENABLE=true
```

### Backup Automático

Crie `scripts/docker-backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="$HOME/backups/scalping-bot"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup dos logs
docker cp mrrobot-scalping-bot:/app/logs $BACKUP_DIR/logs_$DATE

# Backup do .env
cp .env $BACKUP_DIR/.env_$DATE

# Manter apenas últimos 7 backups
ls -t $BACKUP_DIR/logs_* | tail -n +8 | xargs rm -rf
ls -t $BACKUP_DIR/.env_* | tail -n +8 | xargs rm -f

echo "Backup concluído: $DATE"
```

---

## 🔐 Segurança

### Boas Práticas

✅ **Não exponha portas desnecessárias**
```yaml
ports:
  - "127.0.0.1:8000:8000"  # Apenas localhost
```

✅ **Use secrets do Docker** (para produção)
```yaml
services:
  scalping-bot:
    secrets:
      - binance_api_key
      - binance_secret

secrets:
  binance_api_key:
    file: ./secrets/binance_api_key.txt
  binance_secret:
    file: ./secrets/binance_secret.txt
```

✅ **Scan de vulnerabilidades**
```bash
docker scan mrrobot-scalping-bot
```

✅ **Atualize imagens base regularmente**
```bash
docker pull python:3.10-slim
docker-compose build --pull
```

---

## 📝 Comandos de Manutenção

```bash
# Limpar containers parados
docker container prune

# Limpar imagens não usadas
docker image prune -a

# Limpar volumes não usados
docker volume prune

# Limpar tudo
docker system prune -a --volumes

# Ver espaço usado
docker system df
```

---

## ✅ Checklist de Deploy Docker

Antes de fazer deploy em produção:

- [ ] Docker e Docker Compose instalados
- [ ] Arquivo .env configurado
- [ ] Supabase configurado e acessível
- [ ] API Keys da Binance configuradas
- [ ] Testado em modo MOCK
- [ ] Portas configuradas (firewall)
- [ ] Recursos adequados (CPU/RAM)
- [ ] Logs funcionando
- [ ] Health check OK
- [ ] Backup configurado

---

## 🎓 Resumo de Comandos

```bash
# Deploy inicial
./scripts/docker-deploy.sh

# Ver status
docker-compose ps

# Logs
docker-compose logs -f

# Reiniciar
docker-compose restart

# Atualizar
git pull && docker-compose up -d --build

# Entrar no container
docker-compose exec scalping-bot /bin/bash

# Parar tudo
docker-compose down

# Health check
curl http://localhost:8000/health
```

---

**🐳 Pronto! Agora você pode rodar o bot em qualquer lugar com Docker!**

**📈 Happy Trading! 🚀**
