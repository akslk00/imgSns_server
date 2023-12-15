from flask import request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

from email_validator import validate_email,EmailNotValidError
from utils import check_password, hash_password

class UserListResource(Resource):
    # 회원 가입 api
    def post(self):
        
        data = request.get_json()
        
        try:
            validate_email(data['email'])
        except EmailNotValidError as e:
            print(e)
            return{'error':str(e)},400
        if len(data['password'])<4 and len(data['password'])>12:
            return{'error':'비밀번호의 형식이 잘못되었습니다.'},400
        
        password=hash_password(data['password'])
        print(password)
        try:
            connection=get_connection()
            query = '''insert into user
                        (email, nickname, password)
                        values
                        (%s,%s,%s);'''
            record =(data['email'],data['nickname'],password)
            print(password)
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            user_id=cursor.lastrowid

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)},500
        
        access_token = create_access_token(user_id)

        return{'result':'success',
               'access_token':access_token},200
    
class UserLoginResource(Resource):
    
    def post(self):

        data = request.get_json()
        try:
            connection = get_connection()
            query = '''select *
                        from user
                        where email= %s;'''
            record = (data['email'],)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,record)

            result_list=cursor.fetchall()
            print(result_list)

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)},500
        
        if len(result_list) == 0:
            return{'error': '일치하는 회원 정보가 없습니다.'}
        
        check=check_password(data['password'],result_list[0]['password'])
        if check == False:
            return{'error':'비밀번호가 일치하지 않습니다.'}
        
        access_token=create_access_token(result_list[0]['id'])

        return{'result':'success',
               'access_token':access_token},200
    

jwt_blocklist = set()

class UserLogoutResourec(Resource):

    @jwt_required()
    def delete(self):
        jti = get_jwt()['jti']
        print(jti)

        jwt_blocklist.add(jti)

        return{'result':"success"},200