JWT_MIDDLEWARE_ACTIVE = True
# WARNING! Never upload secrets on GitHub
JWT_PRIVATE_KEY = "uhu498HSuhUWHBVWUJFa8Mlcoo"
JWT_SECRET_MESSAGE = 'some_stored_value_server-side'
JWT_ALGORITHM = "HS256"
JWT_DURATION_HOURS = 24 * 30

# Create an "IGNORE_GIT_SECRETS.py" file and place MONGODB_LINK there
# since that filename is ignored on git commits.

# Or edit this (WARNING: don't accidentally push it on GitHub)
MONGODB_LINK = 'not_real_link'
