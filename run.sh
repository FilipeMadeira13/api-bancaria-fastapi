#!/bin/bash

# API Bancária - Run Server Script
# Executa o servidor FastAPI com configurações automáticas

set -e

echo "🚀 Iniciando API Bancária..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "📦 Instalando dependências..."
    pip install --upgrade pip setuptools
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️ Criando arquivo .env..."
    cp .env.example .env
    echo "⚠️ Atualize as variáveis em .env conforme necessário"
fi

# Run the server
echo "✅ Ambiente pronto!"
echo ""
echo "📚 Documentação: http://localhost:8000/docs"
echo "🔗 API Principal: http://localhost:8000"
echo ""
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
