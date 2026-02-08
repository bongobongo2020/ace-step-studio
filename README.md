# ACE-Step Studio

Local-first Suno-style music studio powered by ACE-Step 1.5.

> **Forked from** [roblaughter/ace-step-studio](https://github.com/roblaughter/ace-step-studio)

ACE-Step Studio uses:
- FastAPI backend for generation orchestration, model/runtime config, and API routes
- React + Vite frontend with one-page create/library/player workflow
- SQLite + filesystem storage for song metadata, audio, and cover assets
- Optional OpenAI-compatible endpoint support for prompt, lyrics, and title generation
- Optional local/remote cover-art generation providers (Fal, ComfyUI, A1111)

This project is designed for personal/self-hosted use and can run on macOS and Windows.

## Screenshot

![Custom mode UI](docs/images/custom-mode.png)

## Quick Install (UV)

The easiest way to get started is using [uv](https://github.com/astral-sh/uv), a fast Python package installer.

**Prerequisites:**
- Python 3.10+
- Node.js 18+ (for frontend)
- Git (for cloning ACE-Step-1.5 repo)

**Windows:**
```cmd
# Install uv (if not already installed)
pip install uv

# Run the installer - it will:
# - Clone ACE-Step-1.5 repo automatically
# - Create virtual environment
# - Install all dependencies
# - Download required AI models
# - Start the app
scripts\install_and_run.bat
```

**macOS/Linux:**
```bash
# Install uv (if not already installed)
pip install uv

# Clone ACE-Step-1.5 repo first
git clone https://github.com/ACE-Step/ACE-Step-1.5.git ../ACE-Step-1.5

# Create virtual environment and install dependencies
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Install frontend dependencies
cd ../frontend
npm install

# Start the app (see scripts/start.sh or scripts/start.bat)
```

**First run will download several GB of AI models automatically.**

## Installation

See the full step-by-step setup guide here: [docs/installation.md](./docs/installation.md)

## Repository Layout

```text
.
├── backend/        # FastAPI app, ACE-Step + LM services
├── docs/           # project docs and screenshots
├── frontend/       # Vite/React SPA (Suno-inspired UI)
├── scripts/        # install & start helpers
└── README.md
```

## Quick Start

**Easiest (Windows with uv):**
```cmd
scripts\install_and_run.bat
```

**macOS:**
```bash
./scripts/install_mac.sh
./scripts/start.sh
```

**Windows (manual):**
```powershell
./scripts/install_windows.ps1
./scripts/start.bat
```

Default ports:
- Backend: `8788`
- Frontend: `5175`

Port `8000` is intentionally avoided.

## Configuration Highlights

- `ACE_STEP_HOST` — bind address (set to your Tailscale IP to restrict access)
- `ACE_STEP_PORT` / `ACE_STEP_UI_PORT` — backend/frontend ports
- `ACE_STEP_ACE_REPO_PATH` / `ACE_STEP_CHECKPOINTS_PATH` — ACE repo and checkpoints locations
- `ACE_STEP_OPENAI_ENABLED` + `ACE_STEP_OPENAI_ENDPOINT` — OpenAI-compatible endpoint for prompt/lyrics/title tasks
- Filesystem storage rooted under `data/` (SQLite DB, runtime config, media folders)

Future ACE-Step modes (lego/extract/complete) already have UI placeholders to keep layout stable when the backend grows.
