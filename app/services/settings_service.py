from typing import Dict, Any

_settings_db: Dict[str, Any] = {}


def save_settings(data: Dict[str, Any]):
    # Minimal in-memory persistence for demo/tests
    _settings_db.update(data)
    return _settings_db


def get_settings():
    return dict(_settings_db)
