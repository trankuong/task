from flask import *
import hashlib
from extra import connect_to_database

login_api = Blueprint('login_api', __name__, template_folder='templates')

@login_api.route('/api/v1/login', methods=['POST'])
def loginApi():
    #Array for errors
    errors = []
    posteddata = request.get_json()
    try:
        username = posteddata['username']
        password = posteddata['password']
    except KeyError:
        errors.append("You did not provide the necessary fields")
        return jsonify(errors=errors), 422
        
    db = connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT firstname, lastname, password FROM User WHERE username='" + posteddata['username'] + "'")
    #Check for valid username
    if cur.rowcount != 0:
        result = cur.fetchone()

        #Check for correct password
        password_table = result['password']
        password_parts = password_table.split("$")

        hash_alg = password_parts[0]
        salt = password_parts[1]

        m = hashlib.new(hash_alg)
        m.update(salt + password)
        password_hash = m.hexdigest()
        password_check = hash_alg + "$" + salt + "$" + password_hash

        if password_table != password_check:
            errors.append("Password is incorrect for the specified username")
            return jsonify(errors=errors), 422

        #Login was good so create session
        session['username'] = username
        session['firstname'] = result['firstname']
        session['lastname'] = result['lastname']
        session['logged_in'] = True
        return jsonify({"username":username})
    else:
        errors.append("Username does not exist")
        return jsonify(errors=errors), 404