from email.message import EmailMessage
import ssl
import smtplib
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

sender = 'astrobattery100@gmail.com'
password = os.environ['PUSS']
recipient = 'gerav28131@pelung.com'
subject = '[KYC] Annual Verification'
body = 'Please verify or update your account\'s credentials.'
em = EmailMessage()
em['From'] = sender
em['To'] = recipient
em['subject'] = subject
em.set_content(body)

context = ssl.create_default_context()
server = 'smtp.gmail.com'
# server = '64.233.184.108'
port = 465
# port = 587

with smtplib.SMTP_SSL(server, port, context=context) as smtp:
    # smtp.starttls(context=context)
    smtp.login(sender, password)
    smtp.sendmail(sender, recipient, em.as_string())

# s = smtplib.SMTP_SSL('smtp.gmail.com')
# s.set_debuglevel(1)
# s.login(sender, password)

# s.sendmail(sender, recipient, em.as_string())
# s.quit()