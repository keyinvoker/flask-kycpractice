from flask import Flask, render_template, make_response, request, redirect, abort
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

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/kycapp'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    ktp = db.Column(db.String(16), nullable=False)
    npwp = db.Column(db.String(20), nullable=False)
    is_email_verified = db.Column(db.Boolean, nullable=False, default=False)
    verified_at = db.Column(db.DateTime, nullable=True)
    expiration_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String, nullable=False, default='Unverified')

    def __repr__(self):
        return f"User { self.id }: ({ self.name })"

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

user_post_args = reqparse.RequestParser()
user_post_args.add_argument('name', type=str, help='your name', required=True)
user_post_args.add_argument('email', type=str, help='your email', required=True)
user_post_args.add_argument('phone', type=str, help='your phone', required=True)
user_post_args.add_argument('address', type=str, help='your address', required=True)
user_post_args.add_argument('salary', type=int, help='your salary', required=True)
user_post_args.add_argument('ktp', type=str, help='your KTP', required=True)
user_post_args.add_argument('npwp', type=str, help='your NPWP', required=True)

user_patch_args = reqparse.RequestParser()
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
    'verified_at': fields.DateTime,
    'expiration_date': DateFormat,
    'status': fields.String,
}

class IndexPage(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)
api.add_resource(IndexPage, '/')

class VerifyPage(Resource):
    def get(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('verify.html', user=user), 200, headers)
    
    @marshal_with(resource_fields)
    def patch(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        args = user_patch_args.parse_args()

        if not user:
            abort(404, message="User nonexistence!")

        if args['name']:
            user.name = args['name']
        if args['email']:
            user.email = args['email']
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
        user.last_verified = date.today()

        user.update()

        return user
api.add_resource(VerifyPage, '/verify/<int:user_id>')

class RegisterPage(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('register.html'), 200, headers)
        
    @marshal_with(resource_fields)
    def post(self):
        if request.headers['Content-Type'] == 'application/json':
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

class VerifyPage(Resource):
    def get(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('verify.html', user=user), 200, headers)
    
    @marshal_with(resource_fields)
    def patch(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        args = user_patch_args.parse_args()

        if not user:
            abort(404, message="User nonexistence!")

        if args['name']:
            user.name = args['name']
        if args['email']:
            user.email = args['email']
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
        user.last_verified = date.today()

        user.update()

        return user
api.add_resource(VerifyPage, '/verify/<int:user_id>')

# [EMAILING PROG]
def _get_expiration_date(date_string):
    last_verified = date_string.split('-')
    last_verified = [int(x) for x in last_verified]
    return date(last_verified[0], last_verified[1], last_verified[2])

class VerificationEmail(Resource):
    def get(self):
        load_dotenv(find_dotenv())
        sender = os.environ['SENDER']
        password = os.environ['PUSS']
        server = 'smtp.gmail.com'
        port = 465
        subject = '[@API-final-test] Annual Verification'
        em = EmailMessage()
        em['From'] = sender
        em['Subject'] = subject
        context = ssl.create_default_context()

        users = Users.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(users)
        for user in output:
            expiration_date = _get_expiration_date(user['last_verified'])
            verified_age = expiration_date + datetime.timedelta(days=365)
            if verified_age <= date.today():
                recipient = user['email']
                em['To'] = recipient
                body = f'''
                    <!DOCTYPE html>
                        <body>
                            <center>
                                <h2 style="color:maroon; font-family: Helvetica; text-decoration:underline;">Excel 'n Run</h2>
                                <img src="https://c.tenor.com/tCKYdE2gwlcAAAAi/spider-man-marvel-future-revolution.gif">
                                <h4>Please verify or update your account\'s credentials.</h4>
                                <br>
                                <form action="http://127.0.0.1:5000/verify/{ user['id'] }" method="GET">
                                    <input type="submit" value="VERIFY" class="btn" style="border: 1px solid darkgreen; color:whitesmoke; background-color:green;">
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
api.add_resource(VerificationEmail, '/mail')
# [EMAILING PROG - END]

if __name__ == '__main__':
    app.run(debug=True)