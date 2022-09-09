# NOTE: old app file before implementing REST API

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

# @app.route('/get')
# def get():
#     user = Users.query.all()
#     user_schema = UserSchema(many=True)
#     output = user_schema.dump(user)
#     return {'user': output}


# NOTE: user verify page method needs frontend/html, therefore not implementing REST API
# user_patch_args = reqparse.RequestParser()
# user_patch_args.add_argument('name', type=str, help='your name')
# user_patch_args.add_argument('email', type=str, help='your email')
# user_patch_args.add_argument('phone', type=str, help='your phone')
# user_patch_args.add_argument('address', type=str, help='your address')
# user_patch_args.add_argument('salary', type=int, help='your salary')
# user_patch_args.add_argument('ktp', type=str, help='your KTP')
# user_patch_args.add_argument('npwp', type=str, help='your NPWP')

# class VerifyUser(Resource):
#     @marshal_with(resource_fields)
#     def get(self, user_id):
#         user = Users.query.filter_by(id=user_id).first()
#         return user

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

# api.add_resource(VerifyUser, '/verify-user/<int:user_id>')