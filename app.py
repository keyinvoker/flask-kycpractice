import datetime
from datetime import date
from flask import Flask, render_template, make_response, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv, find_dotenv
from email.message import EmailMessage
import ssl
import smtplib

from validator import RegisterSchemaValidator, UpdateSchemaValidator

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
    created_at = db.Column(db.DateTime, nullable=True) # TODO:created_at
    updated_at = db.Column(db.DateTime, nullable=True)
    is_email_verified = db.Column(db.Boolean, nullable=False, default=False)
    email_verified_at = db.Column(db.Date, nullable=True)
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
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'is_email_verified': fields.Boolean,
    'email_verified_at': DateFormat,
    'status': fields.String,
    'error_messages': fields.String
}

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
            _instance = RegisterSchemaValidator(response=data)
            response = _instance.isTrue()
            if len(response) > 0:
                error_messages = {
                    "error_messages": response
                }, 500
                return error_messages
            
            args = user_post_args.parse_args()
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

        new_user = Users(
            name=name,
            email=email,
            phone=phone,
            address=address,
            salary=salary,
            ktp=ktp,
            npwp=npwp,
            created_at = datetime.datetime.now(),
            updated_at = datetime.datetime.now(),
            is_email_verified=False,
            status='Pending',
        )

        new_user.save()
        # UpdateMailing.get(UpdateMailing, new_user.id)
        EmailVerificationMailing.get(EmailVerificationMailing, new_user.id)
        return new_user, 200
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

class UpdatePage(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        return user
    
    @marshal_with(resource_fields)
    def post(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User nonexistence!")

        # validation
        data = request.get_json()
        _instance = UpdateSchemaValidator(response=data)
        response = _instance.isTrue()
        if len(response) > 0:
            error_messages = {
                "error_messages": response
            }, 403
            return error_messages
        
        args = user_patch_args.parse_args()

        if args['name']:
            user.name = args['name']
        if args['email']:
            user.email = args['email']
            user.is_email_verified = False
            user.email_verified_at = None
            user.status = 'Pending'
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
        user.update()
        UpdateMailing.get(UpdateMailing, user_id)
        return user, 200
api.add_resource(UpdatePage, '/update/<int:user_id>')

class UpdateFinalizer(Resource):
    @marshal_with(resource_fields)
    def post(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        user.updated_at = datetime.datetime.now()

        if user.is_email_verified==True:
            user.status = 'Active'
        user.update()

        if user.is_email_verified==False:
            # user.status = 'Disabled'
            EmailVerificationMailing.get(EmailVerificationMailing, user.id)
        return user
api.add_resource(UpdateFinalizer, '/finalize/<int:user_id>')

class UpdateMailing(Resource):
    def get(self, user_id):
        subject = 'Update Verification'
        em['Subject'] = subject

        user = Users.query.filter_by(id=user_id).first()
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
            smtp.login(sender, password)
            smtp.sendmail(sender, recipient, em.as_string())
        del em['To']
        del em['Subject']
api.add_resource(UpdateMailing, '/mail/<int:user_id>')

class EmailVerification(Resource):
    @marshal_with(resource_fields)
    def post(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        user.is_email_verified = True
        user.email_verified_at = datetime.datetime.now()
        user.status = 'Active'
        user.update()
        return user
api.add_resource(EmailVerification, '/verify/<int:user_id>')

def _get_date(date_string):
    string_to_date = date_string.split('-')
    date_split = [int(x) for x in string_to_date]
    return date(date_split[0], date_split[1], date_split[2])

def _get_expiration_date(date_string):
    string_to_date = date_string.split('-')
    date_split = [int(x) for x in string_to_date]
    last_verified_at = date(date_split[0], date_split[1], date_split[2])
    expiration_date = last_verified_at + datetime.timedelta(days=334)
    return expiration_date

class AnnualMailing(Resource):
    def get(self):
        users = Users.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(users)
        for user in output:
            if not user['email_verified_at'] is None:
                expiration_date = _get_expiration_date(user['email_verified_at'])

                if expiration_date<=date.today() or user['is_email_verified']==False:
                    #
                    if user['is_email_verified']==True:
                        user['is_email_verified']==False

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
                        smtp.login(sender, password)
                        smtp.sendmail(sender, recipient, em.as_string())
                    del em['To']
                    del em['Subject']
api.add_resource(AnnualMailing, '/mail/unverified')

# TODO: mail per person to validate email if email updated:
# annual mailing but per one person or triggered by Update
class EmailVerificationMailing(Resource):
    def get(self, user_id):
        # TODO: use flag to indicate how many times user has been sent email
        # if flag==5 -> 'status': 'disabled'
        # OR not use flag: calculate 'updated_at' to date.today()
        # this should be scheduled to run everyday -> separate function to retrieve all() ?
        user = Users.query.filter_by(id=user_id).first()
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
                smtp.login(sender, password)
                smtp.sendmail(sender, recipient, em.as_string())
            del em['To']
            del em['Subject']

        elif diff==6:
            user.status = 'Disabled'
            user.update()
            return user
api.add_resource(EmailVerificationMailing, '/mail/unverified/<int:user_id>')

# TODO: class IndividualEmailVerificationMailing

if __name__ == '__main__':
    app.run(debug=True)