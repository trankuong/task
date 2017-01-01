from flask import *
from extra import connect_to_database
import os, re, hashlib, uuid, re, MySQLdb, MySQLdb.cursors, json

user_api = Blueprint('user_api', __name__, template_folder='templates')

@user_api.route('/api/v1/user', methods=['GET', 'POST', 'PUT'])
def userApi():

    errors = []

    db = connect_to_database()
    cur = db.cursor()

    if request.method == 'GET':
        if 'username' in session:    
            cur.execute("SELECT firstname, lastname, email FROM User WHERE username='" + session['username'] + "'")
            results = cur.fetchall()
            results = results[0]
            username = session['username']
            firstname = results['firstname']
            lastname = results['lastname']
            email = results['email']
            userDict = { "username": str(username), "firstname": str(firstname), "lastname": str(lastname), "email": str(email) }
            return jsonify(userDict)
        else:
            errors.append("You do not have the necessary credentials for the resource")
            return jsonify(errors=errors), 401



    elif request.method == 'POST':

        entered = request.get_json()

        if 'username' not in entered or 'firstname' not in entered or 'lastname' not in entered or 'password1' not in entered or 'password2' not in entered or 'email' not in entered:
            errors.append("You did not provide the necessary fields")
            return jsonify(errors=errors), 422

        username = entered['username']
        firstname = entered['firstname']
        lastname = entered['lastname']
        password1 = entered['password1']
        password2 = entered['password2']
        email = entered['email']

        #Check that username is unique
        cur.execute("SELECT username FROM User WHERE username='" + str(username) + "';")
        if cur.rowcount > 0:
            errors.append("This username is taken")

        if len(username) < 3:
            errors.append("Usernames must be at least 3 characters long")
        if len(password1) < 8:
            errors.append("Passwords must be at least 8 characters long")
        if len(firstname) < 1:
            errors.append("Must include your first name")
        if len(lastname) < 1:
            errors.append("Must include your last name")

        #Check if fields are too long
        if len(username) > 20:
            errors.append("Username must be no longer than 20 characters")
        if len(firstname) > 20:
            errors.append("Firstname must be no longer than 20 characters")
        if len(lastname) > 20:
            errors.append("Lastname must be no longer than 20 characters")
        if len(email) > 40:
            errors.append("Email must be no longer than 40 characters")

        #Check that username only has letters, numbers and _
        regex = r'^[\w\d_]*$'
        if not re.match(regex, username):
            errors.append("Usernames may only contain letters, digits, and underscores")
        #Check that password has 1 number and 1 letter
        if not any(char.isdigit() for char in password1):
            errors.append("Passwords must contain at least one letter and one number")
        elif not re.search('[a-zA-Z]', password1):
            errors.append("Passwords must contain at least one letter and one number")
        #Check that password is only letters numbers and _
        if not re.match(regex, password1):
            errors.append("Passwords may only contain letters, digits, and underscores")  
         #Check that passwords match
        if password1 != password2:
            errors.append("Passwords do not match")
        #Check that is  a valid email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Email address must be valid")

        if errors:                # if an error is present, return errors
            return jsonify(errors=errors), 422
        else:
            algorithm = 'sha512'       # name of the algorithm to use for encryption
            salt = uuid.uuid4().hex    # salt as a hex string for storage in db

            m = hashlib.new(algorithm)
            m.update(salt + password1)
            password_hash = m.hexdigest()
            password = "$".join([algorithm, salt, password_hash])

            cur.execute("INSERT INTO User (username, firstname, lastname, password, email) VALUES ('" + str(username) + "', '" + str(firstname) + "', '" + str(lastname) + "','" + str(password) + "', '" + str(email) + "');")

            userDict = { "username": str(username), "firstname": str(firstname), "lastname": str(lastname), "email": str(email) }
            return jsonify(userDict), 201



    elif request.method == 'PUT':
        if 'username' in session:
            entered = request.get_json()

            updatePass = False

            if 'firstname' not in entered or 'lastname' not in entered or 'password1' not in entered or 'password2' not in entered or 'email' not in entered:
                errors.append("You did not provide the necessary fields")
                return jsonify(errors=errors), 422


            username = session['username']
            firstname = entered['firstname']
            lastname = entered['lastname']
            password1 = entered['password1']
            password2 = entered['password2']
            email = entered['email']

            #check if fields are too short
            if len(firstname) > 20:
                errors.append("Firstname must be no longer than 20 characters")
            if len(lastname) > 20:
                errors.append("Lastname must be no longer than 20 characters")
            if len(email) > 40:
                errors.append("Email must be no longer than 40 characters")
            
            #Check if fields are too long
            if len(firstname) > 20:
                errors.append("Firstname must be no longer than 20 characters")
            if len(lastname) > 20:
                errors.append("Lastname must be no longer than 20 characters")
            if len(email) > 40:
                errors.append("Email must be no longer than 40 characters")

            #Check that username only has letters, numbers and _
            regex = r'^[\w\d_]*$'
            #Check that is  a valid email
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                errors.append("Email address must be valid")

            if not ( (len(password1) == 0) and (len(password2) == 0) ): # check when user decides to update email
                updatePass = True                                       # update password in db too
                if len(password1) < 8:
                    errors.append("Passwords must be at least 8 characters long")
                #Check that password has 1 number and 1 letter
                if not any(char.isdigit() for char in password1):
                    errors.append("Passwords must contain at least one letter and one number")
                elif not re.search('[a-zA-Z]', password1):
                    errors.append("Passwords must contain at least one letter and one number")
                #Check that password is only letters numbers and _
                if not re.match(regex, password1):
                    errors.append("Passwords may only contain letters, digits, and underscores")
                #Check that passwords match
                if password1 != password2:
                    errors.append("Passwords do not match")
            
            if errors:
                return jsonify(errors=errors), 422
            #only update database when no errors
            else:
                cur.execute("UPDATE User SET firstname = '" + str(firstname) + "', lastname = '" + str(lastname) + "', email = '" + str(email) + "' where username = '" + str(username) + "';")
                #update password too
                if updatePass:

                    cur.execute("SELECT password FROM User WHERE username = '" + username + "';")
                    output = cur.fetchall()

                    #find the old hash and salt
                    password_table = output[0]['password']
                    sep = password_table.find("$")
                    sep2 = password_table.rfind("$")
                    hash_alg = password_table[0:sep]
                    salt = password_table[sep+1:sep2]

                    password = password1

                    m = hashlib.new(hash_alg)
                    m.update(salt + password)
                    password_hash = m.hexdigest()
                    password_insert = "$".join([hash_alg, salt, password_hash])

                    cur.execute("UPDATE User SET password = '" + str(password_insert) + "' WHERE username = '" + str(username) +"';")

                userDict = {
                    "username": username,
                    "firstname": firstname,
                    "lastname": lastname,
                    "email": email      
                }
                session['firstname'] = firstname
                session['lastname'] = lastname
                return jsonify(userDict), 200

        else:
            errors.append("You do not have the necessary credentials for the resource")
            return jsonify(errors=errors), 401



