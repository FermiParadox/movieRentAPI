import warnings
from typing import NoReturn


def _warn_no_secrets_file() -> NoReturn:
    warnings.warn(message="\nLoading secrets from config, instead of env-variables.\n"
                          "Make sure you've edit it. If already done, ignore this message.")


def mongo_db_link() -> str:
    try:
        from IGNORE_GIT_SECRETS import MONGODB_LINK
        return MONGODB_LINK
    except ImportError:
        _warn_no_secrets_file()
        from config import MONGO_DB_LINK
        return MONGO_DB_LINK
