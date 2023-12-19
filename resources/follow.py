from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from config import Config
from mysql_connection import get_connection
from mysql.connector import Error

from datetime import datetime

import boto3

class FollowerResource(Resource):

    # 친구추가
    @jwt_required()
    def post(self,fuserId):
        userId=get_jwt_identity()
        try:
            connection=get_connection()
            query = '''insert into follow
                        (followerId,followeeId)
                        values
                        (%s,%s);'''
            record =(userId,fuserId)

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
    # 친구삭제
    @jwt_required()
    def delete(self,fuserId):
        userId=get_jwt_identity()
        try:
            connection=get_connection()
            query = '''delete from follow
                        where followerId=%s and followeeId=%s;'''
            record =(userId,fuserId)

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
    

class FollowListResource(Resource):

    # 친구의 이미지 가져오기
    @jwt_required()
    def get(self):
        userId=get_jwt_identity()
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        try:
            connection = get_connection()
            query = '''select i.id userId,i.content,i.imgUrl,i.creatAt,
                                u.id userId,u.email,u.nickname,
                                count(I.id) as likeCnt,if(I2.id is Null,0,1) as isLike
                        from image i
                        join follow f
                        on i.userId=f.followeeId
                        join user u
                        on u.id=i.userId
                        left join IsLike I
                        on I.imgId=i.id
                        left join IsLike I2
                        on i.id=I2.imgId and I2.userId=%s
                        where f.followerId=%s
                        group by i.id
                        order by i.creatAt desc
                        limit '''+offset+''','''+limit+''';'''
            record =(userId,userId)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,record)

            result_list=cursor.fetchall()
            print(result_list)

            i = 0
            for row in result_list :
                result_list[i]['creatAt'] = row['creatAt'].isoformat()
                i = i + 1 

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)},500
        
        return{'result':'success',
               'items':result_list,
               'count':len(result_list)}
