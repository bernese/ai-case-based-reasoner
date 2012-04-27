import case,reasoner,general_case,random
reasoner = reasoner.reasoner
general_case = general_case.general_case
case = case.case
caseBase = reasoner ()
def initializeReasoner ():
	#Setup the os cases
	OSs = ["linux","unix","windows","mac","other"]
	probSolution = [("slow","Run the anti-virus, anti-spyware, and defragmenter on the system."),
					("notStart","Try use your OS installation to either recover, or reinstall and use data from backup."),
					("fails","It it can be started again, backup all the data. Else, try and recover the OS.")]
	for os in OSs:
		for pS in probSolution:		
			temp = case(attributes = {"os":[os]},actions = {"os-%s"%os:[pS[0]]},action_prescribe = pS[1])
			caseBase.add_case(temp)
	
		caseBase.add_case(case(attributes = {"os":[os],"program":["internet"]},actions = {"program-internet":["slow"]},
		action_prescribe = "Use anti-virus, remove all toolbars, and run a internet speed test. If the internet speed is nothing or low then talk to your service provider."))
		caseBase.add_case(case(attributes = {"os":[os],"program":["internet"]},actions = {"program-internet":["fails"]},
					action_prescribe = "Use anti-virus, remove all toolbars, and run a internet speed test. If the internet speed is nothing or low then talk to your service provider. Might want to try a different browser."))
		caseBase.add_case(case(attributes = {"os":[os],"program":["internet"]},actions = {"program-internet":["notStart"]},
					action_prescribe = "If you can try an alternative browser, use the alternative browser. If that doesn't fix it, use other assistance."))
					
		#Memory storage
		memories = ["harddrive","removableStorage","cd"]
		for mem in memories:
			caseBase.add_case(case(attributes = {"os":[os],"hardware":[mem]},actions = {"hardware-%s"%mem:["noise"]},
						action_prescribe = "May want to backup and look for a new %s."%mem))
			caseBase.add_case(case(attributes = {"os":[os],"hardware":[mem]},actions = {"hardware-%s"%mem:["notVisible"]},
						action_prescribe = "Try blowing the dust out of the connectors to the device and same cable to its other side."))
		
initializeReasoner()
def myTest ():
	outText = ["Original tree"]
	outText += caseBase.write(spacing = "   ")
	testCase = case(attributes = {"os":["other"]},actions = {"program-movie":["crashes"]})
	outText += ["Trust value should be 0.0000000001 for adaptation case"]+caseBase.adaptation_writer(testCase,space = "   ")
	#Going to add adaptation case in System
	temp = caseBase.adaptation_case(testCase)
	caseBase.add_case (temp)
	outText += ["This should be interesting, searching for testCase A again, should be slightly smaller than .0000000001 or same"]+caseBase.adaptation_writer(testCase,space = "   ")
	testCase = case(attributes = {"os":["linux"],"hardware":["harddrive"]},actions = {"hardware-harddrive":["fails","noise"]})
	outText += ["Trust value should be around .90 for adaptation case"]+caseBase.adaptation_writer(testCase,space = "   ")
	testCase = case(attributes = {"os":["windows"]},actions = {"os-windows":["slow"]})
	outText += ["Trust value should be around .95"]+caseBase.adaptation_writer(testCase,space = "   ")
	testCase = case(attributes = {"os":["windows"]})
	outText += ["This is the case with just an atrribute, which should be less than 10%"]+caseBase.adaptation_writer(testCase,space = "   ")
	testCase = case()
	outText += ["This is the case of nothing, should be .0000000001"]+caseBase.adaptation_writer(testCase,space = "   ")
	f = open("finalTest.txt",'w')
	for line in outText:
		f.write("%s\n"%line)
	f.close()
myTest()
