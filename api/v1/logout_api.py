from flask import *

logout_api = Blueprint('logout_api', __name__, template_folder='templates')

@logout_api.route('/api/v1/logout', methods=['POST'])
def logoutApi():
    if 'username' in session:
        session.pop('username', None)
        session.pop('logged_in', None)
        session.pop('firstname', None)
        session.pop('lastname', None)
        jsonobj = {}
        return jsonify(jsonobj), 204
    else:
        jsonobj = {"errors": [{"message": "You do not have the necessary credentials for the resource"}]}
        return jsonify(jsonobj), 401
