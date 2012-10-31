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
	inter=""
	intra=""
	if request.method=='POST':	#enter this section if you are sending filter data to this function
		if request.form["navFlag"]=='reset':
			#run the reset function
			filter.reset()
		elif request.form["navFlag"]=='view':
			#execute filter and view the results
			return redirect(url_for('view_entry'))
		elif request.form["navFlag"]=='add':
			#ADD
			#create the condition
			cond=createFilterW(request.form['fType'],request.form['opType'],request.form['val']) #gather filter data
			#this if statement needs to check if we are adding an inter-relation or an intra-relation
			if request.form["addType"]=='expand':
				print "1"
				intra=request.form["andorP"]
				print "2"
				print request.form["exCondNum"]
				filter.expandCondition(int(request.form["exCondNum"]),cond,intra)
			elif filter.condition!={} and filter.numCond>0:
				intra=request.form["andor"]
			else:#we are making our first filter param
				filter.addCondition(cond,"","")#add the new condition
		else:
			#this runs if somehow we got here, posted and managed not to hit one of the buttons
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