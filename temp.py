#add path for maxlift.py then use that add command to talk to database,
#information for add will be gathered on teh web app, screened then sent to our
#python backend
from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def home():
	return "hello world"
	
@app.route('/hello/')
def hello(name=None):
	return render_template('main.htm',name=name)

@app.route('/add',methods=['POST','GET'])
def add_entry():
	#add an entry to the database
	return 'Time to add!'
	
if __name__=='__main__':
	app.run()