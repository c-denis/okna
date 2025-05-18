import os
from dotenv import load_dotenv

load_dotenv()

class SecurityConfig:
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')