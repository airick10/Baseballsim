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

	# Check whether the distribution is mathematically valid
	if double < 0 or triple < 0 or h < 1:
	    print("WARNING: Cannot preserve HIT, TB, HR and minimum singles")

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

	# Check whether the distribution is mathematically valid
	if double < 0 or triple < 0 or h < 1:
	    print("WARNING: Cannot preserve HIT, TB, HR and minimum singles")


	player['s_sivlhp'] = single
	player['s_dovlhp'] = double
	player['s_trvlhp'] = triple

	return player
    
def lookup (x, type):
	if type == "H":
		for player in awaydata:
			if player['ID'] == x:
				return player['LastName']
		
		for player in homedata:
			if player['ID'] == x:
				return player['LastName']

	else:
		for player in awaypitch:
			if player['ID'] == x:
				return player['LastName']
		
		for player in homepitch:
			if player['ID'] == x:
				return player['LastName']
    
def diceroll (bat, pitch, score, inning):
	print("")
	print(lookup(basepath[0],"H"), lookup(basepath[1],"H"), lookup(basepath[2],"H"))
	hitlastname = bat['LastName']
	x = random.randint(1, 108)
	# PITCHER CARD
	if random.randint(1,1000) <= 500:
		if pitch['Throws'] == "R":
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
	
		scope = [k, 
		(k + bb), 
		(bb + si),
		(bb + si + hr),
		(bb + si + hr + gidp),
		(bb + si + hr + gidp + do),
		(bb + si + hr + gidp + do + tr)
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
				return False
			else:
				print(hitlastname, "*Fly Out")
				return True
			diamondcheck = False
		elif diamondx < (diamond + 8) and diamondx > diamond:
			if random.randint(1,20) < 11:
				single(bat, pitch, basepath, True, score, inning)
				print(hitlastname, "*Single")
				return False
			else:
				print(hitlastname, "*Groundout")
				return True
			diamondcheck = False
			
	
		if diamondcheck:
			if x > 0 and x <= scope[0]:
				print(hitlastname, "Strikeout")
				return True
			elif x > scope[0] and x <= scope[1]:
				walkhbp(bat, pitch, basepath, score, inning)
				print(hitlastname, "Walk")
				return False
			elif x > scope[1] and x <= scope[2]:
				single(bat, pitch, basepath, False, score, inning)
				print(hitlastname, "Single")
				return False
			elif x > scope[2] and x <= scope[3]:
				homerun(bat, pitch, basepath, score)
				print(hitlastname, "Home Run")
				return False
			elif x > scope[3] and x <= scope[4]:
				print(hitlastname, "GO - Double Play")
				return True
			elif x > scope[4] and x <= scope[5]:
				double(bat, pitch, basepath, False, score, inning)
				print(hitlastname, "Double")
				return False
			elif x > scope[6] and x <= scope[6]:
				walkhbp(bat, pitch, basepath, score, inning)
				print(hitlastname, "Triple")
				return False
			else:
				print(hitlastname, "Groundout")
				return True
	
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
				return False
			else:
				print(lastname, "*Fly Out")
				return True
			diamondcheck = False
		elif diamondx < (diamond + 8) and diamondx > diamond:
			if random.randint(1,20) < 11:
				single(bat, pitch, basepath, True, score, inning)
				print(lastname, "*Single")
				return False
			else:
				print(lastname, "*Groundout")
				return True
			diamondcheck = False
	
		if diamondcheck:
			if x > 0 and x <= scope[0]:
				print(lastname, "Strikeout")
				return True
			elif x > scope[0] and x <= scope[1]:
				walkhbp(bat, pitch, basepath, score, inning)
				print(lastname, "Walk")
				return False
			elif x > scope[1] and x <= scope[2]:
				single(bat, pitch, basepath, False, score, inning)
				print(lastname, "Single")
				return False
			elif x > scope[2] and x <= scope[3]:
				walkhbp(bat, pitch, basepath, score, inning)
				print(lastname, "Hit by Pitch")
				return False
			elif x > scope[3] and x <= scope[4]:
				homerun(bat, pitch, basepath, score, inning)
				print(lastname, "Home Run")
				return False
			elif x > scope[4] and x <= scope[5]:
				print(lastname, "GO - Double Play")
				return True
			elif x > scope[5] and x <= scope[6]:
				double(bat, pitch, basepath, False, score, inning)
				print(lastname, "Double")
				return False
			elif x > scope[6] and x <= scope[7]:
				triple(bat, pitch, basepath, score, inning)
				print(lastname, "Triple")
				return False
			else:
				print(lastname, "Groundout")
				return True
		
		#print(lookup(bat['ID'], 'H'))

def single(bat, pitch, basepath, onetick, score, inning):
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
		if basepath[2] > 0:
			runscored(basepath[2], score, inning)
			basepath[2] = 0
		if basepath[1] > 0:
			print("To Code...")
			# CODE - Open Single to score
			# basepath[2] = basepath[1]
			# basepath[1] = 0
		if basepath[0] > 0:
			print("To Code...")
			# Code - Open Single to advance
			# basepath[1] = basepath[0]
			# basepath[0] = 0
		basepath[0] = bat["ID"]

def double(bat, pitch, basepath, three, score, inning):
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
		if basepath[2] > 0:
			runscored(basepath[2], score, inning)
			basepath[2] = 0
		if basepath[1] > 0:
			runscored(basepath[1], score, inning)
			basepath[1] = 0
		if basepath[0] > 0:
			print("To Code...")
			# CODE - Open Double to score
			# basepath[2] = basepath[0]
		basepath[0] = 0
		basepath[1] = bat["ID"]

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
	else:
		basepath[0] = bat['ID']


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
#print(homelineup[1])

for x in homelineup:
	#position = "ex"
	posstring = x['s_fielding'].split("-")
	x['Position'] = posstring[0].upper()
	x = extrabases(x)

for x in awaylineup:
	#position = "ex"
	posstring = x['s_fielding'].split("-")
	x['Position'] = posstring[0].upper()
	x = extrabases(x)

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
	while outs < 3:
		outcheck = diceroll(awaylineup[awaycount], homepitcher, awayscore, inning)
		awaycount = awaycount + 1
		if outcheck:
			outs = outs + 1
		if awaycount == 9:
			awaycount = 0
	
	basepath=[0,0,0]
	outs = 0
	print("")
	print("Home at Bat - Bottom", inning, sum(awayscore), sum(homescore), awaypitcher['LastName'])
	print("-----------")
	while outs < 3:
		outcheck = diceroll(homelineup[homecount], awaypitcher, homescore, inning)
		homecount = homecount + 1
		if outcheck:
			outs = outs + 1
		if homecount == 9:
			homecount = 0
			
	inning = inning + 1
			
		
#108 dice chances
