from __future__ import with_statement
import sys
sys.path.append('C:\\Users\Charles\Projects\maxLift\pythonFiles')

from maxTable import Lift, addRecW, queryTableW
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing

#create
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS',silent=True)

@app.route('/')
@app.route('/<entry>')
def welcome(entry=None):
	return render_template("welcome.html",entry=entry)

@app.route('/add', methods=['POST','GET'])
def add_entry():
	#call our add function
	#it will take data from teh entry forms
	error=None
	if request.method=='POST':
		addRecW(request.form)
		return redirect(url_for('welcome',entry=request.form['nType']))
	return render_template('addEntry.html',error=error)

@app.route('/view')
def view_entry():
	#get entries in a list
	entries=queryTableW()
	#send that list in a render template format
	return render_template('viewEntry.html',entries=entries)

#THIS IS WEHRE YOU RESUME WORK
@app.route('/build')
def build_filter():
	#Build the filter here
	return render_template('buildFilter.html')
	
	
	
if __name__=='__main__':
   app.run()