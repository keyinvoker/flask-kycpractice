class UpdateMailing(Resource):
    def get(self, user_id):
        subject = 'Update Verification'
        em['Subject'] = subject

        user = User.query.filter_by(id=user_id).first()
        recipient = user.email
        em['To'] = recipient
        body = f'''
                <center>
                    <img src="https://c.tenor.com/tCKYdE2gwlcAAAAi/spider-man-marvel-future-revolution.gif">
                    <h4>
                        <p>Please click VERIFY if you want to finalize your updates.</p>
                        <p>Click UPDATE if you want to update your data again.</p>
                    </h4>
                    <br>
                    <form action="http://127.0.0.1:5000/finalize/{ user.id }" method="POST">
                        <input type="submit" value="FINALIZE UPDATES" style="border: 1px solid darkgreen; color:whitesmoke; background-color:green;">
                    </form>
                    <br>
                    <form action="http://127.0.0.1:5000/update/{ user.id }" method="GET">
                        <input type="submit" value="UPDATE AGAIN" style="border: 1px solid maroon; color:whitesmoke; background-color:maroon;">
                    </form>
                </center>
                '''
        em.set_content(body, subtype='html')
        
        with smtplib.SMTP_SSL(server, port, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, recipient, em.as_string())
        del em['To']
        del em['Subject']