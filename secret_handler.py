import warnings
from typing import NoReturn


def mongo_db_link() -> str:
    try:
        from IGNORE_GIT_SECRETS import MONGODB_LINK
        return MONGODB_LINK
    except ImportError:
        return warn_and_import_from_config()


def warn_and_import_from_config():
    _warn_no_secrets_file()
    from config import MONGO_DB_LINK
    return MONGO_DB_LINK


def _warn_no_secrets_file() -> NoReturn:
    warnings.warn(message="\nLoading secrets from config.py, instead of IGNORE_GIT_SECRETS.py.\n"
                          "Make sure you've edit it. If already done, ignore this message.")
