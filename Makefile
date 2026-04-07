.PHONY: help install dev test lint format clean docs docker-build docker-run docker-stop

help:
	@echo "🏦 API Bancária - Comandos disponíveis"
	@echo ""
	@echo "desenvolvimento:"
	@echo "  make install    - Instala dependências"
	@echo "  make dev        - Roda o servidor em desenvolvimento"
	@echo "  make test       - Executa testes"
	@echo "  make test-cov   - Testes com cobertura"
	@echo ""
	@echo "qualidade:"
	@echo "  make lint       - Verifica lint (flake8)"
	@echo "  make format     - Formata código (black)"
	@echo "  make clean      - Limpa arquivos temporários"
	@echo ""
	@echo "docker:"
	@echo "  make docker-build - Constrói imagem Docker"
	@echo "  make docker-run   - Roda container"
	@echo "  make docker-stop  - Para container"
	@echo ""
	@echo "documentação:"
	@echo "  make docs       - Gera documentação"

install:
	@echo "📦 Instalando dependências..."
	@[ -d .venv ] || python3 -m venv .venv
	@. .venv/bin/activate && pip install --upgrade pip setuptools && pip install -r requirements.txt
	@echo "✅ Dependências instaladas!"

dev:
	@echo "🚀 Iniciando servidor de desenvolvimento..."
	@. .venv/bin/activate && python -m uvicorn app.main:app --reload

test:
	@echo "🧪 Executando testes..."
	@. .venv/bin/activate && pytest -v

test-cov:
	@echo "📊 Executando testes com cobertura..."
	@. .venv/bin/activate && pytest --cov=app --cov-report=html --cov-report=term-missing
	@echo "📈 Cobertura gerada em htmlcov/index.html"

lint:
	@echo "🔍 Verificando lint..."
	@. .venv/bin/activate && pip install flake8
	@. .venv/bin/activate && flake8 app tests --max-line-length=100

format:
	@echo "✨ Formatando código..."
	@. .venv/bin/activate && pip install black
	@. .venv/bin/activate && black app tests

clean:
	@echo "🧹 Limpando arquivos temporários..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info
	@echo "✅ Limpeza concluída!"

docs:
	@echo "📚 Documentação disponível em:"
	@echo "   http://localhost:8000/docs (quando servidor estiver rodando)"
	@echo "   http://localhost:8000/redoc"

docker-build:
	@echo "🐳 Construindo imagem Docker..."
	@docker build -t api-bancaria:latest .
	@echo "✅ Imagem construída!"

docker-run:
	@echo "🐳 Iniciando container..."
	@docker-compose up -d
	@echo "✅ Container rodando em http://localhost:8000"

docker-stop:
	@echo "⛔ Parando container..."
	@docker-compose down
	@echo "✅ Container parado!"

start: install dev
