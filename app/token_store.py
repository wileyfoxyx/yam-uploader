import os
import sys
import keyring
from keyring.errors import PasswordDeleteError
from typing import Optional

SERVICE_BASE = "yandex-music"
# For packaged builds, use a different service name so no old tokens are reused.
if getattr(sys, "frozen", False):
    default_service = f"{SERVICE_BASE}-release-1"
else:
    default_service = SERVICE_BASE
SERVICE_NAME = os.getenv("YM_KEYRING_SERVICE", default_service)
TOKEN_USERNAME = "access-token"


def get_token() -> Optional[str]:
    """Return token from OS keyring if exists, else None."""
    try:
        return keyring.get_password(SERVICE_NAME, TOKEN_USERNAME)
    except Exception:
        return None


essential_note = (
    "Token is stored in your OS keyring (service: 'yandex-music', user: 'access-token')."
)


def set_token(token: str) -> None:
    keyring.set_password(SERVICE_NAME, TOKEN_USERNAME, token)


def clear_token() -> None:
    try:
        keyring.delete_password(SERVICE_NAME, TOKEN_USERNAME)
    except PasswordDeleteError:
        pass
