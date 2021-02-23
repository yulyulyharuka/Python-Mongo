from flask import jsonify
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Create response with http status code and anytype as content as parameter
def response(status, content) :
    response = {
        "status" : status, 
        "content": content,
    }

    return jsonify(response)
 
def load_env() :
    load_dotenv()
    url = os.getenv('MONGO_URL')

    config = {
        "MONGO_URL" : url,
    }
    
    return config