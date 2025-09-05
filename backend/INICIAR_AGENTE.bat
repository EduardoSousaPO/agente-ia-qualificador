@echo off
echo.
echo ===============================================
echo    AGENTE QUALIFICADOR IA - INICIALIZACAO
echo ===============================================
echo.

cd /d "%~dp0"

echo 🔍 Verificando sistema...
python diagnostico_e_correcao_completa.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERRO: Sistema nao esta pronto!
    echo 🔧 Corrija os problemas listados acima
    pause
    exit /b 1
)

echo.
echo 🚀 Iniciando servidor Flask...
echo 📱 Webhook: http://localhost:5000/api/whatsapp/webhook
echo 🤖 Agente: Ana (Consultora Humanizada)
echo.
echo ⚠️  Para parar o servidor: Ctrl+C
echo.

python main.py

pause


