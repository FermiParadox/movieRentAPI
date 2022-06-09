import os


def _password() -> str:
    return os.environ.get('MONGODB_MOVIES_USER0_PASS')


def _create_mongodb_link(password: str) -> str:
    return f'mongodb+srv://user0:{password}@cluster0.wa4gd.mongodb.net/?retryWrites=true&w=majority'


MONGODB_LINK = _create_mongodb_link(password=_password())
