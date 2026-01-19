# 🐳 DOCKER - INSTALAÇÃO COMPLETA

## ✅ Arquivos Docker Criados

### 📄 Dockerfile
- Imagem Python 3.10 slim otimizada
- Multi-stage possível para menor tamanho
- Usuário não-root para segurança
- Health check integrado
- **Localização:** `Dockerfile`

### 📄 docker-compose.yml
- Configuração padrão de desenvolvimento
- Volumes para logs persistentes
- Controle de recursos (CPU/RAM)
- Networking isolado
- **Localização:** `docker-compose.yml`

### 📄 docker-compose.prod.yml
- Configuração otimizada para produção
- Recursos aumentados
- Health check mais rigoroso
- Logging otimizado
- Watchtower para auto-update
- **Localização:** `docker-compose.prod.yml`

### 📄 .dockerignore
- Otimização de build
- Exclui arquivos desnecessários
- Reduz tamanho da imagem
- **Localização:** `.dockerignore`

### 📄 docker-deploy.sh
- Script automatizado de deploy
- Validações de ambiente
- Build e start automatizados
- Health check pós-deploy
- **Localização:** `scripts/docker-deploy.sh`

### 📄 deploy-docker.yml
- GitHub Actions para Docker
- Deploy automatizado via SSH
- Rebuild e restart automatizados
- Health check integrado
- **Localização:** `.github/workflows/deploy-docker.yml`

### 📄 Documentação
- **DOCKER_SETUP.md** - Guia completo (docs/DOCKER_SETUP.md)
- **DOCKER_QUICKSTART.md** - Guia rápido (DOCKER_QUICKSTART.md)

---

## 🚀 Como Usar

### Opção 1: Script Automatizado (Mais Fácil)

```bash
# 1. Configure credenciais
cp env.template .env
nano .env

# 2. Execute o script
chmod +x scripts/docker-deploy.sh
./scripts/docker-deploy.sh

# Pronto! ✅
```

### Opção 2: Manual

```bash
# Desenvolvimento
docker-compose up -d --build

# Produção
docker-compose -f docker-compose.prod.yml up -d --build
```

---

## 📊 Comandos Principais

```bash
# Status
docker-compose ps

# Logs em tempo real
docker-compose logs -f

# Reiniciar
docker-compose restart

# Parar
docker-compose down

# Atualizar código
git pull
docker-compose up -d --build

# Health check
curl http://localhost:8000/health

# Entrar no container
docker-compose exec scalping-bot /bin/bash

# Ver recursos
docker stats mrrobot-scalping-bot
```

---

## 🔧 Vantagens do Docker

✅ **Portabilidade** - Roda em qualquer servidor  
✅ **Isolamento** - Não interfere com outros serviços  
✅ **Consistência** - Mesmo ambiente em dev/prod  
✅ **Facilidade** - Deploy em minutos  
✅ **Segurança** - Container isolado  
✅ **Recursos** - Controle de CPU/RAM  
✅ **Logs** - Centralizados  
✅ **Updates** - Rápidos e seguros  

---

## 📦 Estrutura de Arquivos

```
MRROBOT-FUTURE/
├── Dockerfile                          # Imagem Docker
├── docker-compose.yml                  # Compose dev
├── docker-compose.prod.yml             # Compose prod
├── docker-compose.override.yml.example # Override exemplo
├── .dockerignore                       # Arquivos ignorados
├── DOCKER_QUICKSTART.md                # Guia rápido
├── .github/workflows/
│   └── deploy-docker.yml               # GitHub Actions
├── docs/
│   └── DOCKER_SETUP.md                 # Guia completo
└── scripts/
    └── docker-deploy.sh                # Script de deploy
```

---

## 🎯 Requisitos

- Docker 20.10+
- Docker Compose 1.29+
- 2GB RAM mínimo
- 10GB espaço em disco

---

## 📚 Documentação

- **Guia Completo:** [docs/DOCKER_SETUP.md](docs/DOCKER_SETUP.md)
- **Quick Start:** [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)
- **README Principal:** [README.md](README.md)

---

## ✅ Checklist de Deploy

- [ ] Docker e Docker Compose instalados
- [ ] Arquivo .env configurado
- [ ] Supabase configurado
- [ ] API Keys da Binance configuradas
- [ ] Portas abertas no firewall
- [ ] Testado em modo MOCK
- [ ] GitHub Actions configurado (opcional)

---

## 🎉 Pronto!

Seu bot agora roda em Docker! 🐳

**Comandos essenciais:**
```bash
# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

---

**📈 Happy Trading! 🚀**
