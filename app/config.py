from email.message import EmailMessage
import os
from dotenv import find_dotenv, load_dotenv
import ssl

load_dotenv(find_dotenv())

EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_SERVER = os.environ.get('EMAIL_SERVER')
EMAIL_PORT = os.environ.get('EMAIL_PORT')

em = EmailMessage()
em['From'] = EMAIL_SENDER
context = ssl.create_default_context()
