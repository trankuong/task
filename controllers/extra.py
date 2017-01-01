''' for local testing
from flask import *
import MySQLdb
import MySQLdb.cursors

def connect_to_database():
  options = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'root',
    'db': 'tasks',
    'cursorclass' : MySQLdb.cursors.DictCursor
  }
  db = MySQLdb.connect(**options)
  db.autocommit(True)
  return db
'''
from flask import *
import MySQLdb
import MySQLdb.cursors

def connect_to_database():
  options = {
    'host': 'trankuong.mysql.pythonanywhere-services.com',
    'user': 'trankuong',
    'passwd': 'databasepassword',
    'db': 'trankuong$tasks',
    'cursorclass' : MySQLdb.cursors.DictCursor
  }
  db = MySQLdb.connect(**options)
  db.autocommit(True)
  return db
