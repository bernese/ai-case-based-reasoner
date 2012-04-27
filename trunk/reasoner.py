import case
import general_case
case = case.case
general_case = general_case.general_case
class reasoner ():
	'''data: 
		#case_holder: tree of case objects (the root of tree).
		#general_case: 
	#methods: 
		#add_case: create a new case, find best fit, check if need general (yes: create general), add in tree
		adaptation: Searches for a node that fits best,
			input: input case to find a case to return
			output:  case that matches the best, score, what is missing case, and what extra case
		#search: looks for a case that best fits case (A)
			#input: case A
			#output: closest case in data that matches, number that is close match, diference
		#case_generator: creates a case based on just a list of numbers
			#input: First list of four ints, second list of four ints, (and prescribe sol'n)
				first list: 
					0:Choice of os (0 is nothing)
					1: Choice of program (0 is nothing)
					2: choice of maintainProgram (0 is nothing)
					3: Choice of hardware (0 is nothing)
				second list:
					0:true/false to hardware/software
					1: true/false from above hardware/software ((hardware/software)/(program/maintainProgram))
					2: int what from above 
					3: int what problem to pair with
			#output: outputs a case based off of the input
		write: an way to output to a file, will format the return as list of strings
		'''
		
	MAKE_GENERAL_THRESHOLD = 20
	def write (self,spacing = ""):
		return self.root.write(spacing = spacing)
	def __init__ (self):
		temp = case(None,None)
		self.root = general_case(clone_case = temp)
	def search (self, case_to_find):
		layer_looking_at = [self.root]
		parent_start = None
		while layer_looking_at:	#While there are things to look at
			best_fit_score = -1.5
			best_case = None
			if layer_looking_at:
				for c in layer_looking_at:					#Find highest match on layer
					temp_score = case_to_find.close_relation(c)
					#print "test"
					if (temp_score > best_fit_score or best_fit_score == -1.5):
						best_fit_score = temp_score
						best_case = c
			if isinstance(best_case,general_case):	#If we need to go deeper
				layer_looking_at = best_case.children
				if best_case.parent != parent_start:
					print "#------->  Here is your problem)"
				parent_start = best_case
			else:
				layer_looking_at = []
		return best_case
	def add_case (self,case_add):
		layer_looking_at = [self.root]
		parent_start = None
		while layer_looking_at:	#While there are things to look at
			best_fit_score = -1
			best_case = None
			if layer_looking_at:
				for c in layer_looking_at:					#Find highest match on layer
					temp_score = case_add.close_relation(c)
					#print "test"
					if temp_score > best_fit_score:
						best_fit_score = temp_score
						best_case = c
			if isinstance(best_case,general_case):	#If we need to go deeper
				layer_looking_at = best_case.children
				if best_case.parent != parent_start:
					print "#------->  Here is your problem)"
				parent_start = best_case
				
			else:
				layer_looking_at = []
				
		if best_fit_score >= (self.MAKE_GENERAL_THRESHOLD): #Need to make general
			similar_case = case_add.return_same(best_case)
			parent_above = parent_start
			general_above = False
			while parent_above != None:
				if similar_case.similar(parent_above):
					general_above = True
					parent_above = None
				else:
					parent_above = parent_above.parent
			if general_above:         #New general is same as one above
				parent_start.add_kid(case_add)
			else:
				new_general = general_case(case_add.return_same(best_case))
				parent_start.add_kid (new_general)
				new_general.add_kid(case_add)
				new_general.add_kid(best_case)
		else:
			parent_start.add_kid(case_add)
	def __str__(self):
		return self.root.__str__()				
	def case_maker(self,attr_choose,act_choose,act_pres_choose=None,case_value = 1):
		import random
		case.ATTRIBUTE_VALUES = {"os":5,"program":10,"maintainProgram":3,"hardware":0}
		def dictAdder (first,second):
			returnDict = {}
			for key in first:
				returnDict[key] = first[key][:]
			for key in second:
				if key in first:
					if second[key][0] not in returnDict [key]:
						returnDict [key] = returnDict[key] + second[key]
				else:
					returnDict[key] = second[key][:]
			return returnDict
		#Attribute maker
		aOs = [{}]+map (lambda x: {"os":[x]},["linux","unix","mac","windows","other"])
		aP = [{}]+map (lambda x: {"program":[x]},["internet","wordProcessor",
					"game","music","movie", "other"])
		aMP =[{}]+ map (lambda x: {"maintainProgram":[x]},["antivirus","firewall","defragger",
					"other"])
		aH = [{}]+map (lambda x: {"hardware":[x]},["storage","ram",
							"removableStorage","processor","other"])
		aMaker = lambda w,x,y,z: dict( aOs[w%len(aOs)].items()+aP[x%len(aP)].items()+aMP[y%len(aMP)].items()+aH[z%len(aH)].items())

		#Activities maker
		actP = ["crashes","freezes","notStart","notSave","failsTask","other"]
		actH = ["noise","failure","notStartup","power","notVisible","other"]
		actPnH = [actP,actH]
		aChoices = [[aP,aMP],[aH,aOs]]
		def actPCreator (hardOr,aOrB,whichDict,whichProblem):
			comingFrom = aChoices[hardOr%2][aOrB%2]
			comingFrom = comingFrom[whichDict%len(comingFrom)]
			problem = actPnH[hardOr%2]
			problem = problem[whichProblem%len(problem)]
			if comingFrom:
				return {"%s-%s"%(comingFrom.keys()[0],comingFrom.values()[0]):[problem]}
			return {}

		actCreator = lambda x: reduce ( lambda a,b: dictAdder (a,b), 
			map(lambda blah:actPCreator(blah[0]%2,blah[1]%2,blah[2],blah[3]),x))

		#Case maker:
		attributes = None
		actions = None
		if attr_choose:
			attributes = reduce (lambda x,y:dictAdder(x,y), [aMaker(a[0],a[1],a[2],a[3]) for a in attr_choose])
		if act_choose:
			actions = actCreator(act_choose)
		return case(attributes,actions,act_pres_choose,case_value = case_value)
	def adaptation (self, other_case):
		import math
		best_fit = self.search(other_case)
		score = other_case.close_relation(best_fit)
		extra = other_case.difference (best_fit)
		missing = best_fit.difference (other_case)
		new_adaptation = case(other_case = other_case)
		bfMod = (best_fit.similar(best_fit))/3.0	
		new_adaptation.case_value = best_fit.case_value*(1-(math.e**(-score/bfMod)))
		if new_adaptation.case_value <= 0: 
			new_adaptation.case_value = 0.0000000001
		new_adaptation.action_prescribe = best_fit.action_prescribe
		return [best_fit,score,missing,extra,new_adaptation]
	def adaptation_case(self,other_case):
		import math
		best_fit = self.search(other_case)
		score = other_case.close_relation(best_fit)
		new_adaptation = case(other_case = other_case)
		bfMod = (best_fit.similar(best_fit))/3.0	
		new_adaptation.case_value = best_fit.case_value*(1-(math.e**(-score/bfMod)))
		if new_adaptation.case_value <= 0: 
			new_adaptation.case_value = 0.0000000001
		new_adaptation.action_prescribe = best_fit.action_prescribe
		return new_adaptation
	def adaptation_writer( self, other_case, space = "",space_extra = "    "):
		temp = self.adaptation(other_case)
		answer = []
		space_extra = "".join([space,space_extra])
		answer += ["%sOriginal Case: "%space]
		answer += other_case.write(spacing = space_extra)
		answer += ["%sBest Fit Case: "%space]
		answer += temp[0].write(spacing = space_extra)
		answer += ["%sBest Fit Case Score: %s" %(space,temp[1])]
		answer += ["%sMissing:"%space]
		answer += temp[2].write(spacing = space_extra)
		answer += ["%sExtra"%space]
		answer += temp[3].write(spacing = space_extra)
		answer += ["%sNew Adaptation Case: "%space]
		answer += temp [4]. write(spacing = space_extra)
		return answer
