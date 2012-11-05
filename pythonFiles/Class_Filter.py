#this file will hold our filter class
from sqlalchemy import and_,or_
from Class_Condition import condition
class Filter():
	#filter used to create a search, will be a literal sql string
	
	def __init__(self):
		self.numCond=-1
		self.condition={}	
			#condition parts
			#{condition Number:3 part array}
			#array:
				#[0]: a condition instance
				#[1]: the inter-relationship (and_,or_,"")
				#[2]: the intra condition status (1=intra cond, 0=no intra cond)
		self.filter=""									#the statement will be the literal sql statement that gets queried
		self.filterStr=""
	def reset(self):
		#resets the filter
		self.numCond=-1
		self.condition={}	#condition: [instance of condition class , inter_relationship with existing filter (i.e. or_,and_,blank), intra status 1:exist 0: none]
		self.filter=""									#the statement will be the literal sql statement that gets queried
		self.filterStr=""
		
	def getConds(self):
		#returns an array of just the conditions
		arr=[]
		if self.condition!={}:
			for x in range(0,self.numCond+1):
				arr.append(self.condition[x][0])
		#print arr
		return arr
		
	def addCondition(self,newConditional,inter_rel):
		#adds another level to the statement, there is at least 1 condition already in the statement
		andorDict={"and_":and_,"or_":or_,"":""}
		self.numCond+=1
		self.condition[self.numCond]=[newConditional,andorDict[inter_rel],0]
		#MUST BE RE-WRITTEN
		
	def expandCondition(self,numCond,newCond,intra_rel):
		#this needs to be reworked so that we don't combine the two conditions
		#until we build the filter
		#expands an existing conditional statement to include other statements, the conditional statement is and, or or'd with the newcondition
		andorDict={"and_":and_,"or_":or_,"":""}
		self.condition[numCond][0]=andorDict[intra_rel](self.condition[numCond][0].cond,newCond.cond)
		self.condition[numCond][2]=1
		#print "Expanded"
		
	def buildFilter(self):
		#returns a filter made up of the members of the filter instance
		for key in self.condition.keys():
			if self.condition[key][1]!="": #if it has a relationship
				self.filter=self.condition[key][1](self.filter,self.condition[key][0].cond)
			elif self.condition[key][2]==1:
				#it's an intra relation condition
				self.filter=self.condition[key][0]
			else: self.filter=self.condition[key][0].cond
		return self.filter
	
	def rmvCondition(self,rmvNum):
		#remove a specific condition from the list, rebuild condition list after removal
		#this does not take into account changes in logic stemming from the removal of a piece
		for x in range(rmvNum,self.numCond):
			self.condition[x]=self.condition[x+1]
		self.numCond=self.numCond-1
	
	def hideCondition(self,hideNum):
		#hides a specific condition, changing it to either blank, 0 or 1 depending on which has the least effect on the overall logic statement
		#check if condition is the only 1
		#check if the condition inter-relates with anything
		#check if the condition is related by it's neighbor
		if self.numCond==0:
			#it's the only 1
			self.condition={}
		elif self.condition[hideNum][1]!="":
			#there is an inter-relation, and=1, or=0
			if self.condition[hideNum][1]==and_:
				self.condition[hideNum][0]=condition(0,0,eq)		#always true
			else: 
				self.condition[hideNum][0]=condition(0,1,eq)		#always false
		else:
			#there is a neighbor with an inter-relation, and=1, or=0
			if self.condition[hideNum+1][1]==and_:
				self.condition[hideNum][0]=condition(0,0,eq)		#always true
			else: self.condition[hideNum][0]=condition(0,1,eq)		#always false
	def displayCond(self,condNum):
		#returns a display string for the requested condition
		if self.condition[condNum][1]=="":
			#if there is no inter-relationship, just print the ocndition
			return str(self.condition[condNum][0])
		else:
			#there is an inter-relationship
			return self.condition[1]+" "+str(self.condition[condNum][0])

	def __repr__(self):
		#prints out the entire filter
		filt=""
		if self.condition!={}:
			for index in range(self.numCond,-1,-1):
					filt=filt+" ("+ str(self.condition[index][0])+") "+str(self.condition[index][1])
		
		return filt