from __future__ import with_statement
import sys
sys.path.append('C:\\Users\Charles\Projects\maxLift\pythonFiles')

from maxTable import Lift, addRecW, queryTableW,Filter, createFilterW
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing

#create
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS',silent=True)
filter=Filter()

@app.route('/')
def welcome():
	#flask.flash("hello!")
	return render_template("welcome.html")

@app.route('/add', methods=['POST'])
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
@app.route('/build_filter',methods=['POST','GET'])
def build_filter():
	#Build the filter here
	if request.method=='POST':
		print '1'
		print request.form['fType']
		print request.form['opType']
		print request.form['val']
		cond=createFilterW(request.form['fType'],request.form['opType'],request.form['val'])
		print '2'
		filter.addCondition(cond,"")
		print filter
	return render_template('buildFilter.html',wFilter=filter)
'''
@app.route('/add_to_filter/<filter>', methods=['POST'])
def add_to_filter(filter):
	#this funciton will add to our filter and then return that value to build_filter
	print 'filter: %s'%filter
	if filter==None:
		return render_template('buildFilter.html')
	else:
		return render_template('buildFilter.html',filter=filter)'''
	
	
if __name__=='__main__':
   app.run()