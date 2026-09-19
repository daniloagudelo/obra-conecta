@echo off
title OBRA CONECTA - FRONTEND (no cierres esta ventana mientras uses el sitio)
cd /d "%~dp0frontend"
echo.
echo ============================================================
echo  FRONTEND de Obra Conecta iniciando...
echo  Antes de esto, el BACKEND ya debe estar corriendo
echo  (usa primero iniciar_backend.bat).
echo  NO CIERRES ESTA VENTANA mientras uses la pagina.
echo ============================================================
echo.
npm run dev
pause
