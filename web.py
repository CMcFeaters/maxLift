from __future__ import with_statement
import sys
sys.path.append('C:\\Users\Charles\Projects\maxLift')

from maxTable import Lift, addRec
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing

#create
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS',silent=True)

@app.route('/')
def welcome():
	print 'hey'
	return render_template("welcome.html")

@app.route('/add', methods=['POST'])
def add_entry():
	#call our add function
	#it will take data from teh entry forms
	pass
	
if __name__=='__main__':
   app.run()