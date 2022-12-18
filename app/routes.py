from app import api
from app.resources.index import Index
from app.resources.register import Register
from app.resources.get_one import GetOne
from app.resources.get_all import GetAll
from app.resources.annual_mailing import AnnualMailing

# api.add_resource(Index, '/')
# api.add_resource(Register, '/register')
api.add_resource(GetOne, '/get/<int:user_id>')
api.add_resource(GetAll, "/get")
# api.add_resource(UpdatePage, '/update/<int:user_id>')
# api.add_resource(UpdateFinalizer, '/finalize/<int:user_id>')
# api.add_resource(UpdateMailing, '/mail/<int:user_id>')
# api.add_resource(EmailVerification, '/verify/<int:user_id>')
api.add_resource(AnnualMailing, '/mail/unverified')
# api.add_resource(EmailVerificationMailing, '/mail/unverified/<int:user_id>')