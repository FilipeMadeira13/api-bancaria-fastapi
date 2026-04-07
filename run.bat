@echo off
REM API Bancária - Run Server Script (Windows)
REM Executa o servidor FastAPI com configurações automáticas

echo 🚀 Iniciando API Bancaria...

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo 📦 Instalando dependencias...
    python -m pip install --upgrade pip setuptools
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

REM Check if .env exists
if not exist ".env" (
    echo ⚙️ Criando arquivo .env...
    copy .env.example .env
    echo ⚠️ Atualize as variaveis em .env conforme necessario
)

REM Run the server
echo ✅ Ambiente pronto!
echo.
echo 📚 Documentação: http://localhost:8000/docs
echo 🔗 API Principal: http://localhost:8000
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
