@echo off
chcp 65001 > nul
title Agente Qualificador - Inicialização OTIMIZADA

echo.
echo ⚡ INICIALIZAÇÃO SUPER OTIMIZADA ⚡
echo ================================
echo.

:: Verificar se já está rodando
echo 🔍 Verificando processos existentes...
tasklist /FI "WINDOWTITLE eq Agente Qualificador*" 2>nul | find /I "cmd.exe" >nul
if not errorlevel 1 (
    echo ⚠️  Sistema já está rodando!
    echo 📱 Frontend: http://localhost:3000
    echo 🔧 Backend: http://localhost:5000
    echo.
    pause
    exit /b 0
)

:: Verificar dependências críticas
echo 🔧 Verificando dependências...
where node >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js não encontrado!
    pause
    exit /b 1
)

where python >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    pause
    exit /b 1
)

:: Configurar variáveis de ambiente para performance
set FLASK_ENV=production
set NODE_ENV=production
set PYTHONUNBUFFERED=1
set PYTHONDONTWRITEBYTECODE=1

:: Copiar .env otimizado
echo 📋 Configurando ambiente...
if exist ".env.example" (
    copy /Y ".env.example" "backend\.env" >nul 2>&1
)

:: Inicializar backend otimizado
echo 🚀 Iniciando backend otimizado...
cd backend
start "Agente Qualificador - Backend OTIMIZADO" /MIN python main.py
cd ..

:: Aguardar backend (reduzido para 3 segundos)
echo ⏳ Aguardando backend (3s)...
timeout /t 3 /nobreak >nul

:: Verificar se backend está respondendo
echo 🔍 Testando backend...
curl -s http://localhost:5000/api/health >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Backend ainda inicializando...
    timeout /t 2 /nobreak >nul
)

:: Inicializar frontend otimizado
echo 🎨 Iniciando frontend otimizado...
cd frontend
start "Agente Qualificador - Frontend OTIMIZADO" /MIN npm run dev
cd ..

:: Aguardar frontend (reduzido para 5 segundos)
echo ⏳ Aguardando frontend (5s)...
timeout /t 5 /nobreak >nul

:: Verificar se frontend está respondendo
echo 🔍 Testando frontend...
curl -s http://localhost:3000 >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Frontend ainda inicializando...
    timeout /t 3 /nobreak >nul
)

echo.
echo ✅ SISTEMA OTIMIZADO INICIADO!
echo ================================
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:5000/api/health
echo 📊 Status:   http://localhost:5000/api/simulator/status
echo.
echo 🎯 CREDENCIAIS DE TESTE:
echo Email: eduspires123@gmail.com
echo Senha: 123456789
echo.
echo ⚡ Otimizações aplicadas:
echo   • Cache de inicialização
echo   • Lazy loading de módulos
echo   • Timeouts reduzidos
echo   • Logs minimizados
echo   • Verificação de processos
echo.
echo 💡 Para parar: Feche as janelas ou Ctrl+C
echo.

:: Abrir navegador automaticamente
timeout /t 2 /nobreak >nul
start http://localhost:3000

echo 🌟 Sistema pronto para uso!
pause



