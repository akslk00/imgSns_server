from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required
from flask_restful import Api
from config import Config
from resources.follow import FollowerResource
from resources.image import ImageUploadResource
from resources.main import LikeYesResource, SnsMainResource
from resources.user import UserListResource, UserLoginResource, UserLogoutResourec
from resources.user import jwt_blocklist

app = Flask(__name__)



app.config.from_object(Config)

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header,jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blocklist

api = Api(app)


api.add_resource(UserListResource,'/user/add')

api.add_resource(UserLoginResource,'/user/login')

api.add_resource(UserLogoutResourec,'/user/logout')

api.add_resource(ImageUploadResource,'/upload')

api.add_resource(SnsMainResource,'/main')

api.add_resource(LikeYesResource,'/like')

api.add_resource(FollowerResource,'/follow')



if __name__ == '__main__':
    app.run()
