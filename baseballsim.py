import json
import random
import math

with open("First_Tournament_Buccaneers_hitters.json", "r", encoding="utf-8") as file:
    awaydata = json.load(file)

with open("First_Tournament_Copperheads_hitters.json", "r", encoding="utf-8") as file:
    homedata = json.load(file)

with open("First_Tournament_Buccaneers_pitchers.json", "r", encoding="utf-8") as file:
    awaypitch = json.load(file)

with open("First_Tournament_Copperheads_pitchers.json", "r", encoding="utf-8") as file:
    homepitch = json.load(file)

with open("defense_rating.json", "r", encoding="utf-8") as file:
    defenseratingjson = json.load(file)

with open("e_rating.json", "r", encoding="utf-8") as file:
    eratingjson = json.load(file)
    
basepath = [0,0,0]

def extrabases(player):
	hr = player['s_hrvrhp']
	h = player['s_hitvrhp'] - hr
	tb = player['s_tbvrhp'] - (hr * 4)

	# Calculate extra bases from non-home-run hits
	extra = tb - h

	# Initial distribution (10:1 doubles to triples)
	triple = extra / 12
	double = triple * 10
	single = h - double - triple

	# Enforce minimum of 1 single chance
	if single < 1:
	    single = 1
	    triple = tb - (2 * h) + single
	    double = (3 * h) - tb - (2 * single)

	single = round(single, 4)
	double = round(double, 4)
	triple = round(triple, 4)

	# Check whether the distribution is mathematically valid
	if double < 0 or triple < 0 or h < 1:
	    print("WARNING vs RHP:", player['LastName'], "H:", h, "TB:", tb, "Single:", single, "Double:", double, "Triple:", triple)

	player['s_sivrhp'] = single
	player['s_dovrhp'] = double
	player['s_trvrhp'] = triple


	single = 0
	double = 0
	triple = 0
	hr = player['s_hrvlhp']
	h = player['s_hitvlhp'] - hr
	tb = player['s_tbvlhp'] - (hr * 4)

	# Calculate extra bases from non-home-run hits
	extra = tb - h

	# Initial distribution (10:1 doubles to triples)
	triple = extra / 12
	double = triple * 10
	single = h - double - triple

	# Enforce minimum of 1 single chance
	if single < 1:
	    single = 1
	    triple = tb - (2 * h) + single
	    double = (3 * h) - tb - (2 * single)

	single = round(single, 4)
	double = round(double, 4)
	triple = round(triple, 4)

	# Check whether the distribution is mathematically valid
	if double < 0 or triple < 0 or h < 1:
	    print("WARNING vs LHP:", player['LastName'], "H:", h, "TB:", tb, "Single:", single, "Double:", double, "Triple:", triple)


	player['s_sivlhp'] = single
	player['s_dovlhp'] = double
	player['s_trvlhp'] = triple

	return player
    
def lookup (x, type, category):
	if type == "H":
		for player in awaydata:
			if player['ID'] == x:
				return player[category]
		
		for player in homedata:
			if player['ID'] == x:
				return player[category]

	else:
		for player in awaypitch:
			if player['ID'] == x:
				return player[category]
		
		for player in homepitch:
			if player['ID'] == x:
				return player[category]

def defenseformation(player):
	lowerposition = player['Position'].lower()
	defensearray = [lowerposition,0,0,0]
	functionposition = "s_" + player['Position'].lower()
	if player['Position'] == "C":
		functionposition = "s_ca"
	elif player['Position'] == "P":
		functionposition = "s_p"


	#Get defenses.  // 100 gives the hundreds portion, discarding the remainder.
	#% 100 gives the remainder after division by 100.

	if player['Position'] != "P":
		rangerating = player[functionposition] // 100
		erating = player[functionposition] % 100
		arm = 0
		arminit = player['s_fielding'].split("(")

		# The if here is a check if the player even has an arm.  IF this is an infielder, arm would just be 0.
		if len(arminit) > 1:
			armarray = arminit[1].split(")")
			arm = int(armarray[0])
	else:
		rangerating = 3
		erating = 14
		arm = int(player['s_ho'])

	return defensearray


    
def diceroll (bat, pitch, score, inning, outs, currentdefense):
	print("")
	print(lookup(basepath[0],"H","LastName"), lookup(basepath[1],"H","LastName"), lookup(basepath[2],"H","LastName"))

	if (basepath[0] > 0 and basepath[1] == 0) or (basepath[1] > 0 and basepath[2] == 0):
		outs = stealing(outs,currentdefense)
		if outs == 3:
			return outs

	hitlastname = bat['LastName']
	x = random.randint(1, 108)
	# PITCHER CARD
	if random.randint(1,1000) <= 500:
		if pitch['Throws'] == "R":
			batside = "L"
			if (pitch['s_bpvrhp'] == "w"):
				diamond = -1
			else:
				diamond = int(pitch['s_bpvrhp'])
			k = pitch['s_sovrhp']
			bb = pitch['s_bbvrhp']
			si = pitch['s_sivrhp']
			do = pitch['s_dovrhp']
			tr = pitch['s_trvrhp']
			hr = pitch['s_hrvrhp']
			gidp = pitch['s_dpvrhp']
		else:
			batside = "R"
			if (pitch['s_bpvlhp'] == "w"):
				diamond = -1
			else:
				diamond = int(pitch['s_bpvlhp'])
			k = pitch['s_sovlhp']
			bb = pitch['s_bbvlhp']
			si = pitch['s_sivlhp']
			do = pitch['s_dovlhp']
			tr = pitch['s_trvlhp']
			hr = pitch['s_hrvlhp']
			gidp = pitch['s_dpvlhp']
		
		lastname = pitch['LastName']
		id = pitch['ID']
		defensex = 30	

		scope = [k, 
		(k + bb), 
		(bb + si),
		(bb + si + hr),
		(bb + si + hr + gidp),
		(bb + si + hr + gidp + do),
		(bb + si + hr + gidp + do + tr),
		(bb + si + hr + gidp + do + tr + defensex),
		]
		
		'''
		if x > 0 and x <= scope[0]:
			print(bat['LastName'], "Strikeout")
		elif x > scope[0] and x <= scope[1]:
			print(bat['LastName'], "Walk")
		elif x > scope[1] and x <= scope[2]:
			print(bat['LastName'], "Single")
		elif x > scope[2] and x <= scope[3]:
			print(bat['LastName'], "Home Run")
		else:
			print(bat['LastName'], "Groundout")
		'''
		
		diamondx = random.randint(1, 108)
		diamondcheck = True
		if diamondx <= diamond:
			if random.randint(1,20) < 11:
				homerun(bat, pitch, basepath, score, inning)
				print(hitlastname, "*Home Run")
			else:
				print(hitlastname, "*Fly Out")
				outs += 1
			diamondcheck = False
		elif diamondx < (diamond + 8) and diamondx > diamond:
			if random.randint(1,20) < 11:
				outs = single(bat, pitch, basepath, True, score, inning, outs, batside, currentdefense)
				print(hitlastname, "*Single")
			else:
				print(hitlastname, "*Lineout")
				outs += 1
			diamondcheck = False
			
	
		if diamondcheck:
			if x > 0 and x <= scope[0]:
				print(hitlastname, "Strikeout")
				outs += 1
			elif x > scope[0] and x <= scope[1]:
				walkhbp(bat, pitch, basepath, score, inning)
				print(hitlastname, "Walk")
			elif x > scope[1] and x <= scope[2]:
				outs = single(bat, pitch, basepath, False, score, inning, outs, batside, currentdefense)
				print(hitlastname, "Single")
			elif x > scope[2] and x <= scope[3]:
				homerun(bat, pitch, basepath, score, inning)
				print(hitlastname, "Home Run")
			elif x > scope[3] and x <= scope[4]:
				outs = gbA(bat, pitch, basepath, score, inning, outs)
				print(hitlastname, "GroundoutA")
			elif x > scope[4] and x <= scope[5]:
				outs = double(bat, pitch, basepath, False, score, inning, outs, batside, currentdefense)
				print(hitlastname, "Double")
			elif x > scope[5] and x <= scope[6]:
				triple(bat, pitch, basepath, score, inning)
				print(hitlastname, "Triple")
			elif x > scope[6] and x <= scope[7]:
				outs = xchart(bat, pitch, basepath, score, inning, outs, batside, currentdefense)
				print(hitlastname, "Defense X Chart")
			else:
				x = random.randint(1, 1000)
				if x >= 333:
					outs = gbC(bat, pitch, basepath, score, inning, outs)
					print(lastname, "GroundoutC")
				else:
					outs = gbB(bat, pitch, basepath, score, inning, outs)
					print(lastname, "GroundoutB")
		return outs
	
		#print(lookup(pitch["ID"], "P"))
	
	# HITTER CARD
	else:
		batside = bat['Bats']
		if batside == "S":
			if pitch['Throws'] == "R":
				batside = "L"
			else:
				batside = "R"
		if batside == "R":
			if (bat['s_bpvrhp'] == "w"):
				diamond = -1
			else:
				diamond = int(bat['s_bpvrhp'])
			k = bat['s_sovrhp']
			bb = bat['s_bbvrhp']
			hr = bat['s_hrvrhp']
			hbp = pitch['s_obvrhp'] - (pitch['s_hitvrhp'] + pitch['s_bbvrhp'])
			si = pitch['s_sivrhp']
			do = pitch['s_dovrhp']
			tr = pitch['s_trvrhp']
			gidp = bat['s_dpvrhp']
		else:
			if (bat['s_bpvlhp'] == "w"):
				diamond = -1
			else:
				diamond = int(bat['s_bpvlhp'])
			k = bat['s_sovlhp']
			bb = bat['s_bbvlhp']
			hr = bat['s_hrvlhp']
			hbp = pitch['s_obvlhp'] - (pitch['s_hitvlhp'] + pitch['s_bbvlhp'])
			si = pitch['s_sivlhp']
			do = pitch['s_dovlhp']
			tr = pitch['s_trvlhp']
			gidp = bat['s_dpvlhp']
	
		lastname = bat['LastName']
		id = bat['ID']
	
		scope = [k, 
		(k + bb), 
		(bb + si),
		(bb + si + hbp), 
		(bb + si + hbp + hr),
		(bb + si + hbp + hr + gidp),
		(bb + si + hbp + hr + gidp + do),
		(bb + si + hbp + hr + gidp + do + tr)
		]
		
		diamondx = random.randint(1, 108)
		diamondcheck = True
		if diamondx <= diamond:
			if random.randint(1,20) < 11:
				homerun(bat, pitch, basepath, score, inning)
				print(lastname, "*Home Run")
			else:
				print(lastname, "*Fly Out")
				outs += 1
			diamondcheck = False
		elif diamondx < (diamond + 8) and diamondx > diamond:
			if random.randint(1,20) < 11:
				outs = single(bat, pitch, basepath, True, score, inning, outs, batside, currentdefense)
				print(lastname, "*Single")
			else:
				print(lastname, "*Groundout")
				outs += 1
			diamondcheck = False
	
		if diamondcheck:
			if x > 0 and x <= scope[0]:
				print(lastname, "Strikeout")
				outs += 1
			elif x > scope[0] and x <= scope[1]:
				walkhbp(bat, pitch, basepath, score, inning)
				print(lastname, "Walk")
			elif x > scope[1] and x <= scope[2]:
				outs = single(bat, pitch, basepath, False, score, inning, outs, batside, currentdefense)
				print(lastname, "Single")
			elif x > scope[2] and x <= scope[3]:
				walkhbp(bat, pitch, basepath, score, inning)
				print(lastname, "Hit by Pitch")
			elif x > scope[3] and x <= scope[4]:
				homerun(bat, pitch, basepath, score, inning)
				print(lastname, "Home Run")
			elif x > scope[4] and x <= scope[5]:
				outs = gbA(bat, pitch, basepath, score, inning, outs)
				print(lastname, "GroundoutA")
			elif x > scope[5] and x <= scope[6]:
				outs = double(bat, pitch, basepath, False, score, inning, outs, batside, currentdefense)
				print(lastname, "Double")
			elif x > scope[6] and x <= scope[7]:
				triple(bat, pitch, basepath, score, inning)
				print(lastname, "Triple")
			else:
				x = random.randint(1, 1000)
				if x <= 333:
					outs = gbC(bat, pitch, basepath, score, inning, outs)
					print(lastname, "GroundoutC")
				else:
					outs = gbB(bat, pitch, basepath, score, inning, outs)
					print(lastname, "GroundoutB")

		return outs
		
		#print(lookup(bat['ID'], 'H'))

def single(bat, pitch, basepath, onetick, score, inning, outs, batside, currentdefense):
	x = random.randint(1, 1000)
	#Single*
	if x <= 333 or onetick:
		if basepath[2] > 0:
			runscored(basepath[2], score, inning)
			basepath[2] = 0
		if basepath[1] > 0:
			basepath[2] = basepath[1]
			basepath[1] = 0
		if basepath[0] > 0:
			basepath[1] = basepath[0]
			basepath[0] = 0
		basepath[0] = bat["ID"]
	#Single**
	elif x > 333 and x <= 667:
		if basepath[2] > 0:
			runscored(basepath[2], score, inning)
			basepath[2] = 0
		if basepath[1] > 0:
			runscored(basepath[1], score, inning)
			basepath[1] = 0
		if basepath[0] > 0:
			basepath[2] = basepath[0]
		basepath[0] = bat["ID"]
	#Open Single
	else:
		armroll = random.randint(1,5)
		if batside == "L":
			if armroll == 1:
				for y in currentdefense:
					if y['Position'] == "lf":
						arm = int(y['Arm'])
			elif armroll == 2 or armroll == 3:
				for y in currentdefense:
					if y['Position'] == "cf":
						arm = int(y['Arm'])
			else:
				for y in currentdefense:
					if y['Position'] == "rf":
						arm = int(y['Arm'])
		else:
			if armroll == 1:
				for y in currentdefense:
					if y['Position'] == "rf":
						arm = int(y['Arm'])
			elif armroll == 2 or armroll == 3:
				for y in currentdefense:
					if y['Position'] == "cf":
						arm = int(y['Arm'])
			else:
				for y in currentdefense:
					if y['Position'] == "lf":
						arm = int(y['Arm'])
		if basepath[2] > 0:
			runscored(basepath[2], score, inning)
			basepath[2] = 0
		if basepath[1] > 0:
			runnerspeed = lookup(basepath[1], "H", "s_spd")
			if outs == 2:
				toscore = runnerspeed - arm - 2
			else:
				toscore = runnerspeed - arm
			if toscore >= 10:
				if random.randint(1,20) <= toscore:
					runscored(basepath[1], score, inning)
					basepath[1] = 0
				else:
					outs += 1
					basepath[1] = 0
			else:
				basepath[2] = basepath[1]
				basepath[1] = 0
		if basepath[0] > 0:
			print("To Code...")
			# Code - Open Single to advance
			# basepath[1] = basepath[0]
			# basepath[0] = 0
		basepath[0] = bat["ID"]

	return outs

def double(bat, pitch, basepath, three, score, inning, outs, batside, currentdefense):
	x = random.randint(1, 1000)
	# If the rare three tick Double (Defense) is hit
	if three:
		if basepath[2] > 0:
			runscored(basepath[2], score, inning)
		if basepath[1] > 0:
			runscored(basepath[1], score, inning)
		if basepath[0] > 0:
			runscored(basepath[0], score, inning)
		basepath[0] = 0
		basepath[1] = bat["ID"]
	#Double**
	elif x <= 500:
		if basepath[2] > 0:
			runscored(basepath[2], score, inning)
			basepath[2] = 0
		if basepath[1] > 0:
			runscored(basepath[1], score, inning)
			basepath[1] = 0
		if basepath[0] > 0:
			basepath[2] = basepath[0]
		basepath[0] = 0
		basepath[1] = bat["ID"]
	#Open Double
	else:
		armroll = random.randint(1,5)
		if batside == "L":
			if armroll == 1:
				for y in currentdefense:
					if y['Position'] == "lf":
						arm = int(y['Arm'])
			elif armroll == 2 or armroll == 3:
				for y in currentdefense:
					if y['Position'] == "cf":
						arm = int(y['Arm'])
			else:
				for y in currentdefense:
					if y['Position'] == "rf":
						arm = int(y['Arm'])
		else:
			if armroll == 1:
				for y in currentdefense:
					if y['Position'] == "rf":
						arm = int(y['Arm'])
			elif armroll == 2 or armroll == 3:
				for y in currentdefense:
					if y['Position'] == "cf":
						arm = int(y['Arm'])
			else:
				for y in currentdefense:
					if y['Position'] == "lf":
						arm = int(y['Arm'])
		if basepath[2] > 0:
			runscored(basepath[2], score, inning)
			basepath[2] = 0
		if basepath[1] > 0:
			runscored(basepath[1], score, inning)
			basepath[1] = 0
		if basepath[0] > 0:
			runnerspeed = lookup(basepath[0], "H", "s_spd")
			if outs == 2:
				toscore = runnerspeed - arm - 2
			else:
				toscore = runnerspeed - arm
			if toscore >= 10:
				if random.randint(1,20) <= toscore:
					runscored(basepath[1], score, inning)
					basepath[0] = 0
				else:
					outs += 1
					basepath[0] = 0
			else:
				basepath[2] = basepath[0]
				basepath[0] = 0
		basepath[0] = 0
		basepath[1] = bat["ID"]

	return outs

def triple(bat, pitch, basepath, score, inning):
	if basepath[2] > 0:
		runscored(basepath[2], score, inning)
	if basepath[1] > 0:
		runscored(basepath[1], score, inning)
	if basepath[0] > 0:
		runscored(basepath[0], score, inning)
	basepath[1] = 0
	basepath[0] = 0
	basepath[2] = bat["ID"]

def homerun(bat, pitch, basepath, score, inning):
	if basepath[2] > 0:
		runscored(basepath[2], score, inning)
	if basepath[1] > 0:
		runscored(basepath[1], score, inning)
	if basepath[0] > 0:
		runscored(basepath[0], score, inning)
	runscored(bat['ID'], score, inning)
	basepath = [0,0,0]

def walkhbp(bat, pitch, basepath, score, inning):
	if basepath[2] > 0 and basepath[1] > 0 and basepath[0] > 0:
		runscored(basepath[2], score, inning)
		basepath[2] = basepath[1]
		basepath[1] = basepath[0]
		basepath[0] = bat["ID"]
	elif basepath[2] >= 0 and basepath[1] == 0 and basepath[0] > 0:
		basepath[1] = basepath[0]
		basepath[0] = bat["ID"]
	elif basepath[2] > 0 and basepath[1] >= 0 and basepath[0] == 0:
		basepath[0] = bat["ID"]
	elif basepath[2] == 0 and basepath[1] > 0 and basepath[0] > 0:
		basepath[2] = basepath[1]
		basepath[1] = basepath[0]
		basepath[0] = bat["ID"]
	elif basepath[2] == 0 and basepath[1] == 0 and basepath[0] > 0:
		basepath[1] = basepath[0]
		basepath[0] = bat["ID"]
	else:
		basepath[0] = bat['ID']

def stealing(outs, currentdefense):
	#Stealing
	if basepath[0] > 0 and basepath[1] == 0:
		for y in currentdefense:
			if y['Position'] in "p":
				pitchnum = int(y['Arm'])
			if y['Position'] in "c":
				catchnum = int(y['Arm'])
		pitchcatch = pitchnum + catchnum
		steal = lookup(basepath[0], "H", "s_stealing")
		runnerlastname = lookup(basepath[0], "H", "LastName")
		if "*" in steal:
			stealary = steal.split("/")
			firstnum = stealary[0]
			firstnum = firstnum.replace("*","")
			secondary = stealary[1].split(" ")
			secondnum = secondary[0]
			secondnum = secondnum.replace("-","0")

			paramsplitary = steal.split("(")
			paramsplit = paramsplitary[1].split("-")
			paramfirst = paramsplit[0]
			paramsecond = paramsplit[1].replace(")","")

			dicenumbers = []
			for part in firstnum.split(","):
			    if "-" in part:
			        start, end = part.split("-")
			       	dicenumbers.extend(range(int(start), int(end) + 1))
			    else:
			        dicenumbers.append(int(part))
			print(dicenumbers)

			tostealfirst = int(paramfirst) - int(pitchcatch) - 2
			tostealsecond = int(paramsecond) - int(pitchcatch) - 4


			if tostealfirst >= 14 or tostealsecond >=14:
				dtwenty = random.randint(1, 20)
				print(f"D20:{dtwenty} - StealNum:{tostealfirst}")
				if dtwenty <= tostealfirst:
					basepath[1] = basepath[0]
					basepath[0] = 0
					print("Stole Second Base")
					print(lookup(basepath[0],"H", "LastName"), lookup(basepath[1],"H", "LastName"), lookup(basepath[2],"H", "LastName"))
				else:
					basepath[0] = 0
					outs += 1
					print("Caught Stealing Second Base")
					print(lookup(basepath[0],"H", "LastName"), lookup(basepath[1],"H", "LastName"), lookup(basepath[2],"H", "LastName"))

	elif basepath[1] > 0 and basepath[2] == 0 and random.randint(1, 100) <= 20:
		for y in currentdefense:
			if y['Position'] in "p":
				pitchnum = int(y['Arm'])
			if y['Position'] in "c":
				catchnum = int(y['Arm'])
		pitchcatch = pitchnum + catchnum
		steal = lookup(basepath[1], "H", "s_stealing")
		runnerlastname = lookup(basepath[1], "H", "LastName")
		if "*" in steal:
			stealary = steal.split("/")
			firstnum = stealary[0]
			firstnum = firstnum.replace("*","")
			secondary = stealary[1].split(" ")
			secondnum = secondary[0]
			secondnum = secondnum.replace("-","0")

			paramsplitary = steal.split("(")
			paramsplit = paramsplitary[1].split("-")
			paramfirst = paramsplit[0]
			paramsecond = paramsplit[1].replace(")","")

			dicenumbers = []
			for part in firstnum.split(","):
				if "-" in part:
					start, end = part.split("-")
					dicenumbers.extend(range(int(start), int(end) + 1))
				else:
					dicenumbers.append(int(part))
			print(dicenumbers)

			tostealsecond = int(paramsecond) - int(pitchcatch) - 4


			if tostealsecond >= 14:
				dtwenty = random.randint(1, 20)
				print(f"D20:{dtwenty} - StealNum:{tostealfirst}")
				if dtwenty <= tostealfirst:
					basepath[2] = basepath[1]
					basepath[1] = 0
					print("Stole Third Base")
					print(lookup(basepath[0],"H", "LastName"), lookup(basepath[1],"H", "LastName"), lookup(basepath[2],"H", "LastName"))
				else:
					basepath[1] = 0
					outs += 1
					print("Caught Stealing Third Base")
					print(lookup(basepath[0],"H", "LastName"), lookup(basepath[1],"H", "LastName"), lookup(basepath[2],"H", "LastName"))
	return outs

def gbC(bat, pitch, basepath, score, inning, outs):
	if basepath[2] > 0 and basepath[1] > 0 and basepath[0] > 0:
		runscored(basepath[2], score, inning)
		basepath[2] = basepath[1]
		basepath[1] = basepath[0]
		basepath[0] = 0
	elif basepath[2] > 0 and basepath[1] == 0 and basepath[0] > 0:
		runscored(basepath[2], score, inning)
		basepath[1] = basepath[0]
		basepath[0] = 0
	elif basepath[2] > 0 and basepath[1] > 0 and basepath[0] == 0:
		runscored(basepath[2], score, inning)
		basepath[2] = basepath[1]
		basepath[1] = 0
	elif basepath[2] == 0 and basepath[1] > 0 and basepath[0] > 0:
		basepath[2] = basepath[1]
		basepath[1] = basepath[0]
		basepath[0] = 0
	elif basepath[2] == 0 and basepath[1] > 0 and basepath[0] == 0:
		basepath[2] = basepath[1]
		basepath[1] = 0
		basepath[0] = 0
	elif basepath[2] == 0 and basepath[1] == 0 and basepath[0] > 0:
		basepath[1] = basepath[0]
		basepath[0] = 0
	else:
		basepath[0] = 0
	outs += 1

	return outs


def gbB(bat, pitch, basepath, score, inning, outs):
	if basepath[2] > 0 and basepath[1] > 0 and basepath[0] > 0:
		runscored(basepath[2], score, inning)
		basepath[2] = basepath[1]
		basepath[1] = 0
		basepath[0] = bat["ID"]
	elif basepath[2] > 0 and basepath[1] == 0 and basepath[0] > 0:
		runscored(basepath[2], score, inning)
		basepath[2] = 0
		basepath[0] = bat["ID"]
	elif basepath[2] > 0 and basepath[1] > 0 and basepath[0] == 0:
		runscored(basepath[2], score, inning)
		basepath[2] = 0
		basepath[0] = bat["ID"]
	elif basepath[2] == 0 and basepath[1] > 0 and basepath[0] > 0:
		basepath[2] = basepath[1]
		basepath[1] = 0
		basepath[0] = bat["ID"]
	elif basepath[2] == 0 and basepath[1] == 0 and basepath[0] > 0:
		basepath[1] = 0
		basepath[0] = bat["ID"]
	else:
		basepath[0] = 0

	outs += 1

	return outs


def gbA(bat, pitch, basepath, score, inning, outs):
	dp = False
	if basepath[2] > 0 and basepath[1] > 0 and basepath[0] > 0:
		if outs == 0:
			runscored(basepath[2], score, inning)
			basepath[2] = basepath[1]
			basepath[1] = 0
			basepath[0] = 0
			dp = True
	elif basepath[2] > 0 and basepath[1] == 0 and basepath[0] > 0:
		if outs == 0:
			runscored(basepath[2], score, inning)
			basepath[2] = 0
			basepath[1] = 0
			basepath[0] = 0
			dp = True
	elif basepath[2] > 0 and basepath[1] > 0 and basepath[0] == 0:
		if outs < 3:
			runscored(basepath[2], score, inning)
			basepath[2] = 0
	elif basepath[2] == 0 and basepath[1] > 0 and basepath[0] > 0:
		if outs == 0:
			basepath[2] = basepath[1]
			basepath[1] = 0
			basepath[0] = 0
			dp = True
	elif basepath[2] == 0 and basepath[1] == 0 and basepath[0] > 0:
		if outs == 0:
			basepath[1] = 0
			basepath[0] = 0
			dp = True
	else:
		basepath[0] = 0

	if dp:
		outs += 2
	else:
		outs += 1

	return outs


def xchart(bat, pitch, basepath, score, inning, outs, batside, currentdefense):
	#positionshort = bat['Postion'].lower()
	x = random.randint(1, 30)
	rangerating = str(random.randint(1,5))
	eratingrat = str(random.randint(8,30))
	debug =" "

	rangeratingroll = str(random.randint(1,20))
	eratingroll = str(random.randint(1,6) + random.randint(1,6))
	if x <= 3:
		for player in currentdefense:
		    if player["Position"] == "c":
		        rangerating = str(player["Range"])
		        eratingrat = str(player["ERating"])
		        lastname = player['LastName']
		        break
		#result = defenseratingjson[bat['Position']][range_rating][roll]
		#result = eratingjson[bat['Position']][f"e{erating}"][str(roll)]
		result = defenseratingjson["c"][rangerating][rangeratingroll]
		if result == "e":
			result = eratingjson["c"][eratingrat][eratingroll]
		print(f"Catcher X - {lastname} - {result}")
	elif x == 4:
		for player in currentdefense:
		    if player["Position"] == "1b":
		        rangerating = str(player["Range"])
		        eratingrat = str(player["ERating"])
		        lastname = player['LastName']
		        break
		result = defenseratingjson["1b"][rangerating][rangeratingroll]
		if result == "e":
			result = eratingjson["1b"][eratingrat][eratingroll]
		print(f"First Base X - {lastname} - {result}")
	elif x > 4 and x < 12:
		for player in currentdefense:
		    if player["Position"] == "2b":
		        rangerating = str(player["Range"])
		        eratingrat = str(player["ERating"])
		        lastname = player['LastName']
		        break
		result = defenseratingjson["2b"][rangerating][rangeratingroll]
		if result == "e":
			result = eratingjson["2b"][eratingrat][eratingroll]
		print(f"Second Base X - {lastname} - {result}")
	elif x > 11 and x < 20:
		for player in currentdefense:
		    if player["Position"] == "ss":
		        rangerating = str(player["Range"])
		        eratingrat = str(player["ERating"])
		        lastname = player['LastName']
		        break
		result = defenseratingjson["ss"][rangerating][rangeratingroll]
		if result == "e":
			result = eratingjson["ss"][eratingrat][eratingroll]
		print(f"Shortstop X - {lastname} - {result}")
	elif x > 19 and x < 22:
		for player in currentdefense:
		    if player["Position"] == "3b":
		        rangerating = str(player["Range"])
		        eratingrat = str(player["ERating"])
		        lastname = player['LastName']
		        break
		result = defenseratingjson["3b"][rangerating][rangeratingroll]
		if result == "e":
			result = eratingjson["3b"][eratingrat][eratingroll]
		print(f"Third Base X - {lastname} - {result}")
	elif x > 21 and x < 24:
		for player in currentdefense:
		    if player["Position"] == "lf":
		        rangerating = str(player["Range"])
		        eratingrat = str(player["ERating"])
		        lastname = player['LastName']
		        break
		result = defenseratingjson["lf"][rangerating][rangeratingroll]
		if result == "e":
			result = eratingjson["lf"][eratingrat][eratingroll]
		print(f"Left Field X - {lastname} - {result}")
	elif x > 23 and x < 27:
		for player in currentdefense:
		    if player["Position"] == "cf":
		        rangerating = str(player["Range"])
		        eratingrat = str(player["ERating"])
		        lastname = player['LastName']
		        break
		result = defenseratingjson["cf"][rangerating][rangeratingroll]
		if result == "e":
			result = eratingjson["cf"][eratingrat][eratingroll]
		print(f"Center Field X - {lastname} - {result}")
	elif x > 26 and x < 29:
		for player in currentdefense:
		    if player["Position"] == "rf":
		        rangerating = str(player["Range"])
		        eratingrat = str(player["ERating"])
		        lastname = player['LastName']
		        break
		result = defenseratingjson["rf"][rangerating][rangeratingroll]
		if result == "e":
			result = eratingjson["rf"][eratingrat][eratingroll]
		print(f"Right Field X - {lastname} - {result}")
	else:
		for player in currentdefense:
		    if player["Position"] == "p":
		        rangerating = str(player["Range"])
		        eratingrat = str(player["ERating"])
		        lastname = player['LastName']
		        break
		result = defenseratingjson["p"][rangerating][rangeratingroll]
		if result == "e":
			result = eratingjson["p"][eratingrat][eratingroll]
		print(f"Pitcher X - {lastname} - {result}")



	if "SI" in result:
		if result.count("*") == 1:
			outs = single(bat, pitch, basepath, True, score, inning, outs, batside, currentdefense)
		else:
			outs = single(bat, pitch, basepath, False, score, inning, outs, batside, currentdefense)
	elif "DO" in result:
		if result.count("*") == 3:
			outs = double(bat, pitch, basepath, True, score, inning, outs, batside, currentdefense)
		else:
			outs = double(bat, pitch, basepath, False, score, inning, outs, batside, currentdefense)
	elif "TR" in result:
		triple(bat, pitch, basepath, score, inning)
	elif "e" in result:
		print("Error Check")
		if result[1:2] == "1":
			outs = single(bat, pitch, basepath, False, score, inning, outs, batside, currentdefense)
		elif result[1:2] == "2":
			outs = double(bat, pitch, basepath, False, score, inning, outs, batside, currentdefense)
		else:
			triple(bat, pitch, basepath, score, inning)
	elif "gbA" in result:
		outs = gbA(bat, pitch, basepath, score, inning, outs)
	elif "gbB" in result:
		outs = gbB(bat, pitch, basepath, score, inning, outs)
	elif "gbC" in result:
		outs = gbC(bat, pitch, basepath, score, inning, outs)

	else:
		print("X Rating - Out")

	return outs



def runscored(runner, score, inning):	
	print("*** RUN SCORED ***")
	trueinning = inning - 1
	score[trueinning] = score[trueinning] + 1


#print(data[0]['FirstName'] + ' ' + data[0]['LastName'])
#print(data[0]['s_mlbteam'][1])        # Gotham Knights
#print(data[0]['s_war'])
'''
awayb1 = awaydata[0]
awayb2 = awaydata[1]
awayb3 = awaydata[2]
awayb4 = awaydata[3]
awayb5 = awaydata[4]
awayb6 = awaydata[5]
awayb7 = awaydata[6]
awayb8 = awaydata[7]
awayb9 = awaydata[8]

homeb1 = homedata[0]
homeb2 = homedata[1]
homeb3 = homedata[2]
homeb4 = homedata[3]
homeb5 = homedata[4]
homeb6 = homedata[5]
homeb7 = homedata[6]
homeb8 = homedata[7]
homeb9 = homedata[8]
'''

homelineup = []
awaylineup = []
count = 0
while count < 9:
	homelineup.append(homedata[count])
	awaylineup.append(awaydata[count])
	count = count + 1

homepitcher = homepitch[0]
awaypitcher = awaypitch[0]
homepitcher['Position'] = "P"
awaypitcher['Position'] = "P"
#print(homelineup[1])

#home_defense = []
home_defense = [{"ID": 38, "FirstName": "Ernie", "LastName": "Banks", "Position": "ss", "Range": 2, "ERating": 19, "Arm": 0},
				{"ID": 47, "FirstName": "Albert", "LastName": "Belle", "Position": "lf", "Range": 3, "ERating": 8, "Arm": 0},
				{"ID": 491, "FirstName": "Ryne", "LastName": "Sandberg", "Position": "2b", "Range": 1, "ERating": 8, "Arm": 0},
				{"ID": 312, "FirstName": "Jason", "LastName": "Kendall", "Position": "c", "Range": 3, "ERating": 3, "Arm": 0},
				{"ID": 482, "FirstName": "Pete", "LastName": "Rose", "Position": "3b", "Range": 3, "ERating": 16, "Arm": 0},
				{"ID": 228, "FirstName": "Juan", "LastName": "Gonzalez", "Position": "rf", "Range": 3, "ERating": 10, "Arm": 0},
				{"ID": 573, "FirstName": "Mo", "LastName": "Vaughn", "Position": "1b", "Range": 4, "ERating": 7, "Arm": 0},
				{"ID": 88, "FirstName": "Brett", "LastName": "Butler", "Position": "cf", "Range": 2, "ERating": 3, "Arm": 0}
				]
#away_defense = []
away_defense = [{"ID": 554, "FirstName": "Jim", "LastName": "Thome", "Position": "1b", "Range": 4, "ERating": 10, "Arm": 0},
				{"ID": 315, "FirstName": "Harmon", "LastName": "Killebrew", "Position": "3b", "Range": 4, "ERating": 26, "Arm": 0},
				{"ID": 506, "FirstName": "Corey", "LastName": "Seager", "Position": "ss", "Range": 3, "ERating": 10, "Arm": 0},
				{"ID": 552, "FirstName": "Mickey", "LastName": "Tettleton", "Position": "c", "Range": 3, "ERating": 1, "Arm": 0},
				{"ID": 117, "FirstName": "Jazz", "LastName": "Chisholm, Jr.", "Position": "2b", "Range": 2, "ERating": 20, "Arm": 0},
				{"ID": 462, "FirstName": "Bryan", "LastName": "Reynolds", "Position": "rf", "Range": 4, "ERating": 2, "Arm": -1},
				{"ID": 158, "FirstName": "Willie", "LastName": "Davis", "Position": "cf", "Range": 2, "ERating": 8, "Arm": -1},
				{"ID": 269, "FirstName": "Bobby", "LastName": "Higginson", "Position": "lf", "Range": 2, "ERating": 9, "Arm": -2}
				]

current_defense = []
for x in homelineup:
	#position = "ex"
	posstring = x['s_fielding'].split("-")
	x['Position'] = posstring[0].upper()
	x = extrabases(x)
	#y = (defenseformation(x))
	#home_defense.append({"ID": x['ID'], "FirstName": x['FirstName'], "LastName": x['LastName'], "Position": y[0], "Range": y[1], "ERating": y[2], "Arm": y[3]})
#y = (defenseformation(homepitcher))
#home_defense.append({"ID": homepitcher['ID'], "FirstName": homepitcher['FirstName'], "LastName": homepitcher['LastName'], "Position": y[0], "Range": y[1], "ERating": y[2], "Arm": y[3]})
home_defense.append({"ID": 296, "FirstName": "Satchel", "LastName": "Paige", "Position": "p", "Range": 2, "ERating": 10, "Arm": 0})

for x in awaylineup:
	#position = "ex"
	posstring = x['s_fielding'].split("-")
	x['Position'] = posstring[0].upper()
	x = extrabases(x)
	#y = (defenseformation(x))
	#away_defense.append({"ID": x['ID'], "FirstName": x['FirstName'], "LastName": x['LastName'], "Position": y[0], "Range": y[1], "ERating": y[2], "Arm": y[3]})
#y = (defenseformation(awaypitcher))
#away_defense.append({"ID": awaypitcher['ID'], "FirstName": awaypitcher['FirstName'], "LastName": awaypitcher['LastName'], "Position": y[0], "Range": y[1], "ERating": y[2], "Arm": y[3]})
away_defense.append({"ID": 356, "FirstName": "Babe", "LastName": "Ruth", "Position": "p", "Range": 1, "ERating": 16, "Arm": -3})


for x in homepitch:
	x = extrabases(x)

for x in awaypitch:
	x = extrabases(x)

	

lineupcount = 0
count = 1

while count < 10: 
	print(count, homelineup[lineupcount]['Position'], homelineup[lineupcount]['FirstName'], homelineup[lineupcount]['LastName'], homelineup[lineupcount]['b_batting_avg'], homelineup[lineupcount]['b_hr'], homelineup[lineupcount]['b_rbi'])
	count = count + 1
	lineupcount = lineupcount + 1

print("SP",homepitcher['FirstName'],homepitcher['LastName'])
print("")

lineupcount = 0	
count = 1
while count < 10:
	print(count, awaylineup[lineupcount]['Position'], awaylineup[lineupcount]['FirstName'], awaylineup[lineupcount]['LastName'], awaylineup[lineupcount]['b_batting_avg'], awaylineup[lineupcount]['b_hr'], awaylineup[lineupcount]['b_rbi'])
	count = count + 1
	lineupcount = lineupcount + 1
	
print("SP",awaypitcher['FirstName'],awaypitcher['LastName'])


outs = 0
inning = 1
awaycount = 0
homecount = 0
homescore = [0,0,0,0,0,0,0,0,0]
awayscore = [0,0,0,0,0,0,0,0,0]
while inning < 10:

	basepath=[0,0,0]
	outs = 0
	print("")
	print("Away at Bat - Top", inning, sum(awayscore), sum(homescore), homepitcher['LastName'])
	print("-----------")
	current_defense = home_defense
	while outs < 3:
		outs = diceroll(awaylineup[awaycount], homepitcher, awayscore, inning, outs, current_defense)
		awaycount = awaycount + 1
		if awaycount == 9:
			awaycount = 0
	
	basepath=[0,0,0]
	outs = 0
	print("")
	print("Home at Bat - Bottom", inning, sum(awayscore), sum(homescore), awaypitcher['LastName'])
	print("-----------")
	current_defense = away_defense
	while outs < 3:
		outs = diceroll(homelineup[homecount], awaypitcher, homescore, inning, outs, current_defense)
		homecount = homecount + 1
		if homecount == 9:
			homecount = 0
			
	inning = inning + 1
			
		
#108 dice chances







	

