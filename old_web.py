from __future__ import with_statement
import sys
sys.path.append('C:\\Users\\Charles\\ldb\\flaskr\\sqlBackend')
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing
from queryData import runSelectws
import enterData
import dataValidate
import tableSetup

DATABASE = '/Users/Charles/ldb/flaskr/test0.db' #where the database we are accessing is stored
#DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME2 = 'admin2'
USERNAME = 'admin'
PASSWORD = 'default'

#create
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS',silent=True)

#apparently g is magical and does work behind scenes.  it also
#holds information from one request and is available within each function

@app.route('/')
def welcome():
   error=None
   if not session.get('logged_in'):
       flash('Login or Create a profile!')
   return render_template('welcome_screen.html',error=error)


@app.route('/browse_data')
def browse_data():
   #editing to show entries from liftdb
   if session.get('logged_in'):
       #cur = g.db.execute('select uid, pw from user')
       #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]#for row in cur.fetchall()]
       entries=[]
   else:
       entries=[]
   return render_template('show_entries.html', entries=entries)

@app.route('/add',methods=['POST']) #executes if a post request is made
def add_entry():
   #this is the page that is called whenever the add url is called
   if not session.get('logged_in'):#check for the logged_in key
       abort(401)  #exit if not logged in
   flash('New Entry was successfully posted')  #message that gets flashed onthe screen
   return redirect(url_for('browse_data'))


@app.route('/login', methods=['GET', 'POST'])   #routes the login info
def login():
   error = None
   if request.method == 'POST':    #button pressed?
       nam=request.form['username']
       pw=request.form['password']
       #check if username is in our database
       if runSelectws(['user.uid'],'user.uid="%s"'%nam.lower()) == []:#run a search here to see if it's in the users.uid table
           error = 'Invalid username'
       elif runSelectws(['user.uid'],'user.uid="%s" and user.pw="%s"'%(nam.lower(),pw)) ==[]:#run a search here to see if it's in teh users.pw table
           error = 'Invalid password'
       else:
           session['logged_in'] = True
           flash('Welcome %s'%nam)
           #return redirect(url_for('welcome_screen'))
           return render_template('welcome_screen.html',error=error)
   return render_template('login.html', error=error)


@app.route('/enter_data', methods=['GET','POST'])
def enter_data():
   error=None
   return render_template('enter_data.html',error=error)

@app.route('/search_data', methods=['POST'])
def search_data():
   error=None
   return render_template('search_data.html',error=error)

@app.route('/browse_data', methods=['GET','POST'])
def browse_data():
   error=None
   return render_template('browse_data.html',error=error)

@app.route('/create_workout',methods=['POST'])
def create_workout():
   #this creates our workout data table, it does not write it to our database
   status=request.form['wstatus']

   yr=request.form['year']
   mo=request.form['month']
   dy=request.form['day']

   if not yr.isdigit():
       error= 'fuck'
   
   #wdict=dict([['wDate',date],['wStatus',status]])
   return render_template('enter_data.html',error=error)

@app.route('/create', methods=['POST','GET'])   #routes the registration info
def create():
   error = None
   if request.method == 'POST':    #button pressed?
       
       #run our data validation and post any errors
       nam=request.form['username']
       pw=request.form['password']
       nameError=dataValidate.uidCheck('%s'%nam.lower())
       pwError=dataValidate.pwCheck('%s'%pw)
       
       if nameError!='':#run a search here to see if it's in the users.uid table
           error = nameError
       elif pwError!='':
           error=pwError
       else:
           #create the new user here
           enterData.createEntry(tableSetup.user,dict([
               ['uid',nam.lower()],
               ['name',nam],
               ['pw',pw]]))
           #this should point to some welcome screen
           return redirect(url_for('welcome.html'))
   return render_template('create.html', error=error)

@app.route('/logout')
def logout():
   session.pop('logged_in', None)
   flash('You were logged out')
   return redirect(url_for('welcome'))

if __name__=='__main__':
   app.run()

