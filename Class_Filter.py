#this file will hold our filter class


class Filter():
	#filter used to create a search, will be a literal sql string
	
	def __init__(self):
		self.numCond=0
		self.condition={}	#each condition contains a conditional value and an intra and an inter relation
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
		
'''if  __name__=="__main__":
	temp=Filter("Type==Squat","")
	print "created!"
	temp.expandCondition(0,"Type==Clean","or")
	print "expanded"
	temp.addCondition("Reps==1","","and")
	print "added!"
	print temp'''