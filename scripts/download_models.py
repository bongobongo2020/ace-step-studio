#!/usr/bin/env python3
"""
Download required ACE-Step models using Hugging Face Hub.
This script downloads the default models needed for the app to function.
"""

import sys
import time
from pathlib import Path

# Add backend to path so we can import the model manager
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.services.model_manager import (
    download_model,
    list_models,
    MODEL_SPECS,
)
from app.config import settings


def print_status(message: str):
    print(f"[INFO] {message}")


def print_error(message: str):
    print(f"[ERROR] {message}", file=sys.stderr)


def check_and_download_model(model_id: str, silent: bool = False) -> bool:
    """Check if a model exists, download if missing."""
    if model_id not in MODEL_SPECS:
        print_error(f"Unknown model ID: {model_id}")
        return False

    spec = MODEL_SPECS[model_id]
    local_path = spec.local_path

    # Check if model already exists
    if local_path.exists() and any(local_path.iterdir()):
        if not silent:
            print_status(f"Model '{spec.display_name}' already exists - skipping download")
        return True

    if silent:
        print_status(f"Downloading model '{spec.display_name}' from {spec.repo_id}...")
    else:
        print_status(f"Downloading model '{spec.display_name}' from {spec.repo_id}...")
        print_status(f"  Target: {local_path}")

    try:
        download_model(model_id)

        # Wait for download to complete (it runs in a thread)
        from app.services.model_manager import download_state
        max_wait = 600  # 10 minutes max
        waited = 0
        while waited < max_wait:
            state_info = download_state.get(model_id)
            state = state_info.get("state")
            if state == "completed":
                print_status(f"Download complete: '{spec.display_name}'")
                return True
            elif state == "error":
                error = state_info.get("error", "Unknown error")
                print_error(f"Download failed: {error}")
                return False
            elif state == "idle" or state == "downloading":
                time.sleep(2)
                waited += 2
                if waited % 10 == 0:
                    print_status(f"  Still downloading... ({waited}s)")

        print_error(f"Download timed out after {max_wait}s")
        return False

    except Exception as e:
        print_error(f"Failed to download model: {e}")
        return False


def main():
    # Check if we're running in silent mode (all models exist)
    silent_mode = True
    for model_id, _ in [("dit-turbo", ""), ("lm-0.6b", "")]:
        spec = MODEL_SPECS[model_id]
        if not (spec.local_path.exists() and any(spec.local_path.iterdir())):
            silent_mode = False
            break

    if silent_mode:
        print_status("All models already downloaded. Ready to run!")
        return 0

    print_status("ACE-Step Model Downloader")
    print_status("=" * 40)

    # Ensure checkpoints directory exists
    settings.checkpoints_path.mkdir(parents=True, exist_ok=True)

    # Models to download: default DiT and default LM
    models_to_download = [
        ("dit-turbo", "Main music generation model"),
        ("lm-0.6b", "Language model for prompts/lyrics"),
    ]

    success_count = 0
    for model_id, description in models_to_download:
        print()
        print_status(f"Checking: {description} ({model_id})")
        if check_and_download_model(model_id, silent=False):
            success_count += 1

    print()
    print_status("=" * 40)
    print_status(f"Download summary: {success_count}/{len(models_to_download)} models ready")

    # List all models and their status
    print()
    print_status("Current model status:")
    all_models = list_models()
    for model in all_models:
        status_symbol = {
            "available": "[OK]",
            "missing": "[--]",
            "downloading": "[...]",
            "error": "[!!]",
        }.get(model["status"], "[?]")
        print(f"  {status_symbol} {model['display_name']:15} - {model['status']}")

    if success_count == len(models_to_download):
        print()
        print_status("All required models are ready!")
        return 0
    else:
        print()
        print_error("Some models failed to download. The app may not work correctly.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
