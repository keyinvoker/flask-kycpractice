import app

from flask_restful import reqparse, fields

# app = Flask(__name__)
# api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/kyc'
# db = SQLAlchemy(app)
# ma = Marshmallow(app)


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

# TODO: class IndividualEmailVerificationMailing

if __name__ == '__main__':
    app.run(debug=True)
