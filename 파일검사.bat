@echo off
setlocal
chcp 65001 >nul
title ITR2 Quest Korean Patch
"%~dp0ITR2QuestPatch.exe" verify %*
set "patch_exit=%errorlevel%"
echo.
if not "%patch_exit%"=="0" echo 작업을 완료하지 못했습니다. 위 오류 메시지를 확인하세요.
pause
exit /b %patch_exit%
