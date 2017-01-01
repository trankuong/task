from flask import *
from extra import connect_to_database
import MySQLdb, MySQLdb.cursors, json

activities_api = Blueprint('activities_api', __name__, template_folder='templates')

@activities_api.route('/api/v1/activities',  methods=['GET', 'POST', 'PUT', 'DELETE'])
def activitiesApi():
	
	errors = []

	if request.method == 'GET':
		
		if 'username' in session:
			username = session['username']
			db = connect_to_database()
			cur = db.cursor()

			schedule = {}

			if username == 'admin':
				cur.execute("SELECT activityid, username, activity_time, activity, details FROM Activities ORDER BY username, activity_time ASC, activity ASC;")
			else:
				cur.execute("SELECT activityid, username, activity_time, activity, details FROM Activities WHERE username = '" + username + "' ORDER BY activity_time ASC, activity ASC;")
			
			if cur.rowcount == 0:
				return jsonify(schedule)
			else:
				result = cur.fetchall()
				for each in result:
					if each['username'] not in schedule:
						schedule[each['username']] = []
					activity = {"activityid": each['activityid'], "time": each['activity_time'].strftime("%a, %b %d, %Y %I:%M %p"), "activity": each['activity'], "details": each['details']}
					schedule[each['username']].append(activity)
				return jsonify(result=schedule)
		else:
			errors.append("You can not view any schedules")
			return jsonify(errors=errors), 401


	elif request.method == 'POST':
		if 'username' in session:
			insert = request.get_json()
			username = insert['username']
			time = insert['time']
			activity = insert['activity']
			if 'details' in insert:	
				details = insert['details']
			else:
				details = ""

			db = connect_to_database()
			cur = db.cursor()
			cur.execute("INSERT INTO Activities(username, activity_time, activity, details) VALUES ('" + str(username) + "', '" + str(time) + "', '" + str(activity) + "', '" + str(details) + "');")
			ret_obj = { "username": username, "time": time, "activity": activity, "details": details}
			return jsonify(ret_obj)
		else:
			errors.append("You do not have the necessary permissions for this.")
			return jsonify(errors=errors), 401

	elif request.method == 'PUT':
		if 'username' in session:
			update = request.get_json()
			activityid = update['activityid']
			username = update['username']
			time = update['time']
			activity = update['activity']
			details = update['details']

			if (username == session['username']) or (session['username'] == 'admin'):
				db = connect_to_database()
				cur = db.cursor()
				cur.execute("UPDATE Activities SET activity_time = '" + str(time) + "', activity = '" + str(activity) + "', details = '" + str(details) + "' where activityid = '" + str(activityid) + "';")
				db = connect_to_database()
				cur = db.cursor()
				cur.execute("SELECT activity_time FROM Activities WHERE activityid = '" + str(activityid) + "';")
				result = cur.fetchone()
				ret_obj = result['activity_time'].strftime("%a, %b %d, %Y %I:%M %p")
				return jsonify(result=ret_obj), 200
			else:
				errors.append("You do not have the necessary permissions for this.")
				return jsonify(errors=errors), 401
		else:
			errors.append("You do not have the necessary permissions for this.")
			return jsonify(errors=errors), 401

	elif request.method == 'DELETE':
		if 'username' in session:
			activityid = request.args.get('activityid')

			db = connect_to_database()
			cur = db.cursor()
			cur.execute("SELECT username from Activities where activityid = '" + str(activityid) + "';")
			if cur.rowcount > 0:
				result = cur.fetchone()
				username = result['username']
				if (username == session['username']) or (session['username'] == 'admin'):
					cur.execute("DELETE from Activities WHERE activityid = '" + str(activityid) + "';")
					return jsonify(errors=errors)
				else:
					errors.append("You do not have the necessary permissions for this.")
					return jsonify(errors=username), 401
			else:
				errors.append("Activity does not exist.")
				return jsonify(errors=errors), 401
		#else:
		#	errors.append("You do not have the necessary permissions for this.")
		#		return jsonify(errors=errors), 401
