from flask import Flask, request, jsonify
from markupsafe import escape
from database import connect_db, Database
from utils import response, load_env, hash_password
from model import CreateUserRequestBodyModel, LoginUserRequestBodyModel
from flask_pydantic import validate
from datetime import datetime, timedelta 
import jwt
from functools import wraps

config = load_env()

db = Database(config['MONGO_URL'], 'example')

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

def check_auth(f): 
    @wraps(f)
    def authenticate(*args, **kws):
        token = None
        # jwt is passed in the request header 
        if 'x-auth-token' in request.headers: 
            token = request.headers['x-auth-token'] 
        # return 401 if token is not passed 
        if not token: 
            return response(401, {'message' : 'Unauthorized access'})

        try: 
            # decoding the payload to fetch the stored details 
            data = jwt.decode(token, config['SECRET'], algorithms=["HS256"]) 
            current_user = db.find_user(data['user'])
        except: 
            return response(401, {'message' : 'Invalid Authorization Token'})

        return f(*args, **kws)
    return authenticate

@app.route("/ping", methods = ['GET'])
def ping():
    return response(200, "pong")

@app.route('/user/<username>', methods = ['GET'])
@check_auth
def profile(username):
    user = db.find_user(username)
    if user == None :
        return response(200, "User not found")

    res = {
        'name': user['name'],
        'age': user['age']
    }

    return response(200, res)

@app.route('/user/register', methods = ['POST'])
@validate(body=CreateUserRequestBodyModel)
def create_user():
    req = request.get_json()

    user = {
        'username': req['username'],
        'password': hash_password(req['password'], config['SECRET']),
        'name': req['name'],
        'age': req['age']
    }

    check_username = db.find_user(req['username'])
    if check_username :
        return response(500, "username already taken")
    
    result = db.create_user(user)

    return response(200, "Create User OK")

@app.route('/user/login', methods = ['POST'])
@validate(body=LoginUserRequestBodyModel)
def login_user() :
    req = request.get_json()

    login_data = {
        'username' : req['username'],
    }
        
    result = db.login_user(login_data)

    if not result:
        return response(401, "Data does not match our record.")
    else :
        if (hash_password(req['password'], config['SECRET']) == result['password']) :
            expired_at = datetime.utcnow() + timedelta(minutes = 60)
            token = jwt.encode({ 
                'user': result['username'], 
                'exp' : expired_at 
            }, config['SECRET'], algorithm="HS256")

            content = {
                "username" : result['username'],
                "token" : token.decode('UTF-8'),
                "expired_at": expired_at 
            }
            return response(200, content)
        return response(401, "Data does not match our record.")

@app.route('/user/delete/<username>', methods = ['DELETE'])
def remove_user(username):
    user = db.find_user(username)
    if user == None :
        return response(500, "User doesn't exist")

    result = db.delete_user(username)
    print (result)

    return response(200, "Delete user sucessfully")

if __name__ == '__main__':
   app.run(debug = True)