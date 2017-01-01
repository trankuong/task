import os, re, hashlib, uuid, re, MySQLdb, MySQLdb.cursors
from flask import *
from werkzeug.utils import secure_filename
from extra import connect_to_database

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def main_route():
    if 'username' not in session:
        return render_template("login.html")
    else:
        return render_template("index.html")
        db = connect_to_database()
        cur = db.cursor()
        cur.execute("SELECT firstname, lastname FROM User WHERE username='" + session['username'] + "'")
        results = cur.fetchall()
        if results:
            results = results[0]
            firstname = results['firstname']
            lastname = results['lastname']
            return render_template("index.html", firstname = firstname, lastname = lastname)
        #if the username is not in the database
        else:
            return render_template("login.html")


@main.route('/user', methods=['GET', 'POST'])
def user_route():
    if 'username' in session:
        return redirect(url_for('main.user_edit_route'))
    else:
        return render_template("user.html")


@main.route('/edit', methods=['GET', 'POST'])
def user_edit_route():
    if 'username' not in session:
        return redirect(url_for('main.login'))
    else:
        return render_template("user_edit.html")


@main.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('main.main_route'))
    return render_template("login.html")
