# Guia de Início Rápido

Bem-vindo! Este guia te ajuda a colocar a API Bancária rodando em 2 minutos.

## ⚡ Forma Mais Rápida (Recomendado)

### Linux / Mac
```bash
./run.sh
```

### Windows
```bash
run.bat
```

Pronto! O servidor estará rodando em: **http://localhost:8000/docs**

---

## 📋 Requisitos

- Python 3.11+ (verifique: `python --version`)
- Git (para clonar o repositório)

## 🔧 Instalação Passo a Passo

### 1. Clone o repositório

```bash
git clone https://github.com/FilipeMadeira13/api-bancaria-fastapi.git
cd api-bancaria-fastapi
```

### 2. Escolha uma forma de rodar:

#### Opção A: Script automático (RECOMENDADO)

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```bash
run.bat
```

#### Opção B: Com Make (se você tem Make instalado)

```bash
make install
make dev
```

#### Opção C: Manual com venv

```bash
# Crie ambiente virtual
python -m venv .venv

# Ative
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Rode o servidor
python -m uvicorn app.main:app --reload
```

#### Opção D: Com Poetry

```bash
poetry install
poetry run uvicorn app.main:app --reload
```

---

## 🧪 Testar a API

Depois que o servidor estiver rodando, acesse:

- 📘 **Swagger UI (Recomendado)**: http://localhost:8000/docs
- 📙 **ReDoc**: http://localhost:8000/redoc

### Teste rápido com cURL

```bash
# 1. Registre um usuário
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"name":"Seu Nome","email":"seu@email.com","password":"123456"}'

# Você receberá um token JWT
```

---

## 🧪 Rodar Testes

```bash
# Com Script
make test

# Ou manual
pytest -v

# Com cobertura
pytest --cov=app --cov-report=html
```

---

## 🛠️ Comandos Úteis

```bash
# Ver todos os comandos disponíveis
make help

# Formatar código
make format

# Verificar lint
make lint

# Limpar arquivos temporários
make clean

# Rodar com Docker
make docker-run
```

---

## 🤔 Problemas?

### "uvicorn not found"
```bash
pip install uvicorn
```

### "Python version not supported"
Certifique-se que tem Python 3.11+:
```bash
python --version
```

### "ModuleNotFoundError: No module named 'app'"
Certifique-se de estar no diretório certo:
```bash
cd api-bancaria-fastapi
```

Veja [Troubleshooting](README.md#-troubleshooting) no README para mais problemas.

---

## 📚 Próximos Passos

1. Leia o [README.md](README.md) para documentação completa
2. Explore a documentação interativa em http://localhost:8000/docs
3. Veja [CONTRIBUTING.md](CONTRIBUTING.md) se quer contribuir

---

## 💡 Dicas Úteis

- Use `--reload` no uvicorn para auto-reload ao modificar arquivos
- Configure `.env` com suas variáveis de ambiente
- Rode `make test` antes de fazer commits
- Use `make format` para manter o código limpo

---

**Precisa de ajuda?** Veja [CONTRIBUTING.md](CONTRIBUTING.md) ou abra uma issue no GitHub.

**Happy coding! 🚀**
