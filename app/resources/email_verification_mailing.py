# TODO: mail per person to validate email if email updated:
# annual mailing but per one person or triggered by Update
class EmailVerificationMailing(Resource):
    def get(self, user_id):
        # TODO: use flag to indicate how many times user has been sent email
        # if flag==5 -> 'status': 'disabled'
        # OR not use flag: calculate 'updated_at' to date.today()
        # this should be scheduled to run everyday -> separate function to retrieve all() ?
        user = User.query.filter_by(id=user_id).first()
        diff = date.today() - _get_date(user.updated_at.strftime('%Y-%m-%d'))
        if diff<=datetime.timedelta(5):
            recipient = user.email
            subject = 'Email Verification'
            em['To'] = recipient
            em['Subject'] = subject
            body = f'''
                    <center>
                        <img src="https://c.tenor.com/tCKYdE2gwlcAAAAi/spider-man-marvel-future-revolution.gif">
                        <h4>
                            <p>Please click VERIFY to verify your email and finalize the updates.</p>
                            <p>Click the UPDATE to update the data again.</p>
                        </h4>
                        <br>
                        <form action="http://127.0.0.1:5000/verify/{ user.id }" method="POST">
                            <input type="submit" value="VERIFY EMAIL" style="border: 1px solid darkgreen; color:whitesmoke; background-color:green;">
                        </form>
                        <br>
                        <form action="http://127.0.0.1:5000/update/{ user.id }" method="GET">
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

        elif diff==6:
            user.status = 'Disabled'
            user.update()
            return user