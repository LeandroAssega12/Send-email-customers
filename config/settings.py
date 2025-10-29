from dotenv import load_dotenv
import os

load_dotenv()

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT'))
SSH_USER = os.getenv('SSH_USER')
SSH_PASSWORD = os.getenv('SSH_PASSWORD')

OUTLOOK_EMAIL = os.getenv('OUTLOOK_EMAIL')
OUTLOOK_PASSWORD = os.getenv('OUTLOOK_PASSWORD')

SQL_SERVER=os.getenv('SQL_SERVER')
SQL_DATABASE=os.getenv('SQL_DATABASE')
SQL_USERNAME=os.getenv('SQL_USERNAME')
SQL_PASSWORD=os.getenv('SQL_PASSWORD')