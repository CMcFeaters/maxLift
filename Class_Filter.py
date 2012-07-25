#this file will hold our filter class

class Filter():
	#this is a filter class, it will be used to store the data for our filter statement
	#I want it to handle complex queries with multiple and/or levels
	'''the filter will store an array of levels, each level will have a number, 
	contain some conditionals, relate to all other levels with either an and or an or'''
	#attributes
	def __init__(self):
		self.highestLvl=0	#keeps track of the levels in the filter
							#a level is an "and" or an "or" statement "z==5", 
							#"X==7 and y==6" are 1 level, "x==7 and (z==5 or y==6)" is 2 levels
		
		self.lvls=[]		#an array containing all the levels
		
	#and the following abilities
	def addLevel(self,level):
		#a lvl can only and/or with levels with lower numbers
		if self.lvls!=[]:self.highestLvl+=1
		level.num=self.highestLvl				#assign a number to the level
		
		if level.andLvl!=[]:	#if there are things in the andLvl array we make sure they are only lower thna the current level num
			for thing in level.andLvl:
				if int(thing)>level.num: level.andLvl.remove(thing)
		
		if level.orLvl!=[]:
			#if there are things in the orLvl array we make sure they are only lower thna the current level num
			for thing in level.orLvl:
				if int(thing)>level.num: level.orLvl.remove(thing)
		
		self.lvls.append(level)	#add the level to the list
	
	def createFilter(self):
		#turns the current array of lvls into a single filter statement
		pass
	
		
class Level():
	#a level contains this info
	#packet: an array of conditional statements,how they relate to eachother (and/or)
	conditional=[]	#this array contains all the levels conditional statemetns
	num=0				#this is the levels number, it can be whatever when it's created, it
	
	def __init__(self,conditional,relation,andLvl,orLvl):
				
		self.conditional.append(conditional)	#an array containing all conditional statements for this level
		self.relation=relation					#how the conditionals relate (and/or)
		self.andLvl=andLvl						#all levels this level logicaly "and" with
		self.orLvl=orLvl						#all levels this level logically "or" with
		
	def addToLevel(self,condition,relation):
		#append some conditions to the statement and update how the objects relate
		self.conditional.append(condition)
		self.relation=relation
		
if __name__=="__main__":
	Level0=Level("x==1","none","","")
	Level0.addToLevel("y==7","and")