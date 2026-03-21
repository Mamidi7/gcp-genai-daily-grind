"""
Day 11 Solution: Files + JSON + Environment Variables
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
    errors: list[str] = []
    if "GCP_PROJECT_ID" not in os.environ:
        errors.append("GCP_PROJECT_ID is missing from environment")
    return errors


def load_runtime_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ValueError("Runtime config must be a JSON object")
    return payload


def build_safe_summary() -> dict:
    project_id = os.getenv("GCP_PROJECT_ID", "")
    location = os.getenv("GCP_LOCATION", "")
    creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    config_path = Path(os.getenv("APP_RUNTIME_CONFIG", str(DEFAULT_JSON_PATH)))

    runtime_config = load_runtime_json(config_path)
    env_errors = validate_required_env()

    return {
        "project_id": project_id or "not-set",
        "location": location or "not-set",
        "has_credentials_path": bool(creds),
        "credentials_path": mask_path(creds),
        "runtime_config_path": mask_path(str(config_path)),
        "runtime_config_loaded": bool(runtime_config),
        "runtime_config_keys": sorted(runtime_config.keys()),
        "runtime_profile": runtime_config.get("runtime_profile", "unknown"),
        "env_errors": env_errors,
    }


def validate_or_fail() -> dict:
    errors = validate_required_env()
    if errors:
        return {"status": "invalid", "error": errors[0]}
    return {"status": "valid"}


def main() -> None:
    print("=== Day 11 Solution ===")
    summary = build_safe_summary()
    print("Safe Summary:")
    print(json.dumps(summary, indent=2))
    print()
    print("Validation:")
    print(json.dumps(validate_or_fail(), indent=2))


if __name__ == "__main__":
    main()
