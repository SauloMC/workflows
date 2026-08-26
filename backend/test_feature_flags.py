import os

from feature_flags import get_all_flags, get_flag


def test_new_dashboard_default_off():
    os.environ.pop("NEW_DASHBOARD_ENABLED", None)
    assert get_flag("NEW_DASHBOARD_ENABLED") is False


def test_new_dashboard_can_be_enabled_via_env():
    os.environ["NEW_DASHBOARD_ENABLED"] = "true"
    assert get_flag("NEW_DASHBOARD_ENABLED") is True
    os.environ.pop("NEW_DASHBOARD_ENABLED", None)


def test_get_all_flags_returns_expected_map():
    os.environ.pop("NEW_DASHBOARD_ENABLED", None)
    assert get_all_flags() == {"NEW_DASHBOARD_ENABLED": False}
