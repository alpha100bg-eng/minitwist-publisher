@echo off
REM Demonstration filmee pour l'audit YouTube API.
REM Enchaine les etapes dans l'ordre attendu par les examinateurs :
REM file d'attente -> autorisation OAuth -> envoi -> file d'attente.
setlocal
cd /d "%~dp0.."
set PYTHONPATH=src
set PY=.venv\Scripts\python.exe

echo.
echo ================================================================
echo  MINI TWIST Publisher - demonstration
echo ================================================================
echo.
echo [1/4] File d'attente avant envoi
echo ----------------------------------------------------------------
"%PY%" -m minitwist_publisher status
echo.
pause

echo.
echo [2/4] Autorisation Google (OAuth)
echo  -^> le navigateur va s'ouvrir : clique sur Autoriser
echo ----------------------------------------------------------------
"%PY%" -u -m minitwist_publisher authorize
echo.
pause

echo.
echo [3/4] Envoi de la prochaine video en attente
echo ----------------------------------------------------------------
"%PY%" -u -m minitwist_publisher upload-next
echo.
pause

echo.
echo [4/4] File d'attente apres envoi
echo ----------------------------------------------------------------
"%PY%" -m minitwist_publisher status
echo.
echo Demonstration terminee. Tu peux arreter l'enregistrement.
pause
