import os

PASS_ENV_VAR = 'MONGODB_MOVIES_USER0_PASS'


def fallback_db_password():
    from config import MONGO_DB_PASSWORD

    print("""\n\nWARNING: Secrets NOT stored on Git (DB link, api-key, etc.). 
        Using default (wrong) values from configuration file.

        Please edit the configuration file manually. 
        If already done, ignore this message.""")
    return MONGO_DB_PASSWORD


def password(env_var: str) -> str:
    val = os.environ.get(env_var)
    if not val:
        return fallback_db_password()
    return val


def _create_mongodb_link(password_: str) -> str:
    return f'mongodb+srv://user0:{password_}@cluster0.wa4gd.mongodb.net/?retryWrites=true&w=majority'


def mongo_db_link() -> str:
    mongodb_user0_pass = password(PASS_ENV_VAR)
    return _create_mongodb_link(password_=mongodb_user0_pass)
