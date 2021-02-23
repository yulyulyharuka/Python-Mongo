from flask import Flask, request, jsonify
from markupsafe import escape
from database import connect_db, Database
from utils import response, load_env

config = load_env()

db = Database(config['MONGO_URL'], 'example')

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/ping", methods = ['GET'])
def hello():
    return "pong"

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
def create_user():
    req = request.get_json()

    user = {
        'username': req['username'],
        'name': req['name'],
        'age': req['age']
    }
    result = db.create_user(user)

    return response(200, "Create User OK")

if __name__ == '__main__':
   app.run(debug = True)