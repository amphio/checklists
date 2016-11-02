from __future__ import print_function
import sys
import time
import json
import uuid
import subprocess
import sys
from collections import OrderedDict, namedtuple
from pprint import pprint


def run_checklist(items):
	"""
	Expects a checklist dict
	Returns that checklist with answers from user
	"""
	user_responses = OrderedDict()

	total_items = 0
	for item in items:
		total_items = total_items + 1
	
	#Ask questions
	current_item_number = 1
	for item in items:
		print ("%i of %i: " % (current_item_number, total_items) + item)
		answer = raw_input("> ")
		user_responses[item] = answer
		current_item_number = current_item_number + 1
	#Todo: Plain text Antyhing elsE?
	print ("\nChecklist complete.")
	return user_responses


def run_through_checklists(uncompleted_checklists, expected_responses = OrderedDict(), actual_responses = OrderedDict()):
	"""
	Expects a checklist list
	Returns that checklist with answers from user
	"""
	current_checklist = uncompleted_checklists.keys()[0]
	
	if current_checklist == "Context":
		response = "y"
	else:
		print ("\nWould you like to check " + current_checklist + "?")
		response = raw_input("(y/n) > ")

	if response == "y":
		expected_responses[current_checklist] = uncompleted_checklists[current_checklist]
		actual_responses[current_checklist] = run_checklist(uncompleted_checklists[current_checklist])
	else:
		pass

	#Remove this checklist
	del uncompleted_checklists[current_checklist]

	#Check if checklists exist
	if not uncompleted_checklists:
		#No more checklists found
		pass
	else:
		run_through_checklists(uncompleted_checklists)
	
	completed_checklists = {"expected_responses": expected_responses, "actual_responses": actual_responses}
	return (completed_checklists)


def check_answers(completed_checklists):
	test = completed_checklists["actual_responses"]
	correct_answers = completed_checklists["expected_responses"]


	test_results = {"Test passed":True, "Unexpected_behaviours": {}}
	section_failed = True
	for section in test:
		if section != "Context":
			for question in test[section]:
				if test[section][question] == correct_answers[section][question]:
					pass
				else:
					test_failed = False
					test_results["Unexpected_behaviours"][question] = test[section][question]
					test_results["Test passed"] = False
	return test_results


def dump_to_file(final_results):
	"""
	Writes results to json
	"""
	#Add prefix result
	if final_results["Results"]["Test passed"] == True:
		ouput_filepath = "results/PASSED_" + str(uuid.uuid1()) + ".json"
	else:
		ouput_filepath = "results/FAILED_" + str(uuid.uuid1()) + ".json"
	with open(ouput_filepath,  'w') as fp:
		json.dump(final_results, fp)
	return ouput_filepath


print ("""\n\n\n
               ,
         (`.  : \              __..----..__
          `.`.| |:          _,-':::''' '  `:`-._
            `.:\||       _,':::::'         `::::`-.
              \\`|    _,':::::::'     `:.     `':::`.
               ;` `-''  `::::::.                  `::
            ,-'      .::'  `:::::.         `::..    `:
          ,' /_) -.            `::.           `:.     |
        ,'.:     `    `:.        `:.     .::.          
   __,-'   ___,..-''-.  `:.        `.   /::::.         |
  |):'_,--'           `.    `::..       |::::::.      ::
   `-'                 |`--.:_::::|_____\::::::::.__  ::|
                       |   _/|::::|      \::::::|::/\  :|
                       /:./  |:::/        \__:::):/  \  :
                     ,'::'  /:::|        ,'::::/_/    `. ``-.__
                    ''''   (//|/       ,';':,-'         `-.__  `'--..__
                                                             `''---::::'
""")

#----------------------------------------------------
#PROCESS

#Filepath to checkslists json
checklists_filepath = "iso_checklists.json"

#Load checklist
with open(checklists_filepath) as test_file:    
	uncompleted_checklists = json.load(test_file, object_pairs_hook=OrderedDict)

#Welcome and list checklists
print ("WELCOME TO CHECKLISTS...")
print ('\nThe following checklists are available in %s: ' % checklists_filepath)
for keys in (uncompleted_checklists.keys()):
	print (keys)

#Ask for begin
print ("\nShall we begin?")
response = raw_input("(y/n) > ")
if response == "y":
	pass
else:
	print ("No checklists completed")
	sys.exit()

#Run the optional checklists
completed_checklists = run_through_checklists(uncompleted_checklists)
checklist_results = check_answers(completed_checklists)

#Print test results
print ("CHECKLIST RESULTS:")
pprint (checklist_results)

final_results = OrderedDict()
final_results["Results"] = checklist_results
final_results["actual_responses"] = completed_checklists["actual_responses"]

#Save test results
ouput_filepath = dump_to_file(final_results)
print ("\nTest results saved to: " + ouput_filepath)
print ("Please commit these results to GitHub...")
