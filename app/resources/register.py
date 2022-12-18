
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

        new_user = User(
            name=name,
            email=email,
            phone=phone,
            address=address,
            salary=salary,
            ktp=ktp,
            npwp=npwp,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            is_email_verified=False,
            status='Pending',
        )

        new_user.save()
        # UpdateMailing.get(UpdateMailing, new_user.id)
        EmailVerificationMailing.get(EmailVerificationMailing, new_user.id)
        return new_user, 200
