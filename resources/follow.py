from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from config import Config
from mysql_connection import get_connection
from mysql.connector import Error

from datetime import datetime

import boto3

class FollowerResource(Resource):


    @jwt_required()
    def post(self):
        addfrind=request.args.get('addfrind')
        userId=get_jwt_identity()
        try:
            connection=get_connection()
            query = '''insert into follow
                        (followerId,followeeId)
                        values
                        (%s,'''+addfrind+''');'''
            record =(userId,)

            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)},500
        
        return{'result':'success'},200