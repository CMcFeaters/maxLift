#a class used for conditional statements
#contains:
	#the conditional statement
	#a string representing the conditional statement
from operator import ne,eq,lt,le,ge,gt

class condition():
	l=""		#the left side of the condiion statement	
	op=""		#the operator of the condition statement
	r=""		#the right side of the condition statement
	cond=""		#the condition statement
	#opDict={ne:"!=",eq:"==",lt:"<",le:"<=",gt:">",ge:">="} #a dictionary of operators and there string equivalents
	ops=""		#the string representation of the operator	
	def __init__(self,l,r,op):
		#initializes 
		self.l=l
		self.r=r
		self.op=op
		self.ops={ne:"!=",eq:"==",lt:"<",le:"<=",gt:">",ge:">="}[op]#string representation
		self.cond=op(l,r)
	
	def __repr__(self):
		#returns a string form of condition "op(l,r)"
		return str(self.l)+' '+self.ops+' '+str(self.r)
		