@echo off
echo MONITORAMENTO - AGENTE QUALIFICADOR IA
echo ========================================

echo Status dos Containers:
docker-compose ps

echo.
echo Health Checks:

REM Backend
curl -f http://localhost:5000/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo Backend: ONLINE
) else (
    echo Backend: OFFLINE
)

REM Frontend
curl -f http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo Frontend: ONLINE
) else (
    echo Frontend: OFFLINE
)

echo.
echo Logs Recentes:
docker-compose logs --tail=10

pause
