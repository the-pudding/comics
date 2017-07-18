import pandas as pd
from pandas.io.json import json_normalize
import json
# import ijson
# from pprint import pprint
import matplotlib.pyplot as plt

# User input
# company="Marvel"	# 'Marvel', 'DC' or 'Big2' (both)
# company="DC"
company='Big2'		#Both DC and Marvel

# Initialize
marvelData='marvel_characters_complete.txt'
dcData='dc_characters_complete.txt'
output='powers_x_gender_fixed.csv'
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
output=output.replace('.csv','_%s.csv'%company)

# Read data
print( "Opening the json file..." )
if(company=="big2"):
	json_str=json.load( open(dcData), encoding="utf-8" ) + json.load( open(marvelData), encoding="utf-8" )
else:
	json_str = json.load( open(data), encoding="utf-8" )
# pprint( json_str )

print( "Normalizing pandas..." )
char_Table = json_normalize(json_str)

# print( "List of columns: %s"%list(char_Table) )
male=1
female=2
allNumber = len(char_Table)
maleNumber = len(char_Table[char_Table['gender'].isin([male])])
femaleNumber = len(char_Table[char_Table['gender'].isin([female])])
otherNumber = len(char_Table)-maleNumber-femaleNumber

# Get a list of every single power (even duplicates)
listOfPowers=[]
malePowers=[]
femalePowers=[]
otherPowers=[]
powersCnt=0.0
malePowersCnt=0.0
femalePowersCnt=0.0
otherPowersCnt=0.0
# i is each character. It's going through powers for each character
for i in range(len(char_Table['powers'])):
	# j is going through specific powers for each character, i
	for j in range(len(char_Table['powers'][i])):
		listOfPowers.append( char_Table['powers'][i][j]['name'] )
		if(char_Table['gender'][i]==male):
			malePowers.append( char_Table['powers'][i][j]['name'] )
		elif(char_Table['gender'][i]==female):
			femalePowers.append( char_Table['powers'][i][j]['name'] )
		else:
			otherPowers.append( char_Table['powers'][i][j]['name'] )
	if(len(char_Table['powers'][i])>0):
		powersCnt+=1.0
		if(char_Table['gender'][i]==male):
			malePowersCnt+=1.0
		elif(char_Table['gender'][i]==female):
			femalePowersCnt+=1.0
		else:
			otherPowersCnt+=1.0
# Analyze and save the statistics on powers by gender
file=open(output,'w')
file.write("power\tnum_males\tnum_females\tnum_other\tper_males\tper_females\tper_other\tperdiffMF\n")
uniquePowers=list(set(listOfPowers))
# print uniquePowers
print( "Analyzing powers and saving results..." )
for i in range(len(uniquePowers)):
	cntmale=malePowers.count( uniquePowers[i] )
	cntfemale=femalePowers.count( uniquePowers[i] )
	cntother=otherPowers.count( uniquePowers[i] )
	print "%s:\n\t# of males=%d; females=%d; other=%d"%(uniquePowers[i],cntmale,cntfemale,cntother )
	percentmale=100.0*float(cntmale)/float(maleNumber)
	percentfemale=100.0*float(cntfemale)/float(femaleNumber)
	percentother=100.0*float(cntother)/float(otherNumber)
	print "\t%% of males=%f; females=%f; other=%f"%(percentmale, percentfemale, percentother)
	percentmalePowers=100.0*float(cntmale)/float(malePowersCnt)
	percentfemalePowers=100.0*float(cntfemale)/float(femalePowersCnt)
	percentotherPowers=100.0*float(cntother)/float(otherPowersCnt)
	print "\t%% with powers of males=%f; females=%f; other=%f"%(percentmalePowers, percentfemalePowers, percentotherPowers)
	perdiff=100.0*(percentmalePowers-percentfemalePowers)/percentmalePowers
	perdiffOther=100.0*(percentmalePowers-percentotherPowers)/percentmalePowers
	print "\t%% diffMF %f"%(perdiff)
	print "\t%% diffOther %f"%(perdiffOther)
	file.write('"%s"\t%d\t%d\t%d\t%f\t%f\t%f\t%f\n'%(uniquePowers[i],cntmale,cntfemale,cntother,percentmalePowers,percentfemalePowers,percentotherPowers,perdiff))

file.close()


# Performing T-test to see if differences in gender have statistical significance

print( "Analyzing confidence ..." )
significant=0
significantMale=0
significantFemale=0
insignificant=0
for i in range(len(uniquePowers)):
	s1=float(malePowers.count( uniquePowers[i] ))
	n1=float(maleNumber)
	p1=s1/n1
	s2=float(femalePowers.count( uniquePowers[i] ))
	n2=float(femaleNumber)
	p2=s2/n2
	p = (s1 + s2)/(n1+n2)
	z = (p2-p1)/((p*(1.0-p)*((1.0/n1)+(1.0/n2)))**0.5)
	if( z>=1.95 ):
		significant+=1
		significantFemale+=1
		# print "%s:\n\tz=%s"%(uniquePowers[i],z )
		print "%s"%uniquePowers[i]
	elif( z<=-1.95 ):
		significant+=1
		significantMale+=1
		# print "%s:\n\tz=%s"%(uniquePowers[i],z )
		print "%s"%uniquePowers[i]
	else:
		insignificant+=1

print( "Number of characters=%d; male=%d; female=%d; other=%d"%(allNumber, maleNumber, femaleNumber, otherNumber) )
print( "Number of characters with powers=%d; male=%d; female=%d; other=%d"%(powersCnt, malePowersCnt, femalePowersCnt, otherPowersCnt) )
print( "Number of powers with a significant difference=%d; insignificant=%d; percent=%s%%"%(significant, insignificant, 100.0*float(significant)/(float(significant)+float(insignificant))) )
print( "Number of powers with a significant difference towards male=%d; towards female=%d"%(significantMale, significantFemale) )

exit()
