from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from config import Config
from mysql_connection import get_connection
from mysql.connector import Error

from datetime import datetime

import boto3

class SnsMainResource(Resource):
    # 메인화면
    @jwt_required(optional = True)
    def get(self):
        list = request.args.get('list')
        offset=request.args.get('offset')
        limit = request.args.get('limit')
        
        try:
            connection = get_connection()
            query = '''select i.id,u.id,u.nickname,u.email,i.imgUrl,i.content,i.creatAt
                        from image i
                        join user u
                        on i.userId=u.id
                        order by '''+list+''' desc
                        limit '''+offset+''','''+limit+''';'''
            
            cursor =connection.cursor(dictionary=True)
            cursor.execute(query,)

            result_list = cursor.fetchall()

            print(result_list)

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)},500
        
        i =0
        for row in result_list:
            result_list[i]['creatAt']=row['creatAt'].isoformat()
            i = i + 1

        return{'result':'success',
               'iteam':result_list},200


class LikeYesResource(Resource):

    @jwt_required()
    def post(self):
        ImgId=request.args.get('ImgId')

        UserId=get_jwt_identity()
        try:
            connection=get_connection()
            query ='''insert into IsLike
                    (imgId,userId)
                    values
                    ('''+ImgId+''' , %s);'''
            record = (UserId,)
            print(11111111111111111111)
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error': str(e) },500
        return{'result':'success'},200


