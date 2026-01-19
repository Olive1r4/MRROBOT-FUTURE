# 🐳 Docker Quick Start

Guia ultra-rápido para rodar o bot com Docker.

## ⚡ 3 Comandos para Começar

```bash
# 1. Configure
cp env.template .env && nano .env

# 2. Deploy
./scripts/docker-deploy.sh

# 3. Monitore
docker-compose logs -f
```

## 📊 Comandos Essenciais

```bash
# Status
docker-compose ps

# Logs
docker-compose logs -f

# Reiniciar
docker-compose restart

# Parar
docker-compose down

# Atualizar
git pull && docker-compose up -d --build

# Entrar no container
docker-compose exec scalping-bot /bin/bash

# Health check
curl http://localhost:8000/health
```

## 🔧 Troubleshooting Rápido

```bash
# Ver erros
docker-compose logs --tail=50

# Rebuild completo
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Ver recursos
docker stats
```

## 📚 Documentação Completa

Para mais detalhes, veja: [docs/DOCKER_SETUP.md](docs/DOCKER_SETUP.md)

---

**🚀 É só isso! Seu bot está rodando em Docker!**
