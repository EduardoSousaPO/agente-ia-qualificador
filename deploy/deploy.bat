@echo off
echo INICIANDO DEPLOY - AGENTE QUALIFICADOR IA
echo =============================================

REM Verificar se Docker esta instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Docker nao encontrado. Instale o Docker primeiro.
    pause
    exit /b 1
)

REM Parar containers existentes
echo Parando containers existentes...
docker-compose down

REM Build das imagens
echo Construindo imagens...
docker-compose build --no-cache

REM Iniciar servicos
echo Iniciando servicos...
docker-compose up -d

REM Verificar saude dos servicos
echo Verificando saude dos servicos...
timeout /t 30 /nobreak >nul

curl -f http://localhost:5000/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo Backend: OK
) else (
    echo Backend: FALHA
    pause
    exit /b 1
)

echo.
echo DEPLOY CONCLUIDO COM SUCESSO!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo Logs: docker-compose logs -f
echo =============================================
pause
