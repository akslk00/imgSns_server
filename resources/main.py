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
        userId=get_jwt_identity()
        
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
    # 좋아요
    @jwt_required()
    def post(self,ImgId):

        UserId=get_jwt_identity()
        try:
            connection=get_connection()
            query ='''insert into IsLike
                    (imgId,userId)
                    values
                    (%s, %s);'''
            record = (ImgId,UserId)
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
    # 좋아요 해제
    @jwt_required()
    def delete(self,ImgId):

        UserId=get_jwt_identity()
        try:
            connection=get_connection()
            query ='''delete from IsLike
                    where imgId=%s and userId=%s;'''
            record = (ImgId,UserId)
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

class MainOneResource(Resource):
    # 특정 사진 상세 정보
    @jwt_required(optional=True)
    def get(self,imgId):
        userid=get_jwt_identity()
        try:
            connection = get_connection()
            query = '''select i.id,i.userId,i.content,i.creatAt,
                                u.id,u.email,u.nickname,u.cerateAt,
                                ifnull(count(I.id),0) as cntLike,if(I2.id is Null,0,1) as `like`
                        from image i
                        join user u
                        on i.userId=u.id
                        left join IsLike I
                        on I.imgId=i.id
                        left join IsLike I2
                        on i.id=I2.imgId and I2.userId =%s
                        where i.id = %s;'''
            record = (userid,imgId)

            cursor= connection.cursor(dictionary=True)
            cursor.execute(query,record)

            result_list=cursor.fetchall()
            print(result_list)
            post = result_list[0]

            
            
            if post['id'] is None:
                return{'error':'데이터가 없음'},400
            post['creatAt'] = post['creatAt'].isoformat()
            post['cerateAt'] = post['cerateAt'].isoformat()

                
               
            

            query ='''select concat('#',Tn.name) as tag
                        from tag t
                        join tag_name Tn
                        on t.tagNameId=Tn.id
                        where imgId=%s;'''
            record = (imgId,)

            cursor= connection.cursor(dictionary=True)
            cursor.execute(query,record)

            tag_list=cursor.fetchall()
            

            tag = []
            for tag_dict in tag_list:
                tag.append(tag_dict['tag'])



            cursor.close()
            connection.close()
            
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)},500
        
        return{'result':'success',
               'image':result_list[0],
               'tag':tag},200


