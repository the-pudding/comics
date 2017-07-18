import pandas as pd
from pandas.io.json import json_normalize
import json
# import ijson
# from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
import codecs

# User input
# company="Marvel"	# 'Marvel', 'DC' or 'Big2' (both)
# company="DC"
company='Big2'		#Both DC and Marvel
numBins=200
showNumTeams=False
showNumMembers=False

# Initialize
marvelData='marvel_characters_complete.txt'
dcData='dc_characters_complete.txt'
output='teams_x_gender.json'
company=company.lower()
if(company=="marvel"):
	data=marvelData
elif(company=="dc"):
	data=dcData
elif(company=="big2"):
	pass
else:
	print("Warning: Company must be DC or Marvel")
	exit()
print("Company: %s"%company)
output=output.replace('.json','_%s.json'%company)

# Read data
print( "Opening the json file..." )
if(company=="big2"):
	json_str=json.load( open(dcData), encoding="utf-8" ) + json.load( open(marvelData), encoding="utf-8" )
else:
	json_str = json.load( open(data), encoding="utf-8" )
# pprint( json_str )

print( "Normalizing pandas ..." )
char_Table = json_normalize(json_str)

print( "List of columns: %s"%list(char_Table) )
print len(char_Table)

male=1
female=2
maleNumber = len(char_Table[char_Table['gender'].isin([male])])
femaleNumber = len(char_Table[char_Table['gender'].isin([female])])
otherNumber = len(char_Table)-maleNumber-femaleNumber

# Get a list of every single power (even duplicates)
listOfTeams=[]
totalTeamNum=[]
maleTeamNum=[]
maleTeamName=[]
femaleTeamNum=[]
femaleTeamName=[]
otherTeamNum=[]
otherTeamName=[]
# i is each character. It's going through powers for each character
for i in range(len(char_Table['teams'])):
	# j is going through specific powers for each character, i
	# print char_Table['name'][i]
	numTeams=len(char_Table['teams'][i])
	totalTeamNum.append( numTeams )
	if(char_Table['gender'][i]==male):
		maleTeamNum.append( numTeams )
	elif(char_Table['gender'][i]==female):
		femaleTeamNum.append( numTeams )
	else:
		otherTeamNum.append( numTeams )
	for j in range(numTeams):
		teamName=char_Table['teams'][i][j]['name']
		listOfTeams.append( teamName )
		if(char_Table['gender'][i]==male):
			maleTeamName.append( teamName )
		elif(char_Table['gender'][i]==female):
			femaleTeamName.append( teamName )
		else:
			otherTeamName.append( teamName )

if showNumTeams:
	print "Plotting..."
	minTotal=min(totalTeamNum)
	maxTotal=max(totalTeamNum)
	minMale=min(maleTeamNum)
	maxMale=max(maleTeamNum)
	minFemale=min(femaleTeamNum)
	maxFemale=max(femaleTeamNum)
	minOther=min(otherTeamNum)
	maxOther=max(otherTeamNum)
	# Make histograms of the number of teams characters are on
	plt.figure()
	plt.hist(totalTeamNum, bins=maxTotal-minTotal, normed=1, facecolor='b', alpha=0.5, range=(minTotal,maxTotal))
	plt.title("All genders")
	plt.xlabel(r'Number of teams a character is on')
	plt.ylabel(r'Counts')
	plt.figure()
	plt.hist(maleTeamNum, bins=maxMale-minMale, normed=1, facecolor='g', alpha=0.5, range=(minMale,maxMale))
	plt.title("Male characters")
	plt.xlabel(r'Number of teams a character is on')
	plt.ylabel(r'Counts')
	plt.figure()
	plt.hist(femaleTeamNum, bins=maxFemale-minFemale, normed=1, facecolor='r', alpha=0.5, range=(minFemale,maxFemale))
	plt.title("Female characters")
	plt.xlabel(r'Number of teams a character is on')
	plt.ylabel(r'Counts')
	plt.figure()
	plt.hist(otherTeamNum, bins=maxOther-minOther, normed=1, facecolor='y', alpha=0.5, range=(minOther,maxOther))
	plt.title("Other characters")
	plt.xlabel(r'Number of teams a character is on')
	plt.ylabel(r'Counts')

	plt.figure()
	plt.hist(totalTeamNum, bins=maxTotal-minTotal, normed=1, facecolor='b', alpha=0.5, range=(minTotal,maxTotal))
	plt.title("All genders")
	plt.xlabel(r'Number of teams a character is on')
	plt.ylabel(r'Counts')
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.figure()
	plt.hist(maleTeamNum, bins=maxMale-minMale, normed=1, facecolor='g', alpha=0.5, range=(minMale,maxMale))
	plt.title("Male characters")
	plt.xlabel(r'Number of teams a character is on')
	plt.ylabel(r'Counts')
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.figure()
	plt.hist(femaleTeamNum, bins=maxFemale-minFemale, normed=1, facecolor='r', alpha=0.5, range=(minFemale,maxFemale))
	plt.title("Female characters")
	plt.xlabel(r'Number of teams a character is on')
	plt.ylabel(r'Counts')
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.figure()
	plt.hist(otherTeamNum, bins=maxOther-minOther, normed=1, facecolor='y', alpha=0.5, range=(minOther,maxOther))
	plt.title("Other characters")
	plt.xlabel(r'Number of teams a character is on')
	plt.ylabel(r'Counts')
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')

	plt.figure()
	plt.hist(maleTeamNum, bins=maxMale-minMale, normed=1, facecolor='g', alpha=0.5, range=(minMale,maxMale), label="Male")
	plt.hist(femaleTeamNum, bins=maxFemale-minFemale, normed=1, facecolor='r', alpha=0.5, range=(minFemale,maxFemale), label="Female")
	plt.hist(otherTeamNum, bins=maxOther-minOther, normed=1, facecolor='y', alpha=0.5, range=(minOther,maxOther), label="Other")
	plt.title("All gendered characters")
	plt.xlabel(r'Number of teams a character is on')
	plt.ylabel(r'Counts')
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.legend(loc='best')
	plt.show()


print( "Analyzing teams and saving results..." )
uniqueTeams=list(set(listOfTeams))
numUnique=len(uniqueTeams)
print "Number of unique teams %d"%numUnique
numChar=np.zeros(numUnique,dtype=int)
numMale=np.zeros(numUnique,dtype=int)
numFemale=np.zeros(numUnique,dtype=int)
numOther=np.zeros(numUnique,dtype=int)
# print "%d teams"%numUnique
# print uniqueTeams
for team in listOfTeams:
	i = uniqueTeams.index(team)
	numChar[i]+=1
for team in maleTeamName:
	i = uniqueTeams.index(team)
	numMale[i]+=1
for team in femaleTeamName:
	i = uniqueTeams.index(team)
	numFemale[i]+=1
for team in otherTeamName:
	i = uniqueTeams.index(team)
	numOther[i]+=1
for i in range(numUnique):
	percentWomen=float(numFemale[i])/float(numChar[i])
	print( "%s: %d %d %d %d %f"%(uniqueTeams[i], numChar[i], numMale[i], numFemale[i], numOther[i], percentWomen) )

# Save the data as a json file
file=codecs.open(output, "w", "utf-8")
file.write('{"nodes":[\n')
for i in range(numUnique):
	percentWomen=float(numFemale[i])/float(numChar[i])
	file.write( '{"name":"%s","members":%d,"male":%d,"female":%d,"percent":%f'%(uniqueTeams[i], numChar[i], numMale[i], numFemale[i], percentWomen) )
	if(i==numUnique-1):
		file.write( '}\n' )
	else:
		file.write( '},\n' )
file.write(']}\n')

if showNumMembers:
	print "Plotting..."
	minTotal=min(numChar)
	maxTotal=max(numChar)
	minMale=min(numMale)
	maxMale=max(numMale)
	minFemale=min(numFemale)
	maxFemale=max(numFemale)
	minOther=min(numOther)
	maxOther=max(numOther)
	# Make histograms of the number of teams characters are on
	plt.figure()
	plt.hist(numChar, bins=maxTotal-minTotal, normed=1, facecolor='b', alpha=0.5, range=(minTotal,maxTotal))
	plt.title("All genders")
	plt.xlabel(r'Number of characters on a team')
	plt.ylabel(r'Counts')
	plt.figure()
	plt.hist(numMale, bins=maxMale-minMale, normed=1, facecolor='g', alpha=0.5, range=(minMale,maxMale))
	plt.title("Male characters")
	plt.xlabel(r'Number of characters on a team')
	plt.ylabel(r'Counts')
	plt.figure()
	plt.hist(numFemale, bins=maxFemale-minFemale, normed=1, facecolor='r', alpha=0.5, range=(minFemale,maxFemale))
	plt.title("Female characters")
	plt.xlabel(r'Number of characters on a team')
	plt.ylabel(r'Counts')
	plt.figure()
	plt.hist(numOther, bins=maxOther-minOther, normed=1, facecolor='y', alpha=0.5, range=(minOther,maxOther))
	plt.title("Other characters")
	plt.xlabel(r'Number of characters on a team')
	plt.ylabel(r'Counts')

	plt.figure()
	plt.hist(numChar, bins=maxTotal-minTotal, normed=1, facecolor='b', alpha=0.5, range=(minTotal,maxTotal))
	plt.title("All genders")
	plt.xlabel(r'Number of characters on a team')
	plt.ylabel(r'Counts')
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.figure()
	plt.hist(numMale, bins=maxMale-minMale, normed=1, facecolor='g', alpha=0.5, range=(minMale,maxMale))
	plt.title("Male characters")
	plt.xlabel(r'Number of characters on a team')
	plt.ylabel(r'Counts')
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.figure()
	plt.hist(numFemale, bins=maxFemale-minFemale, normed=1, facecolor='r', alpha=0.5, range=(minFemale,maxFemale))
	plt.title("Female characters")
	plt.xlabel(r'Number of characters on a team')
	plt.ylabel(r'Counts')
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.figure()
	plt.hist(numOther, bins=maxOther-minOther, normed=1, facecolor='y', alpha=0.5, range=(minOther,maxOther))
	plt.title("Other characters")
	plt.xlabel(r'Number of characters on a team')
	plt.ylabel(r'Counts')
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')

	plt.figure()
	plt.hist(numMale, bins=maxMale-minMale, normed=1, facecolor='g', alpha=0.5, range=(minMale,maxMale), label="Male")
	plt.hist(numFemale, bins=maxFemale-minFemale, normed=1, facecolor='r', alpha=0.5, range=(minFemale,maxFemale), label="Female")
	# plt.hist(numOther, bins=maxOther-minOther, normed=1, facecolor='y', alpha=0.5, range=(minOther,maxOther), label="Other")
	plt.title("All gendered characters")
	plt.xlabel(r'Number of characters on a team')
	plt.ylabel(r'Counts')
	plt.legend(loc='best')
	plt.figure()
	plt.hist(numMale, bins=maxMale-minMale, normed=1, facecolor='g', alpha=0.5, range=(minMale,maxMale), label="Male")
	plt.hist(numFemale, bins=maxFemale-minFemale, normed=1, facecolor='r', alpha=0.5, range=(minFemale,maxFemale), label="Female")
	plt.hist(numOther, bins=maxOther-minOther, normed=1, facecolor='y', alpha=0.5, range=(minOther,maxOther), label="Other")
	plt.title("All gendered characters")
	plt.xlabel(r'Number of characters on a team')
	plt.ylabel(r'Counts')
	plt.yscale('log', nonposy='clip')
	plt.xscale('log', nonposy='clip')
	plt.legend(loc='best')
	plt.show()
