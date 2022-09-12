from flask import Flask, render_template, make_response, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with
import datetime
from datetime import date
from flask_marshmallow import Marshmallow
from email.message import EmailMessage
import ssl
import smtplib
import os
from dotenv import load_dotenv, find_dotenv
import re
import random

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/kyc'
db = SQLAlchemy(app)
ma = Marshmallow(app)

load_dotenv(find_dotenv())
sender = os.environ['SENDER']
password = os.environ['PUSS']
server = 'smtp.gmail.com'
port = 465
em = EmailMessage()
em['From'] = sender
context = ssl.create_default_context()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    ktp = db.Column(db.String(16), nullable=False)
    npwp = db.Column(db.String(20), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    is_email_verified = db.Column(db.Boolean, nullable=False, default=False)
    email_verified_at = db.Column(db.DateTime, nullable=True)
    expiration_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(255), nullable=False, default='Unverified')

    def __repr__(self):
        return f"User { self.id }:({ self.name }, { self.email })"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users

user_post_args = reqparse.RequestParser(bundle_errors=True)
user_post_args.add_argument('name', type=str, help='your name', required=True)
user_post_args.add_argument('email', type=str, help='your email', required=True)
user_post_args.add_argument('phone', type=str, help='your phone', required=True)
user_post_args.add_argument('address', type=str, help='your address', required=True)
user_post_args.add_argument('salary', type=int, help='your salary', required=True)
user_post_args.add_argument('ktp', type=str, help='your KTP', required=True)
user_post_args.add_argument('npwp', type=str, help='your NPWP', required=True)

user_patch_args = reqparse.RequestParser(bundle_errors=True)
user_patch_args.add_argument('name', type=str, help='your name')
user_patch_args.add_argument('email', type=str, help='your email')
user_patch_args.add_argument('phone', type=str, help='your phone')
user_patch_args.add_argument('address', type=str, help='your address')
user_patch_args.add_argument('salary', type=int, help='your salary')
user_patch_args.add_argument('ktp', type=str, help='your KTP')
user_patch_args.add_argument('npwp', type=str, help='your NPWP')

class DateFormat(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'address': fields.String,
    'salary': fields.Integer,
    'ktp': fields.String,
    'npwp': fields.String,
    'is_email_verified': fields.Boolean,
    'email_verified_at': fields.DateTime,
    'expiration_date': DateFormat,
    'status': fields.String,
    'error_message': fields.String
}

# VALIDATOR
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class UserSchemaValidator(object):
    def __init__(self, response={}):
        self.response = response

    def isTrue(self):
        error_messages = []

        try:
            name = self.response.get('name')
            if name is None or len(name)<=1:
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Field name is required!')
            
        try:
            email = self.response.get('email')
            if email is None or not re.fullmatch(regex, email):
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Field email has to be a valid email!')
        
        try:
            phone = self.response.get('phone', None)
            if phone is None or len(phone)<=1 or phone.isnumeric()==False:
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Field phone has to be a valid phone number!')
        
        try:
            address = self.response.get('address')
            if address is None or len(address)<=1:
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Field address is required!')
        
        try:
            salary = int(self.response.get('salary'))
            if salary is None or salary==0:
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Field salary is required!')
        
        try:
            ktp = self.response.get('ktp')
            if ktp is None or len(ktp)!=16 or ktp.isnumeric()==False:
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Field KTP has to be 16 digits!')
        
        try:
            npwp = self.response.get('npwp')
            if npwp is None or len(npwp)!=16 or npwp.isnumeric()==False:
                raise Exception('Error')
        except Exception as e:
            error_messages.append('Field NPWP has to be 16 digits!')

        return error_messages
        

class IndexPage(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)
api.add_resource(IndexPage, '/')

class RegisterPage(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('register.html'), 200, headers)
        
    @marshal_with(resource_fields)
    def post(self):
        if request.headers['Content-Type'] == 'application/json':
            # validation
            data = request.get_json()
            _instance = UserSchemaValidator(response=data)
            response = _instance.isTrue()
            if len(response) > 0:
                error_messages = {
                    "error_message": response
                }, 403
                return error_messages
            
            args = user_post_args.parse_args() # NOTE: type(args) = dict
            name = args['name']
            email = args['email']
            phone = args['phone']
            address = args['address']
            salary = args['salary']
            ktp = args['ktp']
            npwp = args['npwp']

        else:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            salary = request.form['salary']
            ktp = request.form['ktp']
            npwp = request.form['npwp']
        is_email_verified = False
        status = 'Unverified'

        new_user = Users(
            name=name,
            email=email,
            phone=phone,
            address=address,
            salary=salary,
            ktp=ktp,
            npwp=npwp,
            is_email_verified=is_email_verified,
            status=status,
        )

        new_user.save()

        return new_user
api.add_resource(RegisterPage, '/register')

class GetOne(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        return user
api.add_resource(GetOne, '/get/<int:user_id>')

class GetAll(Resource):
    def get(self):
        user = Users.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(user)
        return {'user': output}
api.add_resource(GetAll, "/get")



# def generateOTP():
#     return random.randrange(100000, 999999)

# class GetOTP(Resource):
#     def get(self, user_id):
#         user = Users.query.filter_by(id=user_id).first()
#         headers = {'Content-Type': 'text/html'}
#         return make_response(render_template('getotp.html', user=user), 200, headers)

#     def post(self, user_id):
        
#         pass
# api.add_resource('/getotp/<int:user_id>')

# class VerifyOTP(Resource):
#     def post(self, user_id):
#         user = Users.query.filter_by(id=user_id).first()
#         headers = {'Content-Type': 'text/html'}
#         return make_response(render_template('verifyotp.html', user=user), 200, headers)
# api.add_resource('/verifyotp/<int:user_id>')

class UpdatePage(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        # headers = {'Content-Type': 'text/html'}
        # return make_response(render_template('update.html', user=user), 200, headers)
        return user
    
    @marshal_with(resource_fields)
    def post(self, user_id):
        user = Users.query.filter_by(id=user_id).first()

        # validation
        data = request.get_json()
        _instance = UserSchemaValidator(response=data)
        response = _instance.isTrue()
        if len(response) > 0:
            error_messages = {
                "message": response
            }, 403
            return error_messages
        
        args = user_patch_args.parse_args()

        if not user:
            abort(404, message="User nonexistence!")

        if args['name']:
            user.name = args['name']
        if args['email']:
            user.email = args['email']
            user.is_email_verified = False
            user.email_verified_at = None
            user.expiration_date = None
            user.status = 'Unverified'
        if args['phone']:
            user.phone = args['phone']
        if args['address']:
            user.address = args['address']
        if args['salary']:
            user.salary = args['salary']
        if args['ktp']:
            user.ktp = args['ktp']
        if args['npwp']:
            user.npwp = args['npwp']
        
        # NOTE:
        # 1. store updated values
        # 2. send email # TODO
        # 3. if VERIFY, then apply update & 'updated_at' = datetime.datetime.now()
        # 4. else change nothing to DB
        
        user.update()
        UpdateMailing.get(UpdateMailing, user_id)

        return user
api.add_resource(UpdatePage, '/update/<int:user_id>')

class UpdateFinalizer(Resource):
    def post(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        user.updated_at = datetime.datetime.now()
api.add_resource(UpdateFinalizer, '/finalize/<int:user_id>')

class UpdateMailing(Resource):
    def get(self, user_id):
        subject = 'Update Verification'
        em['Subject'] = subject

        user = Users.query.filter_by(id=user_id).first()
        recipient = user.email
        em['To'] = recipient
        body = f'''
            <!DOCTYPE html>
                <body>
                    <center>
                        <img src="https://c.tenor.com/tCKYdE2gwlcAAAAi/spider-man-marvel-future-revolution.gif">
                        <h4>
                            <p>Please click VERIFY to verify your updates.</p>
                            <p>If not, you can ignore this email.</p>
                        </h4>
                        <br>
                        <form action="http://127.0.0.1:5000/verify/{ user.id }" method="POST">
                            <input type="submit" value="VERIFY" style="border: 1px solid darkgreen; color:whitesmoke; background-color:green;">
                        </form>
                        <br>
                        <form action="http://127.0.0.1:5000/update/{ user.id }" method="GET">
                            <input type="submit" value="UPDATE" style="border: 1px solid maroon; color:whitesmoke; background-color:maroon;">
                        </form>
                    </center>
                </body>
            </html>
            '''
        em.set_content(body, subtype='html')
        
        with smtplib.SMTP_SSL(server, port, context=context) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, recipient, em.as_string())
        del em['To']
        del em['Subject']

    # def post(self, user_id):
    #     pass
        # user.updated_at = datetime.datetime.now()
        # user.update()
api.add_resource(UpdateMailing, '/mail/<int:user_id>')




    
class EmailVerification(Resource):
    @marshal_with(resource_fields)
    def post(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        user.is_email_verified = True
        user.email_verified_at = datetime.datetime.now()
        user.expiration_date = user.email_verified_at + datetime.timedelta(days=334)
        # TODO: get verification status of phone + IF
        user.status = 'Verified'
        user.update()
        return user
api.add_resource(EmailVerification, '/verify/<int:user_id>')

def _get_expiration_date(date_string):
    expiration_date = date_string.split('-')
    expiration_date = [int(x) for x in expiration_date]
    return date(expiration_date[0], expiration_date[1], expiration_date[2])

class ScheduledMailing(Resource):
    def get(self):
        em['Subject'] = subject

        users = Users.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(users)
        for user in output:
            subject = 'Account Verification'
            if user['expiration_date'] is not None:
                expiration_date = _get_expiration_date(user['expiration_date'])
            else:
                expiration_date = date.today()

            if (expiration_date is not None and expiration_date<=date.today()) or user['is_email_verified']==False:
                recipient = user['email']
                em['To'] = recipient
                body = f'''
                    <!DOCTYPE html>
                        <body>
                            <center>
                                <img src="https://c.tenor.com/tCKYdE2gwlcAAAAi/spider-man-marvel-future-revolution.gif">
                                <h4>
                                    <p>Please click VERIFY to verify your email and finalize the updates.</p>
                                    <p>Or click the UPDATE to update the data again.</p>
                                </h4>
                                <br>
                                <form action="http://127.0.0.1:5000/verify/{ user['id'] }" method="POST">
                                    <input type="submit" value="VERIFY" style="border: 1px solid darkgreen; color:whitesmoke; background-color:green;">
                                </form>
                                <br>
                                <form action="http://127.0.0.1:5000/update/{ user['id'] }" method="GET">
                                    <input type="submit" value="UPDATE" style="border: 1px solid maroon; color:whitesmoke; background-color:maroon;">
                                </form>
                            </center>
                        </body>
                    </html>
                    '''
                em.set_content(body, subtype='html')
                
                with smtplib.SMTP_SSL(server, port, context=context) as smtp:
                    smtp.login(sender, password)
                    smtp.sendmail(sender, recipient, em.as_string())
                del em['To']
                del em['Subject']
api.add_resource(ScheduledMailing, '/mail/all')

if __name__ == '__main__':
    app.run(debug=True)