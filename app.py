from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
import datetime
from datetime import date
from flask_marshmallow import Marshmallow
from http import HTTPStatus

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/kycapp'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# class HelloWorld(Resource):
#     def get(self):
#         return {'get': 'HelloWORLD GET!'}

#     def post(self):
#         return {'post': 'HelloWORLD POST!'}

#     def get(self, name):
#         return {'name': name}

# api.add_resource(HelloWorld, "/helloworld/<string:name>")

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    ktp = db.Column(db.String(16), nullable=False)
    npwp = db.Column(db.String(20), nullable=False)
    last_verified = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"Users (name = {self.name})"

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

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         address = request.form['address']
#         salary = request.form['salary']
#         ktp = request.form['ktp']
#         npwp = request.form['npwp']
#         last_verified = date.today()

#         new_user = Users(
#             name=name,
#             email=email,
#             phone=phone,
#             address=address,
#             salary=salary,
#             ktp=ktp,
#             npwp=npwp,
#             last_verified = last_verified,
#         )

#         try:
#             db.session.add(new_user)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'Failed adding user!'
#     else:
#         return render_template('register.html')

@app.route('/verify/<int:id>', methods=['POST', 'GET'])
def verify(id):
    user = Users.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.address = request.form['address']
        user.salary = request.form['salary']
        user.ktp = request.form['ktp']
        user.npwp = request.form['npwp']
        user.last_verified = date.today()
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Failed updating user!'
    else:
        return render_template('verify.html', user=user)

# @app.route('/get')
# def get():
#     user = Users.query.all()
#     user_schema = UserSchema(many=True)
#     output = user_schema.dump(user)
#     return {'user': output}



# [using flask_restful.Resource] 👆

user_post_args = reqparse.RequestParser()
user_post_args.add_argument('name', type=str, help='your name', required=True)
user_post_args.add_argument('email', type=str, help='your email', required=True)
user_post_args.add_argument('phone', type=str, help='your phone', required=True)
user_post_args.add_argument('address', type=str, help='your address', required=True)
user_post_args.add_argument('salary', type=int, help='your salary', required=True)
user_post_args.add_argument('ktp', type=str, help='your KTP', required=True)
user_post_args.add_argument('npwp', type=str, help='your NPWP', required=True)

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
    'last_verified': DateFormat,
}

class RegisterUser(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = user_post_args.parse_args()
        name = args['name']
        email = args['email']
        phone = args['phone']
        address = args['address']
        salary = args['salary']
        ktp = args['ktp']
        npwp = args['npwp']
        last_verified = date.today()

        new_user = Users(
            name=name,
            email=email,
            phone=phone,
            address=address,
            salary=salary,
            ktp=ktp,
            npwp=npwp,
            last_verified = last_verified,
        )

        new_user.save()
        return new_user
api.add_resource(RegisterUser, '/register')

# user_patch_args = reqparse.RequestParser()
# user_patch_args.add_argument('name', type=str, help='your name')
# user_patch_args.add_argument('email', type=str, help='your email')
# user_patch_args.add_argument('phone', type=str, help='your phone')
# user_patch_args.add_argument('address', type=str, help='your address')
# user_patch_args.add_argument('salary', type=int, help='your salary')
# user_patch_args.add_argument('ktp', type=str, help='your KTP')
# user_patch_args.add_argument('npwp', type=str, help='your NPWP')

class VerifyUser(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        return user

#     @marshal_with(resource_fields)
#     def post(self, user_id):
#         user = Users.query.filter_by(id=user_id).first()
#         args = user_post_args.parse_args()

#         if not user:
#             abort(404, message="nonexistence")

#         if args['name']:
#             user.name = args['name']
#         if args['email']:
#             user.email = args['email']
#         if args['phone']:
#             user.phone = args['phone']
#         if args['address']:
#             user.address = args['address']
#         if args['salary']:
#             user.salary = args['salary']
#         if args['ktp']:
#             user.ktp = args['ktp']
#         if args['npwp']:
#             user.npwp = args['npwp']
#         user.last_verified = date.today()

#         user.update()

#         return user

api.add_resource(VerifyUser, '/verify-user/<int:user_id>')

class GetAll(Resource):
    def get(self):
        user = Users.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(user)
        return {'user': output}
api.add_resource(GetAll, "/get")
# [using flask_restful.Resource - END]


# [EMAILING PROG]
from email.message import EmailMessage
import ssl
import smtplib
import os
from dotenv import load_dotenv, find_dotenv

# import mysql.connector
# mycursor = db.cursor()
# mycursor.execute('SELECT * FROM users')

load_dotenv(find_dotenv())
sender = 'astrobattery100@gmail.com'
password = os.environ['PUSS']
server = 'smtp.gmail.com'
port = 465
subject = '[@API-test-marshall] Annual Verification'
em = EmailMessage()
em['From'] = sender
em['Subject'] = subject

def _get_expiration_date(date_string):
    last_verified = date_string.split('-')
    last_verified[0] = int(last_verified[0])
    last_verified[1] = int(last_verified[1])
    last_verified[2] = int(last_verified[2])
    return date(last_verified[0], last_verified[1], last_verified[2])

class VerificationEmail(Resource):
    def get(self):
        users = Users.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(users)
        for user in output:
            expiration_date = _get_expiration_date(user['last_verified'])
            verified_age = expiration_date + datetime.timedelta(days=365)
            if verified_age <= date.today():
                recipient = user['email']
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

api.add_resource(VerificationEmail, '/mail')
# [EMAILING PROG - END]



if __name__ == '__main__':
    app.run(debug=True)