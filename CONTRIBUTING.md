# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o MRROBOT-FUTURE! Este documento fornece diretrizes para contribuir com o projeto.

---

## 📋 Código de Conduta

Ao participar deste projeto, você concorda em manter um ambiente respeitoso e colaborativo. Esperamos:

- ✅ Respeito mútuo entre contribuidores
- ✅ Feedback construtivo
- ✅ Foco em melhorar o projeto
- ❌ Linguagem ofensiva ou comportamento inadequado

---

## 🚀 Como Contribuir

### 1. Reportar Bugs

Se você encontrou um bug:

1. Verifique se já não existe uma [issue](https://github.com/seu-usuario/MRROBOT-FUTURE/issues) sobre o problema
2. Se não existir, crie uma nova issue com:
   - **Título claro:** Ex: "Circuit breaker não ativa em modo PROD"
   - **Descrição detalhada:** O que aconteceu vs o que era esperado
   - **Passos para reproduzir:** Como replicar o bug
   - **Ambiente:** Modo (MOCK/PROD), Python version, SO
   - **Logs:** Cole logs relevantes (remova informações sensíveis!)

**Template de Bug Report:**
```markdown
## Descrição
[Descreva o bug de forma clara]

## Passos para Reproduzir
1. Configure MODE=PROD
2. Execute trade manual
3. ...

## Comportamento Esperado
[O que deveria acontecer]

## Comportamento Atual
[O que realmente aconteceu]

## Ambiente
- Modo: MOCK/PROD
- Python: 3.10.5
- SO: Ubuntu 22.04
- Versão do bot: v1.0.0

## Logs
```
[Cole logs relevantes aqui]
```
```

---

### 2. Sugerir Melhorias

Para sugerir novas funcionalidades:

1. Abra uma issue com a tag `enhancement`
2. Descreva:
   - **Problema que resolve:** Por que essa feature é útil?
   - **Solução proposta:** Como funcionaria?
   - **Alternativas consideradas:** Outras abordagens possíveis?
   - **Impacto:** Afeta performance? Segurança? Compatibilidade?

**Template de Feature Request:**
```markdown
## Problema
[Descreva o problema que a feature resolve]

## Solução Proposta
[Como a feature funcionaria]

## Alternativas
[Outras formas de resolver o problema]

## Benefícios
- Melhora performance em X%
- Facilita uso para Y
- ...

## Impactos
- [ ] Requer mudanças no banco de dados
- [ ] Requer mudanças na API
- [ ] Pode afetar trades existentes
```

---

### 3. Contribuir com Código

#### 3.1. Fork e Clone

```bash
# Fork o repositório no GitHub
# Depois clone seu fork

git clone https://github.com/seu-usuario/MRROBOT-FUTURE.git
cd MRROBOT-FUTURE

# Adicione o repositório original como upstream
git remote add upstream https://github.com/original-usuario/MRROBOT-FUTURE.git
```

#### 3.2. Crie uma Branch

```bash
# Atualize main
git checkout main
git pull upstream main

# Crie branch para sua feature
git checkout -b feature/nome-da-feature

# Ou para bugfix
git checkout -b fix/nome-do-bug
```

**Convenção de nomes:**
- `feature/` - Novas funcionalidades
- `fix/` - Correções de bugs
- `docs/` - Melhorias na documentação
- `refactor/` - Refatoração de código
- `test/` - Adição/melhoria de testes

#### 3.3. Faça suas Alterações

**Boas práticas:**

✅ **Código limpo:**
- Use nomes descritivos para variáveis e funções
- Adicione docstrings em funções complexas
- Mantenha funções pequenas e focadas
- Siga PEP 8 (use `black` para formatação)

✅ **Testes:**
- Teste suas alterações em modo MOCK
- Adicione testes para novas funcionalidades
- Verifique se não quebrou testes existentes

✅ **Documentação:**
- Atualize README.md se necessário
- Adicione comentários em código complexo
- Atualize docstrings

✅ **Commits:**
- Commits pequenos e focados
- Mensagens claras e descritivas
- Use português ou inglês (seja consistente)

**Exemplo de bom commit:**
```bash
git commit -m "feat: adiciona suporte a trailing stop loss

- Implementa trailing stop que acompanha o preço
- Adiciona parâmetro TRAILING_STOP_PERCENTAGE no config
- Atualiza documentação com exemplos
- Testes em modo MOCK passando"
```

#### 3.4. Teste Localmente

```bash
# Instale dependências de desenvolvimento
pip install -r requirements.txt
pip install black flake8 pytest

# Formate código
black src/

# Verifique linting
flake8 src/ --max-line-length=120

# Execute testes
pytest tests/

# Teste manualmente
MODE=MOCK python -m src.main
```

#### 3.5. Push e Pull Request

```bash
# Push para seu fork
git push origin feature/nome-da-feature

# No GitHub, abra um Pull Request
```

**Template de Pull Request:**
```markdown
## Descrição
[Descreva as mudanças de forma clara]

## Tipo de Mudança
- [ ] Bug fix (correção que não quebra funcionalidade existente)
- [ ] Nova feature (adiciona funcionalidade sem quebrar existente)
- [ ] Breaking change (mudança que quebra funcionalidade existente)
- [ ] Documentação

## Como Foi Testado?
- [ ] Testado em modo MOCK
- [ ] Testado em modo PROD (com valores mínimos)
- [ ] Testes automatizados adicionados
- [ ] Documentação atualizada

## Checklist
- [ ] Código segue o estilo do projeto
- [ ] Comentários adicionados em código complexo
- [ ] Documentação atualizada
- [ ] Nenhum warning novo foi introduzido
- [ ] Testes passam localmente
- [ ] Commits são atômicos e bem descritos

## Screenshots (se aplicável)
[Adicione screenshots se houver mudanças visuais]

## Issues Relacionadas
Closes #123
Related to #456
```

---

## 🎨 Padrões de Código

### Python

**Formatação:**
- Use `black` com linha de 120 caracteres
- Use `flake8` para linting
- Siga PEP 8

**Imports:**
```python
# Ordem de imports:
# 1. Bibliotecas padrão
# 2. Bibliotecas de terceiros
# 3. Módulos locais

import os
from datetime import datetime
from typing import Dict, List

import numpy as np
import pandas as pd
from fastapi import FastAPI

from src.config import get_config
from src.database import Database
```

**Docstrings:**
```python
def calculate_position_size(symbol: str, price: float, config: Dict) -> float:
    """
    Calcula o tamanho da posição baseado no risco.
    
    Args:
        symbol: Símbolo da moeda (ex: BTCUSDT)
        price: Preço atual da moeda
        config: Configuração da moeda do banco de dados
    
    Returns:
        Tamanho da posição em USDT
    
    Raises:
        ValueError: Se o preço for inválido
    """
    pass
```

**Type Hints:**
```python
# Use type hints sempre que possível
def get_trades(symbol: str, limit: int = 10) -> List[Dict]:
    pass

# Para tipos complexos
from typing import Optional, Union, Tuple

def analyze_signal(data: List[float]) -> Tuple[bool, str]:
    pass
```

---

## 🧪 Testes

### Estrutura de Testes

```
tests/
├── test_config.py
├── test_database.py
├── test_exchange_manager.py
├── test_indicators.py
└── test_risk_manager.py
```

### Exemplo de Teste

```python
import pytest
from src.indicators import TechnicalIndicators

def test_rsi_calculation():
    """Testa cálculo do RSI"""
    indicators = TechnicalIndicators()
    
    # Dados de teste
    prices = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 
              111, 110, 112, 114, 113]
    
    # Calcular RSI
    rsi = indicators.calculate_rsi(prices, period=14)
    
    # Verificações
    assert 0 <= rsi <= 100, "RSI deve estar entre 0 e 100"
    assert rsi > 50, "RSI deve estar acima de 50 para preços em alta"

def test_rsi_with_insufficient_data():
    """Testa RSI com dados insuficientes"""
    indicators = TechnicalIndicators()
    
    prices = [100, 102, 101]  # Apenas 3 valores
    
    rsi = indicators.calculate_rsi(prices, period=14)
    
    # Deve retornar valor neutro
    assert rsi == 50.0
```

### Executar Testes

```bash
# Todos os testes
pytest

# Teste específico
pytest tests/test_indicators.py

# Com cobertura
pytest --cov=src tests/

# Verbose
pytest -v
```

---

## 📚 Documentação

### Quando Atualizar

Atualize documentação quando:

- ✅ Adicionar nova funcionalidade
- ✅ Mudar comportamento existente
- ✅ Adicionar/remover parâmetros de configuração
- ✅ Mudar API endpoints
- ✅ Corrigir informações incorretas

### Arquivos a Atualizar

- `README.md` - Para mudanças gerais
- `docs/API_EXAMPLES.md` - Para mudanças na API
- `docs/ESTRATEGIAS.md` - Para mudanças nas estratégias
- `ESTRUTURA_PROJETO.md` - Para mudanças estruturais
- Docstrings no código

---

## 🔍 Code Review

### O que Revisamos

- ✅ Código funciona como esperado
- ✅ Testes adequados foram adicionados
- ✅ Documentação foi atualizada
- ✅ Código segue padrões do projeto
- ✅ Não introduz vulnerabilidades de segurança
- ✅ Performance não foi degradada
- ✅ Não quebra funcionalidades existentes

### Processo

1. Mantenedor revisa o PR
2. Solicita mudanças se necessário
3. Contribuidor faz ajustes
4. Mantenedor aprova e faz merge

---

## 🏷️ Versionamento

Seguimos [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Mudanças incompatíveis na API
- **MINOR** (0.1.0): Nova funcionalidade compatível
- **PATCH** (0.0.1): Correções de bugs compatíveis

---

## 🎯 Áreas que Precisam de Ajuda

Contribuições são especialmente bem-vindas em:

### Alta Prioridade
- 🔴 Testes automatizados (cobertura atual: 0%)
- 🔴 Backtesting framework
- 🔴 Dashboard web em tempo real

### Média Prioridade
- 🟡 Suporte a Shorts
- 🟡 Trailing stop loss
- 🟡 Notificações (Telegram/Discord)
- 🟡 Machine Learning para otimização

### Baixa Prioridade
- 🟢 Suporte a outras exchanges
- 🟢 Múltiplos timeframes
- 🟢 Volume profile
- 🟢 Melhorias na documentação

---

## 💬 Comunicação

### Onde Discutir

- **Issues:** Para bugs e features específicas
- **Pull Requests:** Para discussão de código
- **Discussions:** Para ideias gerais e dúvidas

### Etiqueta

- Seja respeitoso e construtivo
- Forneça contexto suficiente
- Seja paciente - mantenedores são voluntários
- Agradeça feedback recebido

---

## 🎓 Recursos para Contribuidores

### Documentação do Projeto

- [README.md](README.md) - Visão geral
- [ESTRUTURA_PROJETO.md](ESTRUTURA_PROJETO.md) - Arquitetura
- [ESTRATEGIAS.md](docs/ESTRATEGIAS.md) - Lógica de trading
- [TESTES.md](docs/TESTES.md) - Como testar

### Ferramentas Úteis

- [Black](https://black.readthedocs.io/) - Formatação de código
- [Flake8](https://flake8.pycqa.org/) - Linting
- [Pytest](https://pytest.org/) - Framework de testes
- [Git](https://git-scm.com/doc) - Controle de versão

### Aprendizado

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [CCXT Documentation](https://docs.ccxt.com/)
- [Supabase Docs](https://supabase.com/docs)
- [Trading Strategies](https://www.investopedia.com/)

---

## ✅ Checklist Final

Antes de submeter seu PR:

- [ ] Código formatado com `black`
- [ ] Linting passa (`flake8`)
- [ ] Testes adicionados/atualizados
- [ ] Testes passam (`pytest`)
- [ ] Documentação atualizada
- [ ] Commits bem descritos
- [ ] Branch atualizada com main
- [ ] PR template preenchido
- [ ] Testado em modo MOCK
- [ ] Sem informações sensíveis no código

---

## 🙏 Agradecimentos

Obrigado por contribuir! Cada contribuição, por menor que seja, ajuda a melhorar o projeto para toda a comunidade.

**Contribuidores principais:**
- [Lista será atualizada conforme contribuições]

---

## 📝 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto (MIT License).

---

**🚀 Pronto para contribuir? Comece abrindo uma issue ou fork do projeto!**
