'''a simple database project using sqlAlchemy.  Goal is to have a orm based table to put in workout info
info: date, type, max weight, max reps'''

from sqlalchemy import create_engine, Column, Integer, String, Date, and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Class_Filter import Filter
import sys, string
from operator import ne,eq,lt,le,ge,gt
from Class_Condition import condition

sys.path.append("C:\\Users\Charles\Dropbox\Programming\py\general_use")
from validation import digitValidate,optionValidate

#this section chooses the path the database is stored on
'''try:#desktop path
	path="/Users/Charles/Projects/maxLift/lift.db"
	if open(path): pass
except IOError as e:#laptoppath
	print "not Found"
	path="/Users/Charles/Magic/Projects/1rm/lift.db"'''
path ="C:\\Users\Charles\Dropbox\Programming\DataBases\lift.db"
	
engine  = create_engine('sqlite:///'+path,echo=True)	#'''create the engine here, we will use sqlite and keep it in file'''
Base=declarative_base()	#this is our declarative base, it maintains a catalog of classes and tables relative to it
Session = sessionmaker(bind=engine)	#declare our session, the session is bound to engine and is the ORM's handle to the database

filter=Filter()

class Lift(Base): #this is the class our database is based around
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
	memberDict={0:("id",id),1:("type",type),2:("date",date),3:("month",month),4:("day",day),5:("year",year),6:("maxReps",maxReps),7:("maxWeight",maxWeight)}# a dictionary of all the members
	
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
	#adds an individual record to our table, then commits it
	nType=raw_input("What type of lift?").lower()
	nMonth=digitValidate("Month? (MM)",2)
	nDay=digitValidate("Day? (DD)",2)
	nYear=digitValidate("Year? (YYYY)",4)
	nmaxReps=int(raw_input("Number of reps?"))
	nmaxWeight=int(raw_input("How many lbs?"))
	session.add(Lift(nType,nMonth,nDay,nYear,nmaxReps,nmaxWeight)) #this is still an outstanding change 
	session.commit()



def queryTable():
	#queries the database with whatever is currently in the filter
	for thing in session.query(Lift).filter(filter.buildFilter()):
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

def addParam(cond):
	#adds a new parameter to our filter
	andor={0:and_,1:or_}
	print "0) AND\n1) OR"
	filter.addCondition(cond,andor[optionValidate("->",range(2))],0)
	
def expandParam(cond):
	#allows the user to choose a condition to expand
	for key in filter.condition.keys():
		print "%s) %s"%(key,filter.condition[key][0])
	choice=int(raw_input("->"))
	andor={0:and_,1:or_}	#what type of expansion
	print "0) AND\n1) OR"
	filter.expandCondition(choice,cond,andor[optionValidate("->",range(2))])
	
def createFilter():
	#this function displays all the parameters that can be added to filters
	#uses 2 dicts and 1 user entry to setup the filter parameters
	#returns the filter statement op(cat,val)
	
	opDict={0:("!=",ne),1:("==",eq),2:("<",lt),3:("<=",le),4:(">=",ge),5:(">",gt)} #the operator dict (0) is the printable symbol (1) is the object
	
	#cat: the category we filter by
	
	#print out cat options 
	for key in Lift.memberDict.keys():		
		print "%s) %s"%(key,Lift.memberDict[key][0])
	#user input for the category, selects the key for memberdict from the items in memTemp
	(_cat,cat)=Lift.memberDict[optionValidate("Choose filter category",range(key+1))]
	
	#op: The operator we use in our filtering eg: ==, >
	for key in opDict.keys():		
		print "%s) %s"%(key,opDict[key][0])
	#user input for the category, selects the key for opDict from the items in opTemp
	(_op,op)=opDict[optionValidate("Choose filter category",range(key+1))]
	
	#val: teh value we are evaluating towards
	val=raw_input("%s %s "%(_cat,_op)).lower()										
	
	return condition(cat,val,op)	

def addFilterP():
	#this function displays all the parameters that can be added to filters
	#returns a string "rule" 
	newCond=createFilter()	#new filter is entered by user, if existing filters, determine if it's an "and" or an "or" filter
	if filter.condition=={}:			#if this is the first thignin our filter, we jsut add the case and call it a day
		filter.addCondition(newCond,"")
	else:								#if it's not, find out how it relates to the other cases
		#determine if it expands an existing option or creates a new one
		choice={0:expandParam,1:addParam}
		print "0) Expand Existing Parameter \n1) Add New Parameter"
		choice[optionValidate("->",range(2))](newCond)
		

def rmvFilterP():
	#function to remove a filter parameter
	#display parameters that can be removed
	#change conditions based on removing 1 from beginning, middle or end
	
	#choose parameter to remove
	print "Pick parameter to remove"
	for key in filter.condition.keys():
		print "%s) %s"%(key,filter.condition[key][0])
	choice=optionValidate("->",range(len(filter.condition.keys())))
	
	filter.hideCondition(choice)
	
	
def addOrderP():
	#function to add an orderby parameter
	pass

def rmvOrderP():
	#function to remove a specific orderby paramater
	pass
	
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
	
	options={0:("Add a Record",addRec),1:("Edit Search Parameters",searchEdit),2:("Execute the Search",queryTable),3:("Exit Program",exit)}
	#filter.addCondition("date==7","")
	#filter.expandCondition(0,"id==5",or_)
	#filter.addCondition(eq(Lift.type,"Clean"),"")
	#filter.expandCondition(0,gt(Lift.maxWeight,300),and_)
	filter.addCondition(condition(Lift.type,"clean",eq),"",0)
	filter.expandCondition(0,condition(Lift.type,"squat",eq),or_)
	filter.addCondition(condition(Lift.month,"08",eq),and_,0)
	while 1:
		print "Current Filter: %s"%filter
		for num in options.iterkeys():
			print "%s: %s"%(num,str(options[num][0]))
		options[optionValidate("->",range(4))][1]()
	''' thing in session.query(Lift).filter(and_(Lift.type=="Squat",Lift.maxReps==1)):
		print thing'''