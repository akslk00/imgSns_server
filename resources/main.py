from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from config import Config
from mysql_connection import get_connection
from mysql.connector import Error

from datetime import datetime

import boto3

class SnsMainResource(Resource):

    @jwt_required(optional = True)
    def get(self):

        try:
            connecrion = get_connection()
            query = ''''''
        except Error as e:
            return
        return
