class GetOne(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return user
