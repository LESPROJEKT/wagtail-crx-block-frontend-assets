from importlib.util import find_spec

from .base import *  # noqa: F401,F403

# Speed up tests and avoid filesystem writes.
DATABASES["default"]["NAME"] = ":memory:"

# Required for Wagtail admin staticfiles versioning.
SECRET_KEY = "test-secret-key"

# Wagtail 6 removed modeladmin; drop it when unavailable.
if not find_spec("wagtail.contrib.modeladmin"):
    INSTALLED_APPS = [
        app for app in INSTALLED_APPS if app != "wagtail.contrib.modeladmin"
    ]

# Keep caching simple for tests.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
