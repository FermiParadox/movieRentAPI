import os

PASSWORD = os.environ.get('MONGODB_MOVIES_USER0_PASS')
MONGODB_LINK = f'mongodb+srv://user0:{PASSWORD}@cluster0.wa4gd.mongodb.net/?retryWrites=true&w=majority'
