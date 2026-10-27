# 💸 API Bancária Assíncrona com FastAPI

[![Python](https://img.shields.io/badge/Python-3.11+-3776ab?logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Projeto de uma **API RESTful assíncrona** para gerenciamento de contas bancárias, transações e extratos. Desenvolvida com arquitetura limpa, autenticação JWT, testes automatizados e pronta para deploy.

**[Demo](#-exemplos-de-execução)** • **[Documentação](#-documentação-dos-endpoints)** • **[Deployment](#-deployment)** • **[Contribuir](#-contribuindo)**

---

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Como usar](#-como-usar)
- [Endpoints](#-documentação-dos-endpoints)
- [Testes](#-testes)
- [Docker](#-docker)
- [Deployment](#-deployment)
- [CI/CD](#-cicd-github-actions)
- [Troubleshooting](#-troubleshooting)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🚀 Funcionalidades

- ✅ **Autenticação JWT** - Registro, login e geração de tokens
- ✅ **Gerenciamento de contas** - Uma conta por usuário
- ✅ **Transações** - Depósitos e saques com validação de saldo
- ✅ **Extrato** - Consulta com filtros por tipo e intervalo de datas
- ✅ **Validações** - Valores positivos, saldo suficiente, emails únicos
- ✅ **Assincronismo** - SQLite async + aiosqlite
- ✅ **Testes automatizados** - 7 testes cobrindo fluxos principais
- ✅ **Clean Architecture** - Separação clara de responsabilidades
- ✅ **Documentação automática** - Swagger UI e OpenAPI
- ✅ **Docker ready** - Pronto para containerização
- ✅ **Migrations** - Alembic para versionamento do schema

---

## 📦 Tecnologias

| Categoria | Tecnologia |
|-----------|-----------|
| **Linguagem** | Python 3.11+ |
| **Framework Web** | FastAPI 0.104+ |
| **ORM/Modelos** | SQLModel + SQLAlchemy |
| **Banco de Dados** | SQLite + aiosqlite |
| **Autenticação** | JWT (python-jose) + bcrypt |
| **Validação** | Pydantic v2 |
| **Configuração** | pydantic-settings |
| **Testes** | pytest + pytest-asyncio |
| **Migrações** | Alembic |
| **Containerização** | Docker + Docker Compose |

---

## ⚡ Requisitos

- Python 3.11+
- Poetry (recomendado) ou pip
- Docker & Docker Compose (para containerização)
- Git

---

## 📦 Instalação

As dependências são declaradas em `pyproject.toml`, a fonte de referência do projeto. O arquivo `poetry.lock` registra as versões resolvidas para tornar as instalações reproduzíveis.

As ferramentas de testes e qualidade (`pytest`, `pytest-asyncio`, `httpx`, `pytest-cov`, Black e flake8) ficam no grupo de desenvolvimento `dev`.

### Opção 1: Com Poetry (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/FilipeMadeira13/api-bancaria-fastapi.git
cd api-bancaria-fastapi

# Instale as dependências de execução e desenvolvimento
poetry install --with dev

# Ative o ambiente virtual
poetry shell
```

### Opção 2: Com pip e venv

O `requirements.txt` é uma exportação das dependências resolvidas pelo Poetry e inclui execução e desenvolvimento. Ele contém hashes para verificar a integridade dos pacotes baixados. Ao alterar dependências, atualize a declaração em `pyproject.toml` e sincronize o lock e a exportação; evite editar o `requirements.txt` manualmente.

```bash
# Clone o repositório
git clone https://github.com/FilipeMadeira13/api-bancaria-fastapi.git
cd api-bancaria-fastapi

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências verificando os hashes
pip install --require-hashes -r requirements.txt
```

---

## ⚙️ Configuração

### Variáveis de Ambiente

Copie o arquivo de exemplo e configure conforme necessário:

```bash
cp .env.example .env
```

**Variáveis disponíveis:**

```env
# Segurança
SECRET_KEY=sua-chave-secreta-muito-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Banco de Dados
DATABASE_URL=sqlite+aiosqlite:///./bank.db
SQL_ECHO=false  # Ativa logs SQL (útil para debug)
```

⚠️ **Em produção:**
- Gere uma SECRET_KEY forte: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- Use um banco PostgreSQL ou MySQL
- Defina `SQL_ECHO=false`

---

## 🏃 Como usar

### 1. Ativar o ambiente virtual

```bash
# Com .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Com Poetry
poetry shell
```

### 2. Rodar o servidor de desenvolvimento

**Forma mais fácil (recomendado):**

```bash
# Linux/Mac
./run.sh

# Windows
run.bat
```

**Formas alternativas:**

```bash
# Direto com uvicorn
uvicorn app.main:app --reload

# Ou com Python module
python -m uvicorn app.main:app --reload

# Ou com Poetry
poetry run uvicorn app.main:app --reload
```

Servidor rodando em: **http://localhost:8000**

### 3. Acessar a documentação

- 📘 **Swagger UI**: http://localhost:8000/docs
- 📙 **ReDoc**: http://localhost:8000/redoc
- 📄 **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 📝 Documentação dos Endpoints

### Autenticação

#### Registrar novo usuário
```http
POST /auth/register
Content-Type: application/json

{
  "name": "João Silva",
  "email": "joao@example.com",
  "password": "senha-segura-aqui"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Fazer login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=joao@example.com&password=senha-segura-aqui

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Contas

#### Criar conta bancária
```http
POST /account/
Authorization: Bearer {seu_token}

Response (201):
{
  "id": 1,
  "user_id": 1,
  "balance": 0.0
}
```

### Transações

#### Registrar transação (Depósito/Saque)
```http
POST /transaction/
Authorization: Bearer {seu_token}
Content-Type: application/json

{
  "type": "deposit",
  "value": 100.00
}

Response (201):
{
  "message": "Deposit realizado com sucesso",
  "new_balance": 100.00,
  "transaction_id": 1
}
```

Tipos: `"deposit"` ou `"withdraw"`

### Extrato

#### Consultar transações
```http
GET /statement/
Authorization: Bearer {seu_token}

Response (200):
[
  {
    "id": 1,
    "account_id": 1,
    "type": "deposit",
    "value": 100.00,
    "timestamp": "2026-04-06T10:30:00"
  }
]
```

**Filtros opcionais:**
- `?type=deposit` - Filtra por tipo
- `?start_date=2026-04-01T00:00:00&end_date=2026-04-06T23:59:59` - Filtra por intervalo

---

## 📊 Exemplos de Execução

### Com cURL

```bash
# 1. Registrar usuário
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"name":"João","email":"joao@test.com","password":"123456"}'

# 2. Extrair token (será retornado no passo anterior)
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# 3. Criar conta
curl -X POST "http://localhost:8000/account/" \
  -H "Authorization: Bearer $TOKEN"

# 4. depositar dinheiro
curl -X POST "http://localhost:8000/transaction/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"deposit","value":500.00}'

# 5. Consultar extrato
curl -X GET "http://localhost:8000/statement/" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🧪 Testes

Instale as dependências de desenvolvimento antes de executar os testes. Os dois caminhos da seção de instalação incluem essas ferramentas; `pytest-cov` fornece as opções de cobertura usadas abaixo.

### Rodar testes com cobertura

```bash
# Todos os testes
poetry run pytest -v

# Com relatório de cobertura
poetry run pytest --cov=app --cov-report=html

# Teste específico
poetry run pytest tests/test_auth.py -v
```

Os testes estão organizados por autenticação, contas, transações e extrato. Confirme os resultados e a cobertura executando os comandos acima; esta atualização da documentação não incluiu execução de testes.

---

## 🐳 Docker

### Construir imagem

```bash
docker build -t api-bancaria:latest .
```

### Rodar container

```bash
docker run -p 8000:8000 \
  -e SECRET_KEY=sua-chave \
  -e DATABASE_URL=sqlite+aiosqlite:///./bank.db \
  api-bancaria:latest
```

### Com Docker Compose

```bash
docker-compose up -d
```

**Arquivo `docker-compose.yml` (criar se não existir):**

```yaml
version: '3.9'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      SECRET_KEY: ${SECRET_KEY:-super-secret}
      DATABASE_URL: sqlite+aiosqlite:///./bank.db
      SQL_ECHO: "false"
    volumes:
      - ./bank.db:/app/bank.db
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 🚀 Deployment

### Railway

```bash
# 1. Instale Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Init project
railway init

# 4. Deploy
railway up
```

### Heroku

```bash
# 1. Create app
heroku create nome-da-sua-api

# 2. Set environment variables
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# 3. Deploy
git push heroku main
```

### Render

1. Conecte seu repositório GitHub ao [Render.com](https://render.com)
2. Configure as variáveis de ambiente no dashboard
3. Deploy automático ao fazer push

### Variáveis de Ambiente para Produção

```env
SECRET_KEY=your-strong-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=postgresql://user:password@host:5432/dbname
SQL_ECHO=false
```

---

## 🔄 CI/CD (GitHub Actions)

Crie `.github/workflows/tests.yml` para testes automáticos:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.11', '3.12', '3.13']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install poetry
        poetry install
    
    - name: Run tests
      run: poetry run pytest -v --cov=app
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
```

---

## 📋 Estrutura do Projeto

```
api-bancaria-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Inicialização FastAPI
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configurações (env variables)
│   │   └── security.py        # Autenticação JWT, hash
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py          # SQLModel (User, Account, Transaction)
│   │   └── schemas.py         # Pydantic schemas (request/response)
│   ├── infra/
│   │   ├── __init__.py
│   │   └── database.py        # Conexão e sessão async
│   └── routers/
│       ├── __init__.py
│       ├── auth.py            # /auth/* endpoints
│       ├── account.py         # /account/* endpoints
│       ├── transaction.py     # /transaction/* endpoints
│       └── statement.py       # /statement/* endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Configuração pytest
│   ├── test_auth.py
│   ├── test_account.py
│   ├── test_transaction.py
│   └── test_statement.py
├── alembic/                    # Migrações de banco
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## 🔧 Troubleshooting

### Erro: "Current Python version X is not allowed by the project (>=3.13)"

```bash
# Seu projeto agora funciona com Python 3.11+
# Se você está usando Poetry com Python 3.12, use:
poetry env use $(which python3)

# Ou instale as dependências diretamente:
pip install -r requirements.txt
```

### Erro: "Command 'uvicorn' not found"

```bash
# Ative o ambiente virtual primeiro
source .venv/bin/activate

# Depois reinstale as dependências
pip install uvicorn fastapi

# Ou use poetry
poetry install
```

### Erro: "No module named 'app'"

```bash
# Certifique-se de rodar do diretório raiz
cd api-bancaria-fastapi

# E use o uvicorn corretamente
python -m uvicorn app.main:app --reload
```

### Erro: "Password cannot be longer than 72 bytes"

- Use bcrypt nativo (já implementado)
- Não use senhas com mais de 72 caracteres

### Banco de dados não criado

```bash
# O banco é criado automaticamente ao rodar a app
# Se quiser forçar:
python -c "from app.infra.database import create_db_and_tables; import asyncio; asyncio.run(create_db_and_tables())"
```

### Testes falhando

```bash
# Limpe o ambiente
rm -rf .venv
python -m venv .venv
source .venv/bin/activate

# Instale dependências
pip install -r requirements.txt

# Rode os testes novamente
pytest -v
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. **Fork** o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um **Pull Request**

### Padrões de Código

- Use [Black](https://github.com/psf/black) para formatação
- Siga [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Adicione testes para novas funcionalidades
- Mantenha testes com cobertura > 80%

### Configurar pre-commit (opcional)

```bash
pip install pre-commit
pre-commit install
```

---

## 📚 Melhorias Futuras

- [ ] Integração com banco PostgreSQL
- [ ] Suporte a múltiplas contas por usuário
- [ ] Dashboard com dados agregados
- [ ] Webhook para notificações
- [ ] Rate limiting
- [ ] Paginação avançada
- [ ] Testes de carga (k6/locust)
- [ ] Observabilidade (Prometheus, Grafana)
- [ ] CORS configurável
- [ ] Swagger authentication

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Carlos Filipe Madeira de Souza**

Desenvolvedor em formação com foco em APIs, dados e engenharia de software.

- 🐙 GitHub: [@FilipeMadeira13](https://github.com/FilipeMadeira13)
- 💼 LinkedIn: [Carlos Filipe](https://linkedin.com/in/carlos-filipe-madeira-de-souza-16211922a)
- 📧 Email: cfilipemadeira@gmail.com

---

## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com) - Framework excepcional
- [SQLModel](https://sqlmodel.tiangolo.com) - ORM moderno
- [Pydantic](https://docs.pydantic.dev) - Validação de dados

---

**Made with ❤️ by [Carlos Filipe](https://github.com/FilipeMadeira13)**

