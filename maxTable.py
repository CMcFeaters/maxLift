'''a simple database project using sqlAlchemy.  Goal is to have a orm based table to put in workout info
info: date, type, max weight, max reps'''

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Class_Filter import Filter
import sys, string, inspect

current_module=sys.modules[__name__] #this is our current module, we're going to use this to print what the fuck we can do here

engine  = create_engine('sqlite:////Users/Charles/Magic/Projects/1rm/lift.db',echo=True)	#'''create the engine here, we will use sqlite and keep it in file'''
Base=declarative_base()	#this is our declarative base, it maintains a catalog of classes and tables relative to it
Session = sessionmaker(bind=engine)	#declare our session, the session is bound to engine and is the ORM's handle to the database

newFilt= Filter() #an instance of the Filter object, it will be in each iteration of the program



class Lift(Base):
	#lift is added to the Base catalog
	__tablename__='lift'	#give it a name
	#members of the Lift class
	id=Column(Integer, primary_key = True)	#describe the items
	type = Column(String(50))
	date = Column(Integer)	#YYYYMMDD
	month=Column(Integer)
	day=Column(Integer)
	year=Column(Integer)
	maxReps = Column(Integer)
	maxWeight = Column(Integer)
	
	def __init__ (self,type,month,day,year,maxReps,maxWeight):	#init case
		self.type = type
		self.date = int(str(year)+str(month)+str(day))
		self.month=month
		self.day=day
		self.year=year
		self.maxReps = maxReps
		self.maxWeight = maxWeight
	
	def __repr__(self):	#this is what is called when the class is called to represent itself
		return "***\nLift: '%s'\nDate: '%s'\nReps: '%s'\nWeight: '%s'"%(self.type,str(self.month)+"/"+str(self.day)+"/"+str(self.year),self.maxReps,self.maxWeight)

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
	nMonth=int(raw_input("Month? (MM)"))
	nDay=int(raw_input("Day? (DD)"))
	nYear=int(raw_input("Year? (YYYY)"))
	nmaxReps=int(raw_input("Number of reps?"))
	nmaxWeight=int(raw_input("How many lbs?"))
	session.add(Lift(nType,nMonth,nDay,nYear,nmaxReps,nmaxWeight)) #this is still an outstanding change 
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

def addFilterP():
	#this function displays all the parameters that can be added to filters
	#returns a string "rule" 
	newFilter=createFilter()	#new filter is entered by user, if existing filters, determine if it's an "and" or an "or" filter
	
def rmvFilterP():
	#function to remove a filter parameter
	pass
	
def addOrderP():
	#function to add an orderby parameter
	pass

def rmvOrderP():
	#function to remove a specific orderby paramater
	pass
	
def createFilter():
	#this function displays all the parameters that can be added to filters
	#returns a string representing a filter statement 
	
	arr=[item for item in dir(Lift) if not item.startswith("_") ]	#build a quick array and print out all 
	
	#allow user to input the data for the filter
	cat=arr[int(raw_input("Choose filter category"))]	#cat: the category we filter by
	op=raw_input("Operator: ")							#op: The operator we use in our filtering eg: ==, >
	val=raw_input("%s %s "%(cat,op))					#val: teh value we are evaluating towards
	
	#add a method to evaluate if the new filter is legal
	return (cat,op,val)	#return the filter as a triple in the format of cat,op,val
	
	
		
def searchEdit():
	#search function generator, returns a tuple, containing the filter and orderby parameters
	options={0:("Add a filter Parameter",addFilterP),1:("Add order parameter",addOrderP),2:("Remove Filter Parameter",rmvFilterP),\
		3:("Remove Filter Parameter",rmvOrderP),4:("Done",exit)}
	currentFilter=""
	currentOrder=""
	while 1:
		for num in options.iterkeys():
			print "%s: %s"%(num,str(options[num][0]))
		choice=int(raw_input("->"))
		if choice==4:
			break
		else: options[choice][1]()
	

if __name__ == "__main__":
	#this is going to be the main loop, 2 layer menu, add or search
	#add portion add records
	#search portion, display current search parameters, allow addition of and/or parameters and order parameters
	
	options={0:("Add a Record",addRec),1:("Edit Search Parameters",searchEdit),2:("Execute the Search",showTable),3:("Exit Program",exit)}
	
	while 1:
		for num in options.iterkeys():
			print "%s: %s"%(num,str(options[num][0]))
		options[int(raw_input("->"))][1]()
		
		


