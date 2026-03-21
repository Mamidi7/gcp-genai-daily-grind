"""
Day 11 Exercises: Files + JSON + Environment Variables

Goal: Fill TODO blocks and run this file.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_JSON_PATH = BASE_DIR / "config/runtime_profile.json"


def mask_path(path_value: str) -> str:
    if not path_value:
        return "not-set"
    return f".../{Path(path_value).name}"


def validate_required_env() -> list[str]:
    """TODO: Check only GCP_PROJECT_ID and return error list."""
    errors: list[str] = []
    # TODO-1: add validation for required env key
    return errors


def load_runtime_json(path: Path) -> dict:
    """TODO: Load JSON file and ensure object type."""
    # TODO-2: open file and json.load
    # TODO-3: ensure loaded value is dict, else raise ValueError
    return {}


def build_safe_summary() -> dict:
    project_id = os.getenv("GCP_PROJECT_ID", "")
    location = os.getenv("GCP_LOCATION", "")
    creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    config_path = Path(os.getenv("APP_RUNTIME_CONFIG", str(DEFAULT_JSON_PATH)))

    runtime_config = load_runtime_json(config_path)
    env_errors = validate_required_env()

    summary = {
        "project_id": project_id or "not-set",
        "location": location or "not-set",
        "has_credentials_path": bool(creds),
        "credentials_path": mask_path(creds),
        "runtime_config_loaded": bool(runtime_config),
        "runtime_config_keys": sorted(runtime_config.keys()),
        "runtime_profile": runtime_config.get("runtime_profile", "unknown"),
        "env_errors": env_errors,
    }
    return summary


def main() -> None:
    print("=== Day 11 Exercises ===")
    print("Step 1: Fill TODOs in validate_required_env and load_runtime_json")
    print("Step 2: Run again and verify safe output")
    print()

    try:
        summary = build_safe_summary()
        print("Safe Config Summary:")
        print(json.dumps(summary, indent=2))
    except Exception as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
