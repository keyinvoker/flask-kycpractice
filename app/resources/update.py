class UpdatePage(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return user
    
    @marshal_with(resource_fields)
    def post(self, user_id):
        user = User.query.filter_by(id=user_id).first()
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