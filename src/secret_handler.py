import warnings
from typing import NoReturn


class MongoDBLink:
    def link(self) -> str:
        try:
            from IGNORE_GIT_SECRETS import MONGODB_LINK
            return MONGODB_LINK
        except ImportError:
            return self._warn_and_import_from_config()

    def _warn_and_import_from_config(self) -> str:
        self._warn_no_secrets_file()
        from config import MONGODB_LINK
        return MONGODB_LINK

    def _warn_no_secrets_file(self) -> NoReturn:
        warnings.warn(message="\nLoading secrets from config.py, instead of IGNORE_GIT_SECRETS.py.\n"
                              "Make sure you've edit it. If already done, ignore this message.")
