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
    
def lookup (x, type):
	if type == "H":
		for player in awaydata:
			if player['ID'] == x:
				return player['Team']
		
		for player in homedata:
			if player['ID'] == x:
				return player['Team']

	else:
		for player in awaypitch:
			if player['ID'] == x:
				return player['Team']
		
		for player in homepitch:
			if player['ID'] == x:
				return player['Team']
    
def diceroll (bat, pitch):
	hitlastname = bat['LastName']
	x = random.randint(1, 108)
	if random.randint(1,1000) <= 500:
		if pitch['Throws'] == "R":
			if (pitch['s_bpvrhp'] == "w"):
				diamond = -1
			else:
				diamond = int(pitch['s_bpvrhp'])
			k = pitch['s_sovrhp']
			bb = pitch['s_bbvrhp']
			hr = pitch['s_hrvrhp']
			h = pitch['s_tbvrhp'] - (pitch['s_hrvrhp'] * 4)
			gidp = pitch['s_dpvrhp']
		else:
			if (pitch['s_bpvlhp'] == "w"):
				diamond = -1
			else:
				diamond = int(pitch['s_bpvlhp'])
			k = pitch['s_sovlhp']
			bb = pitch['s_bbvlhp']
			hr = pitch['s_hrvlhp']
			h = pitch['s_tbvlhp'] - (pitch['s_hrvlhp'] * 4)
			gidp = pitch['s_dpvlhp']
		
		lastname = pitch['LastName']
		id = pitch['ID']
	
		scope = [k, 
		(k + bb), 
		(bb + h),
		(bb + h + hr),
		(bb + h + hr + gidp)]
		
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
				print(hitlastname, "*Home Run")
				return False
			else:
				print(hitlastname, "*Fly Out")
				return True
			diamondcheck = False
		elif diamondx < (diamond + 8) and diamondx > diamond:
			if random.randint(1,20) < 11:
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
				#basepath[id,0,0]
				print(hitlastname, "Walk")
				return False
			elif x > scope[1] and x <= scope[2]:
				#bathpath[id,0,0]
				print(hitlastname, "Single")
				return False
			elif x > scope[2] and x <= scope[3]:
				print(hitlastname, "Home Run")
				return False
			elif x > scope[3] and x <= scope[4]:
				print(hitlastname, "GO - Double Play")
				return True
			else:
				print(hitlastname, "Groundout")
				return True
	
		#print(lookup(pitch["ID"], "P"))
			
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
			h = bat['s_tbvrhp'] - (bat['s_hrvrhp'] * 4)
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
			h = bat['s_tbvlhp'] - (bat['s_hrvlhp'] * 4)
			gidp = bat['s_dpvlhp']
	
		lastname = bat['LastName']
		id = bat['ID']
	
		scope = [k, 
		(k + bb), 
		(bb + h),
		(bb + h + hbp), 
		(bb + h + hbp + hr),
		(bb + h + hbp + hr + gidp)]
		
		diamondx = random.randint(1, 108)
		diamondcheck = True
		if diamondx <= diamond:
			if random.randint(1,20) < 11:
				print(lastname, "*Home Run")
				return False
			else:
				print(lastname, "*Fly Out")
				return True
			diamondcheck = False
		elif diamondx < (diamond + 8) and diamondx > diamond:
			if random.randint(1,20) < 11:
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
				#basepath = [id,0,0]
				print(lastname, "Walk")
				return False
			elif x > scope[1] and x <= scope[2]:
				#basepath = [id,0,0]
				print(lastname, "Single")
				return False
			elif x > scope[2] and x <= scope[3]:
				print(lastname, "Hit by Pitch")
				return False
			elif x > scope[3] and x <= scope[4]:
				print(lastname, "Home Run")
				return False
			elif x > scope[4] and x <= scope[5]:
				print(lastname, "GO - Double Play")
				return True
			else:
				print(lastname, "Groundout")
				return True
		
		#print(lookup(bat['ID'], 'H'))

	
	
		

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

for x in awaylineup:
	#position = "ex"
	posstring = x['s_fielding'].split("-")
	x['Position'] = posstring[0].upper()
	

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

while inning < 10:

	outs = 0
	print("")
	print("Away at Bat - Top", inning, homepitcher['LastName'])
	print("-----------")
	while outs < 3:
		outcheck = diceroll(awaylineup[awaycount], homepitcher)
		awaycount = awaycount + 1
		if outcheck:
			outs = outs + 1
		if awaycount == 9:
			awaycount = 0
	
	outs = 0
	print("")
	print("Home at Bat - Bottom", inning, awaypitcher['LastName'])
	print("-----------")
	while outs < 3:
		outcheck = diceroll(homelineup[homecount], awaypitcher)
		homecount = homecount + 1
		if outcheck:
			outs = outs + 1
		if homecount == 9:
			homecount = 0
			
	inning = inning + 1
			
		
#108 dice chances
