
from api import api
from api.routes.verification import Verification
from api.routes.user import CRUDUser
from api.routes.task import CRUDTask


api.add_resource(Verification, '/api/verification')
api.add_resource(CRUDUser, '/api/user')
api.add_resource(CRUDTask, '/api/task')