@echo off
echo ========================================
echo   AGENTE QUALIFICADOR IA - INICIALIZAR
echo ========================================
echo.

echo [1/4] Verificando dependencias Python...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias Python
    pause
    exit /b 1
)

echo.
echo [2/4] Verificando dependencias Node.js...
cd ..\frontend
call npm install
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias Node.js
    pause
    exit /b 1
)

echo.
echo [3/4] Copiando configurações e iniciando Backend Flask...
cd ..
copy ".env.local.backend" "backend\.env"
cd backend
start "Backend Flask" cmd /k "python app.py"
timeout /t 5

echo.
echo [4/4] Copiando configurações e iniciando Frontend Next.js...
copy ".env.local.frontend" "frontend\.env.local"
cd frontend
start "Frontend Next.js" cmd /k "npm run dev"

echo.
echo ========================================
echo   SISTEMA INICIADO COM SUCESSO!
echo ========================================
echo.
echo URLs Disponiveis:
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:5000
echo.
echo Credenciais Demo:
echo   Email: admin@demo.com
echo   Senha: demo123
echo.
echo Pressione qualquer tecla para continuar...
pause > nul

