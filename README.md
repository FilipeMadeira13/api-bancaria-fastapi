# 💸 API Bancária Assíncrona com FastAPI

Projeto de uma API RESTful para gerenciamento de contas bancárias, transações (depósitos e saques) e exibição de extratos. Utiliza autenticação JWT e arquitetura assíncrona com FastAPI e SQLModel.

---

## 🚀 Funcionalidades

- ✅ Cadastro e autenticação de usuários com JWT
- ✅ Criação de contas bancárias únicas por usuário
- ✅ Registro de transações (depósito e saque)
- ✅ Validação de saldo e valores positivos
- ✅ Consulta de extrato com filtros (tipo e data)
- ✅ Endpoints protegidos por autenticação
- ✅ Banco de dados SQLite assíncrono (aiosqlite)
- ✅ Testes automatizados com `pytest` e `httpx`
- ✅ Documentação automática via Swagger e OpenAPI

---

## 📦 Tecnologias

- Python 3.13
- FastAPI
- SQLModel
- SQLite + aiosqlite (async)
- JWT (via `python-jose`)
- Alembic (migrações)
- Pytest (testes)
- Pydantic v2

---

## 🏗️ Estrutura do Projeto

```bash
api-bancaria-fastapi/
├── app/
│ ├── core/ # Segurança, JWT, configurações
│ ├── domain/ # Modelos e esquemas
│ ├── infra/ # Banco de dados, sessão
│ ├── routers/ # Endpoints (auth, account, transaction, statement)
│ └── main.py # Inicialização da API
├── tests/ # Testes automatizados
├── alembic/ # Controle de migrações
├── requirements.txt
└── README.md
```

---

## ⚙️ Como executar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/FilipeMadeira13/api-bancaria-fastapi.git
cd api-bancaria-fastapi
```

### 2. Criar ambiente virtual e instalar dependências

```bash
poetry install --no-root
```

### 3. Rodar o servidor

```bash
uvicorn app.main:app --reload
```

Acesse em: http://localhost:8000/docs

## 🧪 Rodar os testes

```bash
pytest -v
```

## 🔐 Autenticação

A autenticação é baseada em JWT.
Após o registro/login, envie o token no header:

```makefile
Authorization: Bearer <seu_token>
```

## 📄 Documentação interativa

- Swagger UI: http://localhost:8000/docs

- OpenAPI JSON: http://localhost:8000/openapi.json

## 🛠️ Futuras melhorias

- Integração com banco PostgreSQL

- Suporte a múltiplas contas por usuário

- Dashboard com dados agregados

- Deploy com Docker e CI/CD

## 👨‍💻 Autor

Carlos Filipe Madeira de Souza
Desenvolvedor em formação com foco em APIs, dados e engenharia de software.

- GitHub: [@FilipeMadeira13](https://github.com/FilipeMadeira13)

- [LinkedIn](linkedin.com/in/carlos-filipe-madeira-de-souza-16211922a)

## 📝 Licença

Este projeto está licenciado sob a MIT License.
