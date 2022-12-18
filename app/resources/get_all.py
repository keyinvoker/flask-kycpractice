
class GetAll(Resource):
    def get(self):
        user = User.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(user)
        return {'user': output}
