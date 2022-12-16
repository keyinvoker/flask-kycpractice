class EmailVerification(Resource):
    @marshal_with(resource_fields)
    def post(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        user.is_email_verified = True
        user.email_verified_at = datetime.datetime.now()
        user.status = 'Active'
        user.update()
        return user
