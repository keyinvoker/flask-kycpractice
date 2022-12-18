class UpdateFinalizer(Resource):
    @marshal_with(resource_fields)
    def post(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        user.updated_at = datetime.datetime.now()

        if user.is_email_verified==True:
            user.status = 'Active'
        user.update()

        if user.is_email_verified==False:
            # user.status = 'Disabled'
            EmailVerificationMailing.get(EmailVerificationMailing, user.id)
        return user
