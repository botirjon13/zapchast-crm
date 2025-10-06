import os
SECRET_KEY = os.getenv('SECRET_KEY', 'supersecret')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60*24))
