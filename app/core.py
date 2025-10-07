import os
SECRET_KEY = os.getenv('SECRET_KEY', 'supersecret')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60*24))


# Default single admin (used when single-admin mode)
import os
DEFAULT_ADMIN_USERNAME = os.getenv('DEFAULT_ADMIN_USERNAME', 'admin')
DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_PASSWORD', '1234')
DEFAULT_ADMIN_FULLNAME = os.getenv('DEFAULT_ADMIN_FULLNAME', 'Administrator')
