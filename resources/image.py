from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from config import Config
from mysql_connection import get_connection
from mysql.connector import Error

from datetime import datetime

import boto3

class ImageUploadResource(Resource):

    @jwt_required()
    def post(self):
        file=request.files.get('photo')
        content=request.form.get('content')
        user_id =  get_jwt_identity()
        if file is None:
            return{'error':'파일을 업로드 하세요'},400
        
        current_time=datetime.now()
        new_file_name=current_time.isoformat().replace(':','_')+'.jpg'

        file.filename = new_file_name
        
        s3= boto3.client('s3',
                        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY)
        
        try:
            s3.upload_fileobj(file,
                              Config.S3_BUCKET,
                              new_file_name,
                              ExtraArgs = {'ACL':'public-read',
                                           'ContentType':'image/jpeg'})
        except Exception as e:
            print(e)
            return{'error':str(e)},500
        
        tag_list=self.detect_labels(new_file_name,Config.S3_BUCKET)
        print(tag_list)

        try:
            connection = get_connection()
            query = '''insert into image
                        (userId,content,imgUrl)'''
        except Error as e:
            return
        
        return{"result":"success",
               "labels":tag_list,
               "count":len(tag_list)}
    
    def detect_labels(self, photo, bucket):

        client = boto3.client('rekognition',
                              'ap-northeast-2',
                              aws_access_key_id = Config.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY)
        
        response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},

        MaxLabels=5,
        )
        
        print('Detected labels for ' + photo)
        print()

        # 레이블만 가져오기
        tag_list =[]
        for label in response['Labels']:
            if label['Confidence'] >=90:
                print("Label: " + label['Name'])
                print("Confidence: " + str(label['Confidence']))
                tag_list.append(label['Name'])
                

        return tag_list

        