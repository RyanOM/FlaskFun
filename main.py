from flask import Flask, request
app = Flask(__name__)

import json

DB = {
    'aaron': {
        'age': 21,
        'presents': [],
    },
    'ryan': {
        'presents': [],
    }
}

def query(username):
    user = DB[username]
    return {
        'username': username,
        'presents': user.get('presents', []),
        'age': user.get('age', 0)
    }

def insert_user(username, age):
    DB[username] = {
        'age': age,
    }

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/users")
def users_list():
    return json.dumps(DB.items())

@app.route("/users/search")
def search():
    q = request.args.get('q')

    results = []

    for username, user_data in DB.items():
        if q in username:
            user_data['username'] = username
            results.append(user_data)

    return json.dumps(results, indent=True)

@app.route("/user/<username>")
def get_user(username):
    try:
        person = query(username)
    except:
        return "Unknown user %s" % username

    return json.dumps(person)


@app.route("/user", methods=['POST'])
def create_user():
    if request.method == 'GET':
        return "GET, noting to do"

    f = request.form

    if not('name' in f and 'age' in f):
        return "Please supply name and age"

    insert_user(f['name'], f['age'])

    return "Successfuly created user: %s" % (f['name'])

if __name__ == "__main__":
    app.run(debug=True)
