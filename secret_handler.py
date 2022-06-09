import os

PASS_ENV_VAR = 'MONGODB_MOVIES_USER0_PASS'


def password(env_var) -> str:
    val = os.environ.get(env_var)
    if not val:
        raise ValueError("You haven't set the password environment variable.")
    return val


def _create_mongodb_link(password_: str) -> str:
    return f'mongodb+srv://user0:{password_}@cluster0.wa4gd.mongodb.net/?retryWrites=true&w=majority'


def mongo_db_link():
    mongodb_user0_pass = password(PASS_ENV_VAR)
    return _create_mongodb_link(password_=mongodb_user0_pass)
