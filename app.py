from flask import Flask, session, render_template
import controllers
import api.v1

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

app.register_blueprint(controllers.main)

app.register_blueprint(api.v1.user_api)
app.register_blueprint(api.v1.activities_api)
app.register_blueprint(api.v1.login_api)
app.register_blueprint(api.v1.logout_api)

# set the secret key.  keep this really secret:
app.secret_key = '\x19\xf0\xb2\xd4\x9e\xc6\x94`A\xa2\x9cVx\x83\xa2\xb3\xc0\x08>8\xaf\xe6\nE'

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host='0.0.0.0', port=3000, debug=True)
