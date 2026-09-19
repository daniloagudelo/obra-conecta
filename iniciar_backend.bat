@echo off
title OBRA CONECTA - BACKEND (no cierres esta ventana mientras uses el sitio)
cd /d "%~dp0backend"
call venv\Scripts\activate
echo.
echo ============================================================
echo  BACKEND de Obra Conecta iniciando...
echo  NO CIERRES ESTA VENTANA mientras uses la pagina.
echo  Para apagarlo, cierra esta ventana o presiona Ctrl+C.
echo ============================================================
echo.
uvicorn app.main:app --reload
pause
