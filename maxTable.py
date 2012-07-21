'''a simple database project using sqlAlchemy.  Goal is to have a orm based table to put in workout info
info: date, type, max weight, max reps'''

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys, string
import inspect
import datetime

current_module=sys.modules[__name__] #this is our current module, we're going to use this to print what the fuck we can do here

engine  = create_engine('sqlite:////Users/Charles/Magic/Projects/1rm/lift.db',echo=True)	#'''create the engine here, we will use sqlite and keep it in file'''
Base=declarative_base()	#this is our declarative base, it maintains a catalog of classes and tables relative to it
Session = sessionmaker(bind=engine)	#declare our session, the session is bound to engine and is the ORM's handle to the database

class Lift(Base):
	#lift is added to the Base catalog
	__tablename__='lift'	#give it a name
	
	id=Column(Integer, primary_key = True)	#describe the items
	type = Column(String(50))
	date = Column(Integer)	#YYYYMMDD
	maxReps = Column(Integer)
	maxWeight = Column(Integer)
	
	def __init__ (self,type,date,maxReps,maxWeight):	#init case
		self.type = type
		self.date = date
		self.maxReps = maxReps
		self.maxWeight = maxWeight
	
	def __repr__(self):	#this is what is called when the class is called to represent itself
		return "***\nLift: '%s'\nDate: '%s'\nReps: '%s'\nWeight: '%s'"%(self.type,self.date,self.maxReps,self.maxWeight)

session=Session()	#a Session object, this is initiated in order to communicate with the database
Base.metadata.create_all(engine) #this creates our table

#things we can do with our session object:
#session.add ( things ) - adds things to our session and to the database after we commit
#x=session.Query( table ).filter_by(  attribute statement ).order - queries the database returning results in array
#session.add_all([multiple,things])
#session.dirty - shows what has been changed in the db
#session.new - shows what has not been committed yet
#session.commit - commits all the outstanding changes to the db

def addRec():
#adds an individual record to our table, does not commit it
	nType=raw_input("What type of lift?")
	nDate=int(raw_input("Date? (YYYYMMDD)"))
	nmaxReps=int(raw_input("Number of reps?"))
	nmaxWeight=int(raw_input("How many lbs?"))
	session.add(Lift(nType,nDate,nmaxReps,nmaxWeight)) #this is still an outstanding change 
	print session.dirty
	raw_input("READY?")
	session.commit()
	
def showTable():
	#this function will print all the entries in the table
	ord=raw_input("Ordered (y/n)")
	if ord=='y' :
		the_order=getOrder()
		for thing in session.query(Lift).order_by(the_order):
			print thing
	else:
		for thing in session.query(Lift):
			print thing

		
def getOrder():
	#returns a string of which category to order the results by
	arr=[]
	for item in dir(Lift):
		if not item.startswith("_"):
			arr.append(item)
			print "%s: %s"%(arr.index(item),item)
	choice=int(raw_input("What order?"))
	return arr[choice]
	
def lsearchTable(nam,val):
	#this will be used with the like command
	pass
	
def searchTable():
	#this function allows us to search the table based on entered parameters
	
	arr=[]
	for item in dir(Lift):
		if not item.startswith("_"):
			arr.append(item)
	for item in arr:
		print "%s: %s"%(arr.index(item),item)
	
	type=arr[int(raw_input("choose search method"))]
	
	op=raw_input("Operator: ")
	rule=raw_input("%s %s "%(type,op))
	
	for thing in session.query(Lift).filter(("%s%s%s"%(type,op,rule))):
		print thing
		
def showTableBy():
	#this function allows you to show a table ordered by whatever the hell yoyu want
	the_order=getOrder()
	for thing in session.query(Lift).order_by(the_order):
		print thing
	

if __name__ == "__main__":
	'''options={0:addRec,1:showTable,2:searchTable,3:showTableBy,4:exit}
	
	for num in options.iterkeys():
		print "%s: %s"%(num,str(options[num]))
		
	options[int(raw_input("WHAT?"))]()'''
		
		


