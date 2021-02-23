from flask import jsonify
import os
from os.path import join, dirname
from dotenv import load_dotenv
import hashlib

# Create response with http status code and anytype as content as parameter
def response(status, content) :
    response = {
        "status" : status, 
        "content": content,
    }

    return jsonify(response), status
 
def load_env() :
    load_dotenv()

    config = {
        "MONGO_URL" : os.getenv('MONGO_URL'),
        "SECRET" : os.getenv('SECRET_KEY'),
    }
    
    return config

def hash_password(password, secret) :
    password = password.encode('utf-8')
    secret = secret.encode('utf-8')
    hash_password = hashlib.sha256(password + secret).hexdigest()

    return hash_password