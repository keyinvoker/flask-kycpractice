from datetime import date
import smtplib

from flask_restful import Resource

from app.config import em
from app.models.user import User
from app.schemas.user_schema import UserSchema
from app.utils.time_calculator import _get_expiration_date


class AnnualMailing(Resource):
    def get(self):
        users = User.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(users)
        for user in output:
            if not user['email_verified_at'] is None:
                expiration_date = _get_expiration_date(user['email_verified_at'])

                if (
                    expiration_date <= date.today()
                    or user['is_email_verified'] is False
                ):
                    if user['is_email_verified'] is True:
                        user['is_email_verified'] is False

                    recipient = user['email']
                    subject = 'Annual Verification'
                    em['To'] = recipient
                    em['Subject'] = subject
                    body = f'''
                            <center>
                                <img src="https://c.tenor.com/tCKYdE2gwlcAAAAi/spider-man-marvel-future-revolution.gif">
                                <h4>
                                    <p>Please VERIFY your credentials to continue using our services.</p>
                                    <p>Or click the UPDATE to change your data.</p>
                                </h4>
                                <br>
                                <form action="http://127.0.0.1:5000/verify/{ user['id'] }" method="POST">
                                    <input type="submit" value="VERIFY NOW" style="border: 1px solid darkgreen; color:whitesmoke; background-color:green;">
                                </form>
                                <br>
                                <form action="http://127.0.0.1:5000/update/{ user['id'] }" method="GET">
                                    <input type="submit" value="UPDATE DATA" style="border: 1px solid maroon; color:whitesmoke; background-color:maroon;">
                                </form>
                            </center>
                            '''
                    em.set_content(body, subtype='html')
                    
                    with smtplib.SMTP_SSL(server, port, context=context) as smtp:
                        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                        smtp.sendmail(EMAIL_SENDER, recipient, em.as_string())
                    del em['To']
                    del em['Subject']