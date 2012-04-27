import case
case = case.case
class general_case (case):
	'''#
	inherits:
		case
	data: Extra
		children
	methods:
		add_kid
		remove_kid
		write
	'''
	NAME = "general case"
	def __init__(self, clone_case,kids = []):
		case.__init__(self,other_case = clone_case)
		self.children = kids
	def add_kid (self,new_kid):
		if new_kid.case_value > self.case_value:
			self.case_value = new_kid.case_value       # going to make sure that it has the highest trust of kid
		if self.children is None:
			self.children = []
		self.children = self.children + [new_kid]
		if new_kid.parent: 			#if kid has parent
			new_kid.parent.remove_kid(new_kid)
		new_kid.parent = self
	def remove_kid (self,rem_kid):
		self.children.remove(rem_kid)
	def __str__ (self):
		children_string = [kid.__str__() for kid in self.children]
		return "This case is moddeled on %s with children of %s"%(case.__str__(self),children_string)
	def write (self,spacing = "",default_spacing = "   "):
		start = case.write(self,spacing,default_spacing)
		space = "".join([spacing,default_spacing])
		for child in self.children:
			start = start + child.write(spacing=space,default_spacing=default_spacing)
		return start
