'''a simple database project using sqlAlchemy.  Goal is to have a orm based table to put in workout info
info: date, type, max weight, max reps'''

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
import inspect
import datetime

current_module=sys.modules[__name__] #this is our current module, we're going to use this to print what the fuck we can do here

engine  = create_engine('sqlite:////Users/Charles/Magic/Projects/1rm/1rm.db',echo=True)	#'''create the engine here, we will use sqlite and keep it in file'''
Base=declarative_base()	#this is our declarative base, it maintains a catalog of classes and tables relative to it
Session = sessionmaker(bind=engine)	#declare our session, the session is bound to engine and is the ORM's handle to the database

class Lift(Base):
	#lift is added to the Base catalog
	__tablename__='Lift'	#give it a name
	
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
		return "<User ('%s','%s','%s','%s')"%(self.type,self.date,self.maxReps,self.MaxWeight)		

session=Session()	#a Session object, this is initiated in order to communicate with the database

#things we can do with our session object:
#session.add ( things ) - adds things to our session and to the database after we commit
#x=session.Query( table ).filter_by(  attribute statement ).order - queries the database returning results in array
#session.add_all([multiple,things])
#session.dirty - shows what has been changed in the db
#session.new - shows what has not been committed yet
#session.commit - commits all the outstanding changes to the db

def addRec():
	nType=raw_input("What type of lift?")
	nDate=raw_input("Date? (YYYYMMDD)")
	nmaxReps=raw_input("Number of reps?")
	nmaxWeight=raw_input("How many lbs?")
	session.add(Lift(nType,nDate,nmaxReps,nmaxWeight))
	
def showTable():
	pass

if __name__ == "__main__":
	for name,obj in inspect.getmembers(current_module,inspect.isbuiltin):
		run(obj)
	


