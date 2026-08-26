import os

FEATURE_FLAGS = {
    "NEW_DASHBOARD_ENABLED": "NEW_DASHBOARD_ENABLED",
}


def _as_bool(value):
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def get_flag(name: str, default: bool = False) -> bool:
    if not name:
        raise ValueError("Feature flag name is required.")

    if name not in FEATURE_FLAGS:
        raise KeyError(f"Unknown feature flag: {name}")

    return _as_bool(os.getenv(name, str(default)))


def get_all_flags() -> dict[str, bool]:
    return {key: get_flag(key) for key in sorted(FEATURE_FLAGS)}
