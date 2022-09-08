from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with
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

# @app.route('/verify/<int:id>', methods=['POST', 'GET'])
# def verify(id):
#     user = Users.query.get_or_404(id)
#     if request.method == 'POST':
#         user.name = request.form['name']
#         user.email = request.form['email']
#         user.phone = request.form['phone']
#         user.address = request.form['address']
#         user.salary = request.form['salary']
#         user.ktp = request.form['ktp']
#         user.npwp = request.form['npwp']
#         user.last_verified = date.today()
        
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'Failed updating user!'
#     else:
#         return render_template('verify.html', user=user)

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

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'address': fields.String,
    'salary': fields.Integer,
    'ktp': fields.String,
    'npwp': fields.String,
    'last_verified': fields.DateTime,
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
        return new_user, 201
api.add_resource(RegisterUser, '/register')

class VerifyUser(Resource):
    def get(id):
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
api.add_resource(VerifyUser, '/verify/<int:id>')

class GetAll(Resource):
    def get(self):
        user = Users.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(user)
        return {'user': output}
api.add_resource(GetAll, "/get")
# [using flask_restful.Resource - END]



if __name__ == '__main__':
    app.run(debug=True)