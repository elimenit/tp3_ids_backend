from dotenv import load_dotenv
import os

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_NAME_DB = os.getenv('MYSQL_NAME_DB')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_HOST = os.getenv('MYSQL_HOST')
FLASK_HOST = os.getenv('FLASK_HOST')
FLASK_PORT = os.getenv('FLASK_PORT')
SECRET_KEY = os.getenv('SECRET_KEY')
