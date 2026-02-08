@echo off
setlocal

set "ROOT_DIR=%~dp0.."
for %%I in ("%ROOT_DIR%") do set "ROOT_DIR=%%~fI"
set "BACKEND_DIR=%ROOT_DIR%\backend"
set "ACE_REPO_DIR=%ROOT_DIR%\ACE-Step-1.5"

echo ========================================
echo ACE-Step Studio - UV Install and Run
echo ========================================
echo.

:: Check if uv is installed
where uv >nul 2>nul
if errorlevel 1 (
  echo [ERROR] uv is not installed or not in PATH
  echo Please install uv first: https://github.com/astral-sh/uv
  echo Or run: pip install uv
  exit /b 1
)

:: Check for Node.js
where npm >nul 2>nul
if errorlevel 1 (
  echo [WARNING] npm is not available in PATH
  echo Install Node.js for full functionality
  echo.
)

:: Check for git
where git >nul 2>nul
if errorlevel 1 (
  echo [WARNING] git is not available in PATH
  echo ACE-Step-1.5 repo will not be cloned automatically
  echo.
)

:: Set default environment variables if not defined
if not defined ACE_STEP_PORT set "ACE_STEP_PORT=8788"
if not defined ACE_STEP_UI_PORT set "ACE_STEP_UI_PORT=5175"
if not defined ACE_STEP_HOST set "ACE_STEP_HOST=0.0.0.0"
if not defined ACE_STEP_ACE_REPO_PATH set "ACE_STEP_ACE_REPO_PATH=%ACE_REPO_DIR%"

:: Check if ACE-Step-1.5 repo exists, clone and sync if missing
where git >nul 2>nul
if not errorlevel 1 (
  if not exist "%ACE_REPO_DIR%\.git" (
    :: Remove existing directory if it exists but isn't a git repo
    if exist "%ACE_REPO_DIR%" (
      echo [INFO] Removing invalid ACE-Step-1.5 directory...
      rmdir /s /q "%ACE_REPO_DIR%" 2>nul
    )
    echo [INFO] ACE-Step-1.5 repo not found. Cloning from GitHub...
    echo   This may take a while...
    git clone https://github.com/ACE-Step/ACE-Step-1.5.git "%ACE_REPO_DIR%"
    if errorlevel 1 (
      echo [WARNING] Failed to clone ACE-Step-1.5 repo
      echo   Some features may not work correctly
    )
  )
) else (
  echo [WARNING] git not found - skipping ACE-Step-1.5 repo clone
)

:: Check if venv already exists
if exist "%BACKEND_DIR%\.venv\Scripts\python.exe" (
  echo [INFO] Virtual environment already exists.
  echo [INFO] Checking if ACE-Step-1.5 package is installed...
  "%BACKEND_DIR%\.venv\Scripts\python.exe" -c "import acestep" >nul 2>nul
  if errorlevel 1 (
    echo [INFO] ACE-Step-1.5 package not installed, installing now...
    if exist "%ACE_STEP_ACE_REPO_PATH%" (
      uv pip install -e "%ACE_STEP_ACE_REPO_PATH%" --python "%BACKEND_DIR%\.venv\Scripts\python.exe"
    )
  )
  goto :run_app
)

echo ========================================
echo First-time setup - Installing dependencies
echo ========================================
echo.

echo [1/4] Creating UV virtual environment...
uv venv "%BACKEND_DIR%\.venv"
if errorlevel 1 (
  echo [ERROR] Failed to create virtual environment
  exit /b 1
)

echo.
echo [2/4] Installing backend dependencies (pyproject.toml)...
uv pip install -e "%BACKEND_DIR%" --python "%BACKEND_DIR%\.venv\Scripts\python.exe"
if errorlevel 1 (
  echo [ERROR] Failed to install backend dependencies
  exit /b 1
)

echo.
echo [3/4] Installing ACE-Step-1.5 package...
if exist "%ACE_STEP_ACE_REPO_PATH%" (
  uv pip install -e "%ACE_STEP_ACE_REPO_PATH%" --python "%BACKEND_DIR%\.venv\Scripts\python.exe"
) else (
  echo [WARNING] ACE-Step-1.5 directory not found at: %ACE_STEP_ACE_REPO_PATH%
  echo Some features may not work correctly
)

echo.
echo [4/4] Installing frontend dependencies...
if exist "%ROOT_DIR%\frontend\package.json" (
  cd /d "%ROOT_DIR%\frontend"
  call npm install
  if errorlevel 1 (
    echo [WARNING] Failed to install frontend dependencies
  )
  cd /d "%ROOT_DIR%"
) else (
  echo [WARNING] Frontend package.json not found
)

echo.
echo Setup complete!
echo.

:run_app
echo ========================================
echo Starting application...
echo ========================================
echo.

echo [Checking] Required AI models...
"%BACKEND_DIR%\.venv\Scripts\python.exe" "%ROOT_DIR%\scripts\download_models.py"
if errorlevel 1 (
  echo [WARNING] Model download encountered issues. The app may not work correctly.
)

echo.
echo.
echo ========================================
echo Configuration:
echo   Backend:  http://%ACE_STEP_HOST%:%ACE_STEP_PORT%
echo   Frontend: http://localhost:%ACE_STEP_UI_PORT%
echo ========================================
echo.

:: Start backend
start "ACE Backend" cmd /k "cd /d "%ROOT_DIR%" && "%BACKEND_DIR%\.venv\Scripts\python.exe" -m uvicorn app.main:app --app-dir backend --host %ACE_STEP_HOST% --port %ACE_STEP_PORT%"

:: Start frontend (if npm is available)
where npm >nul 2>nul
if not errorlevel 1 (
  start "ACE Frontend" cmd /k "cd /d "%ROOT_DIR%\frontend" && npm run dev -- --host %ACE_STEP_HOST% --port %ACE_STEP_UI_PORT%"
)

echo.
echo Installation complete. Application starting...
echo Press any key to close this window (servers will continue running)
pause >nul

exit /b 0
