class case ():
	ATTRIBUTE_VALUES = {}
	ACTIONS_VALUE = {}
	ACTIONS_DONE_VALUE = {}
	NAME = "case"
	'''
	#data:
		#attributes: describes case attributes, a dict of (item,[attribute]) which describes the attribute
			#ATTRIBUTES_VALUE: a dict of (item,value)
		#actions: a dict of (acted_upon,[action]) which describes what is happening
			#ACTIONS_VALUE: a dict (acted_upon,value)
		#actions_done:a dict of (acted_upon,[action]) previously prescribed solutions
			#ACTIONS_DONE_VALUE: a dict of (acted_upon, value)
		#action_prescribe: what was prescribed in case
		#parent: refr to parent
		case_value: how much value this case is worth,from 0-1, a trust value
			or even how effective it was
		ATTRIBUTE_MIN: min score to add attribute
		ACTIONS_MIN: Min score to add to actions
		ACTIONS_DONE_MIN: Min score to add to actions done
		ACTIONS_PRESCRIBE_MIN: min score to add to actions_prescribed
	#methods:
		#close_relation_value: is the close relation tester
			#input: other case
			#output: value representing closeness number
		#diference: returns what this attribute has but other attribute(s) don't or diferent
			#input: other case 
			#output: returns [attribute,action,actions_done,action_prescribe]
		#__init__:
			#input: attributes, actions, actions_done, action_prescribe, parent
		return_same:
			#input: other_case
			#output: return a case that has only the same
		write:
			#input: spacing
			#output: list of spacing plus __str__
			'''
	ATTRIBUTE_MIN = 1
	ACTIONS_MIN = 50
	ACTIONS_DONE_MIN = 17
	ACTION_PRESCRIBE_MIN = 1
	def __init__(self, attributes = None, actions = None,action_prescribe=None,
				parent = None,actions_done=None,other_case = None, case_value = 1):				
		
		self.attributes = attributes
		self.actions = actions
		self.action_prescribe = action_prescribe
		self.actions_done = actions_done
		self.parent = parent
		self.case_value = case_value
		if other_case:
			self.alt_init(other_case)
	def alt_init (self, other_case):
		self.attributes = other_case.attributes 
		self.actions = other_case.actions
		self.action_prescribe = other_case.action_prescribe
		self.actions_done = other_case.actions_done 
		self.parent = other_case.parent 
		self.case_value = other_case.case_value
	def __str__ (self):
		return "%s Attributes: %s || Actions: %s || Action Prescribe: %s || Actions Done: %s"%(self.NAME,self.attributes,
			self.actions,self.action_prescribe,self.actions_done)
	def close_relation (self,other_case):
		def tempFunction (partA,partB,values,minimum = 1, difference_min = 1):#returns match value for field(attributes or actions...)
			if partA:
				dtLPartA = []#Breaking dictionaries to lists, since values are lists (had problems)
				dtLPartB = []
				if ((partA is None) or (partB is None)):             #Nothing in list
					return 0
				for key in partA:
					for listItem in partA[key]:
						dtLPartA = dtLPartA + ["%s_%s"%(key,listItem)]
				for key in partB:
					for listItem in partB[key]:
						dtLPartB = dtLPartB + ["%s_%s"%(key,listItem)]
				difference_amount = len(filter(lambda q: q not in dtLPartB,dtLPartA)) #adding pure integers of size of differences
				difference_amount += len(filter(lambda q: q not in dtLPartA,dtLPartB))
				like = filter(lambda q: q in dtLPartB,dtLPartA) #making list of only same
				likeTimesValue = 0 #Creating value for each match
				for val in values.keys():
					likeTimesValue += sum(map(lambda a: values[val],filter(lambda test:"%s_"%(val) in test,like)))
				return len(like)*minimum+ likeTimesValue - difference_amount*difference_min #returns point value
			return 0
		total = 0														#Start value and run each section of data
		total += tempFunction(self.attributes,other_case.attributes,
				      self.ATTRIBUTE_VALUES,self.ATTRIBUTE_MIN,difference_min = self.ATTRIBUTE_MIN/10.0)
		total += tempFunction (self.actions,other_case.actions,
				       self.ACTIONS_VALUE,self.ACTIONS_MIN,difference_min = self.ACTIONS_MIN/10.0)
		total += tempFunction (self.actions_done,other_case.actions_done,
				       self.ACTIONS_DONE_VALUE,self.ACTIONS_DONE_MIN,difference_min = self.ACTIONS_DONE_MIN/10.0)
		return total * self.case_value * other_case.case_value
	def return_same (self, other_node):
		def dictAdder (first,second):
			returnDict = {}
			if len(first) == 0:
				if len(second) == 0:
					return dictAdder
				for key in second:
					if isinstance(second[key],type([])):
						returnDict[key] = second[key]
					else:
						returnDict[key] = [second[key]]
				return returnDict
				
			for key in first:
				if isinstance(first[key],type([])):
					returnDict[key] = first[key]
				else:
					returnDict[key] = [first[key]]
			for key in second:
				if key in first.keys():
					if not isinstance(second[key],type([])):							
						if second[key] not in returnDict [key]: #Make sure no duplicates
							returnDict [key] = returnDict[key] + [second[key]]
					else:
						for smallValue in second[key]:
							if smallValue not in returnDict [key]:
								returnDict [key] = returnDict[key] + [smallValue]
				else:
					if not isinstance(second[key],type([])):
						returnDict[key] = [second[key]]
					else:
						returnDict[key] = second[key]	
			return returnDict
		def tempFunction (partA,partB):
			if partA:
				dtLPartA = []#Breaking dictionaries to lists, since values are lists (had problems)
				dtLPartB = []
				
				if ((partA is None) or (partB is None)):             #Nothing in list
					return 0
				for key in partA:
					for listItem in partA[key]:
						dtLPartA = dtLPartA + [(key,listItem)]
				for key in partB:
					for listItem in partB[key]:
						dtLPartB = dtLPartB + [(key,listItem)]
						
				temp = filter(lambda small: small in dtLPartB,dtLPartA)   #make smaller list of similarities
				if len(temp) > 1:
					finalTemp = {}
					for small in temp:
						finalTemp = dictAdder(finalTemp,dict([small]))
					return finalTemp
				elif len(temp) == 0:
					return None
				else:
					temp = dict(temp)
					temp[temp.keys()[0]] = [temp[temp.keys()[0]]]
					return temp
		sim = [None]*4 #Get the differences ready to return
		sim[0] = tempFunction (self.attributes,other_node.attributes)
		if sim[0] == 0:
			sim[0] = None
		sim [1] = tempFunction(self.actions,other_node.actions)
		if sim[1] == 0:
			sim[1] = None
		sim [2]= tempFunction (self.actions_done,other_node.actions_done)
		if sim[2] == 0:
			sim[2] = None
		sim [3]= self.action_prescribe if self.action_prescribe == other_node.action_prescribe else None
		if sim[3] == 0:
			sim[3] = None
		temp = case(sim[0],sim[1],sim[3],None,sim[2],case_value = max([self.case_value,other_node.case_value]))
		return temp
	def difference (self, other_node):
		
		def tempFunction (partA,partB):
			if partA:
				dtLPartA = []#Breaking dictionaries to lists, since values are lists (had problems)
				dtLPartB = []
				if (partA is None):             #Nothing in list
					return []
				for key in partA:
					for listItem in partA[key]:
						dtLPartA = dtLPartA + ["%s_%s"%(key,listItem)]
				if (partB is None):
					return partA
				for key in partB:
					for listItem in partB[key]:
						dtLPartB = dtLPartB + ["%s_%s"%(key,listItem)]
				temp = filter(lambda small: small not in dtLPartB,dtLPartA)   #make smaller list of diferences
				if temp:
					return temp

		difference = [[None]]*4 #Get the differences ready to return
		difference[0] = tempFunction (self.attributes,other_node.attributes)
		difference [1] = tempFunction(self.actions,other_node.actions)
		difference [2]= tempFunction (self.actions_done,other_node.actions_done)
		difference [3]= self.action_prescribe if self.action_prescribe != other_node.action_prescribe else ""
		return case(attributes = difference[0],actions = difference[1],actions_done = difference[2],
					action_prescribe = difference[3])
	def write (self,spacing = "",default_spacing = "   "):
		answer = ["%s %s"%(spacing,self.NAME)]
		spacing = "".join([spacing,default_spacing])
		answer = answer + ["%sAttributes: %s"%(spacing,self.attributes)]
		answer = answer + ["%sActions: %s"%(spacing,self.actions)]
		answer = answer + ["%sAction Prescribe: %s"%(spacing,self.action_prescribe)]
		answer = answer + ["%sActions Done: %s"%(spacing,self.actions_done)]
		answer += ["%sTrust Value: %s"%(spacing,self.case_value)]
		return answer
	def isSame (self,other_case):
		myScore = self.similar (self)
		otherScore = other_case.similar(other_case)
		if myScore == otherScore:
			return self.similar (other_case) == myScore
		return False
	similar = close_relation
