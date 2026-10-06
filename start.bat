@echo off
set "ROOT=%~dp0"
start "SmartERP Backend (SQLite local)" powershell -NoExit -Command "Set-Location '%ROOT%backend'; & '.\start_local.bat'"
start "SmartERP Frontend" powershell -NoExit -Command "Set-Location '%ROOT%frontend'; npm run dev"
