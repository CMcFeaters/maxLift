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
count=0
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
	entries=queryTableW(filter)
	#send that list in a render template format
	return render_template('viewEntry.html',entries=entries)

#THIS IS WEHRE YOU RESUME WORK
@app.route('/build_filter',methods=['POST','GET'])
def build_filter():
	#Build the filter here
	#this section needs the options to add more than 1 filter type, i.e. and/or
	#need options to remove things from filter
	#then an option to view the filter data
	print 'yes'
	if request.method=='POST':	#enter this section if you are sending filter data to this function
		if request.form["special"]=='reset':
			filter.reset()
		elif request.form["special"]=='view':
			return redirect(url_for('view_entry'))
		elif request.form["special"]=='add':
			cond=createFilterW(request.form['fType'],request.form['opType'],request.form['val']) #gather filter data
			filter.addCondition(cond,"","")#add the new comdition
		else:
			print 'user error'
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