#this file will hold our filter class
from sqlalchemy import and_,or_

class Filter():
	#filter used to create a search, will be a literal sql string
	
	def __init__(self):
		self.numCond=0
		self.condition={}	#condition: [and(x==1,y==2),inter_relationship with existing filter i.e. or_,and_,blank]
		self.filter=""									#the statement will be the literal sql statement that gets queried
		self.filterStr=""
	
	def addCondition(self,newConditional,inter_rel):
		#adds another level to the statement, there is at least 1 condition already in the statement
		if self.condition!={}:
			self.numCond+=1
		self.condition[self.numCond]=[newConditional,inter_rel]
		#MUST BE RE-WRITTEN
		
	def expandCondition(self,numCond,newCond,intra_rel):
		#expands an existing conditional statement to include other statements, the conditional statement is and, or or'd with the newcondition
		print 'FUCK'
		self.condition[numCond][0]=intra_rel(self.condition[numCond][0],newCond)
		
	def buildFilter(self):
		#returns a filter made up of the members of the filter instance
		for key in self.condition.keys():
			if self.condition[key][1]!="": #if it has a relationship
				self.filter=self.condition[key][1](self.filter,self.condition[key][0])
			else:
				self.filter=self.condition[key][0]
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
		if self.numCond==0 and self.condition!={}:
			#it's the only 1
			self.condition={}
		elif self.condition[hideNum][1]!="":
			#there is an inter-relation, and=1, or=0
			if str(self.condition[hideNum][1])==and_:
				self.condition[hideNum][0]==1
			else: self.condition[hideNum][0]==0
		else:
			#there is a neighbor with an inter-relation, and=1, or=0
			if str(self.condition[hideNum+1][1])==and_:
				self.condition[hideNum][0]==1
			else: self.condition[hideNum][0]==0	
		
		
