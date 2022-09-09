# from app import db
from email.message import EmailMessage
import ssl
import smtplib
import os
from dotenv import load_dotenv, find_dotenv
import datetime
from datetime import date
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    db='kycapp',
)

def _get_send_date(last_verified):
    send_date = last_verified + datetime.timedelta(days=365)
    return send_date

mycursor = mydb.cursor()
mycursor.execute('SELECT * FROM users')



# [EMAILING PROGRAM]
load_dotenv(find_dotenv())
sender = 'astrobattery100@gmail.com'
password = os.environ['PUSS']
server = 'smtp.gmail.com'
port = 465

subject = '[@home] Annual Verification'
em = EmailMessage()
em['From'] = sender
em['Subject'] = subject

for user in mycursor:
    if _get_send_date(user[8]) <= date.today():
        recipient = user[2]
        em['To'] = recipient
        body = '''
               <!DOCTYPE html>
                <body>
                    <p>Please verify or update your account\'s credentials.</p>
                    <br>
                    <form action="http://127.0.0.1:5000/" method="GET">
                        <center>
                            <input type="submit" value="VERIFY" class="btn" style="border: 1px solid darkgreen; color:whitesmoke; background-color:green;">
                        </center>
                    </form>
                </body>
                </html>
               '''
        em.set_content(body, subtype='html')

        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL(server, port, context=context) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, recipient, em.as_string())
        del em['To']