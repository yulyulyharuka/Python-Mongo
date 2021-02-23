from flask import Flask, request, jsonify
from markupsafe import escape
from database import connect_db, Database
from utils import response, load_env, hash_password
from model import CreateUserRequestBodyModel, LoginUserRequestBodyModel
from flask_pydantic import validate

config = load_env()

db = Database(config['MONGO_URL'], 'example')

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/ping", methods = ['GET'])
def ping():
    return response(200, "pong")

@app.route('/user/<username>', methods = ['GET'])
def profile(username):
    user = db.find_user(username)
    if user == None :
        return response(200, "User not found")

    res = {
        'name': user['name'],
        'age': user['age']
    }

    return response(200, res)

@app.route('/user/create', methods = ['POST'])
@validate(body=CreateUserRequestBodyModel)
def create_user():
    req = request.get_json()

    user = {
        'username': req['username'],
        'password': hash_password(req['password'], config['SECRET']),
        'name': req['name'],
        'age': req['age']
    }
    result = db.create_user(user)

    return response(200, "Create User OK")

@app.route('/user/login', methods = ['POST'])
@validate(body=LoginUserRequestBodyModel)
def login_user() :
    req = request.get_json()

    login_data = {
        'username' : req['username'],
        'password' : hash_password(req['password'], config['SECRET'])
    }
    result = db.login_user(login_data)

    return response(200, "login token")

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