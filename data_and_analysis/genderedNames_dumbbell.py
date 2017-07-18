import pandas as pd
from pandas.io.json import json_normalize
import json
# import ijson
# from pprint import pprint
import matplotlib.pyplot as plt
import codecs

# User input
# company="Marvel"	# 'Marvel', 'DC' or 'Big2' (both)
# company="DC"
company='Big2'		#Both DC and Marvel

# Initialize
marvelData='marvel_characters_complete.txt'
dcData='dc_characters_complete.txt'
output='genderedDumbbell.csv'
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

# List of gendered names
# Note: Some names listed here as diminutive were changed later in the data. For example, in the final piece 'ms' was no longer included as diminutive
debugNames=False
femaleNames=["sister", "she-", "lady", "woman", "mrs.", "dame", "queen", "maid", "madam", "countess", "mother", "mom", "duchess", "governess", "empress", "baroness", "chick", "babe", "doll", "spygal", "badgal", "girl", "daughter", "miss", "ms.", "princess", "lass", "damsel", "mademoiselle"]
femaleDiminutive=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
femaleCat=["sister", "she-", "lady", "woman", "mrs.", "dame", "queen", "maid", "madam", "countess", "mother", "mom", "duchess", "governess", "empress", "baroness", "chick", "babe", "doll", "spygal", "badgal", "girl", "daughter", "miss", "ms.", "princess", "lass", "damsel", "mademoiselle"]

maleNames=["senior", "sr", "brother", "he-", "man", "mr.", "mr ", "master", "guy", "gentleman", "sir", "king", "lord", "count", "father", "dad", "duke", "don ", "earl of", "governor", "viscount", "emperor", "bishop", "baron", "jr", "junior", "boy", "son of", "darkson", "prince", "lad", "lil' bro"]
maleDiminutive=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
maleCat=["senior", "sr", "sister", "she-", "woman", "mrs.", "mrs. ", "master", "gal", "lady", "madam", "queen", "lady", "countess", "mother", "mom", "duchess", "don ", "earl of", "governoress", "viscountess", "empress", "bishop", "baroness", "jr", "junior", "girl", "daughter", "daughter", "princess", "lass", "sister"]

exceptions=["Hillman", "Mangrove", "Mancha", "Brickman", "Mandrac", "Manslaughter", "Mansfield", "Mandarin", "Manuel", "Kaufman", "Kellerman", "Mandrill", "Boyd", "Manipulator", "Dolman", "Hoffman", "Manny", "Dworman", "Mangog", "Manelli", "Talisman", "Truman", "Yeoman", "Roman", "Silberman", "Manic", "Dynaman", "Freeman", "Haldeman", "Feinman", "Manzo", "Wildman", "Shiffman", "Feldman", "Manacle", "Manhattan", "Boynton", "Dorman", "Manning", "Manticore", "Manolis", "Boyer", "Manitou", "Gorman", "Woodman", "Holliman", "Herman", "Mangle", "Weiderman", "Manh", "Newman", "Risman", "Silverman", "Amanaman", "Buckman", "Akerman", "Maniac", "Redman", "Zeeman", "Mandibus", "al-Rahman", "Caiman", "Mangano", "Manna", "Manifold", "Human", "German", "Katuman", "Mantega", "Dillman", "Mandla", "Westman", "Beekman", "Manifold", "Harderman", "Aikman", "Mane", "Lippman", "Manta", "Manchester", "Zuckerman", "Mantis", "Mannheim", "Brookman", "Friedman", "Harriman", "Mannix", "Mandell", "Heiman", "Whorrsman", "Manga", "Hoberman", "Mantegna", "Neiman", "Kriptman", "Layman", "Mannering", "Brockman", "Blairman", "Asherman", "Manson", "Tellman", "Orman", "Norman", "Manners", "Lockman", "Manarry", "Horstman", "Manson", "Manfred", "Norman", "Wolverman", "Mangal", "Doberman", "Altman", "Letterman", "Tuckman", "Beckman", "Buchman", "Hallman", "Welman", "Coleman", "Fordman", "Bowman", "Talman", "Manners", "Mannkin", "Coachman", "Ullman", "Saltzman", "Wolfman", "Mangubat", "Manos", "Rodman", "Mantee", "Ryman", "Mannix", "Vanderman", "Maniak", "Sherman", "Bob Battleman", "Hachiman", "Aman", "Manoo", "Boyle", "Boyne", "Masters", "Master Sergeant", "Masterson", "John Bushmaster", "Guy Gardner", "Guy Kopski", "Guy Hawtree", "Guy Jones", "Guy Dimond", "Guy Harding", "Sirius", "Sirianni", "Sirocco", "Siron", "Kingdom", "Kingston", "Kingslayer", "Davy King", "Marden King", "Tom King", "Jimmy King", "Viking", "Vyking", "Kingsley", "Jack King", "Gregory King", "Gary King", "Alexander Ryking", "John King", "Kingii", "Ironclad", "Lucian Ballad", "Ladykiller", "Al-Khalad", "Jeter Warlord", "Lordin", "Phil Addad", "Dadingra Ummon Tarru", "Dean Haddad", "Henry Bishop", "Bill Bishop", "Jruk", "Sreng of the Firbolg", "Sramian Snitch", "Telos Usr", "Sro-Himm", "Bill Junior", "Missy", "Emily Sims", "Ruth Adams", "Alisa Adams", "Sarah Simms", "Nancy Adams", "Danica Williams", "Diane Abrams", "Dr. Marlena Tims", "May Adams", "Tracy Adams", "Nikki Adams", "Ronnie Sims", "Cindy Adams", "Coat of Arms", "Joy Adams", "Mindy Williams", "Martha Williams", "Annabelle Adams", "Cynthia Adams", "Ellie Sims", "Mia Sims", "Atha Williams", "Coleen McQueen", "Isolde McQueen", "Olivia Queen", "Thea Queen", "Emiko Queen", "Queenie", "Harley Queens", "Cynthia Glass", "Smother", "Momenta", "Beldame", "Dolly Jarvis", "Dolly Constantine", "Dolly Space", "Erna Dollar", "Dolly Dimly", "Dolly Donahue"]


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

def checkNameGender( Name,listNames,listDiminutive,listExceptions,listCounts,listExampleNames ):
	name=Name.lower()
	for j in range(len(listNames)):
		gendered=False
		diminutive=False
		genderName=listNames[j]
		# Determine if the name is gendered
		if(name[:len(genderName)]==genderName):
			gendered=True
			if( listDiminutive[j] ):
				diminutive=True
			break
		elif(name[-len(genderName):]==genderName):
			gendered=True
			if( listDiminutive[j] ):
				diminutive=True
			break
		elif "-%s"%genderName in name:
			gendered=True
			if( listDiminutive[j] ):
				diminutive=True
			break
		elif " %s"%genderName in name:
			gendered=True
			if( listDiminutive[j] ):
				diminutive=True
			break
	if gendered:
		# Exceptions are sensitive to capitalization
		for exception in listExceptions:
			if exception in Name:
				gendered=False
				break
	if gendered:
		listCounts[j]+=1
		listExampleNames[j].append( Name )
		if debugNames:
			print( "%s"%Name )
	return gendered,diminutive





# Get a list of every single power (even duplicates)
# i is each character. It's going through powers for each character
cntMaleNames=0.0
cntMaleNamesDiminutive=0.0
cntFemaleNames=0.0
cntFemaleNamesDiminutive=0.0
cntMaleNamesList=[]
cntFemaleNamesList=[]
maleNamesList=[]
femaleNamesList=[]

for i in range(len(maleNames)):
	cntMaleNamesList.append(0)
	maleNamesList.append([])
for i in range(len(femaleNames)):
	cntFemaleNamesList.append(0)
	femaleNamesList.append([])
for i in range(len(char_Table['name'])):
	# Check the character's gender
	if(char_Table['gender'][i]==male):
		gendered,diminutive=checkNameGender( char_Table['name'][i], maleNames, maleDiminutive, exceptions,cntMaleNamesList,maleNamesList )
		if gendered:
			cntMaleNames+=1.0
			if diminutive:
				cntMaleNamesDiminutive+=1.0
	elif(char_Table['gender'][i]==female):
		gendered,diminutive=checkNameGender( char_Table['name'][i], femaleNames, femaleDiminutive, exceptions,cntFemaleNamesList,femaleNamesList )
		if gendered:
			cntFemaleNames+=1.0
			if diminutive:
				cntFemaleNamesDiminutive+=1.0

percentMaleGendered=100.0*cntMaleNames/float(maleNumber)
percentMaleDiminutive=100.0*cntMaleNamesDiminutive/float(maleNumber)
percentFemaleGendered=100.0*cntFemaleNames/float(femaleNumber)
percentFemaleDiminutive=100.0*cntFemaleNamesDiminutive/float(femaleNumber)
print( "Number of males with gendered name: %d"%cntMaleNames )
print( "Percent males with gendered name: %lf"%percentMaleGendered )
print( "Percent males with diminutive name: %lf"%percentMaleDiminutive )
print( "Number of females with gendered name: %d"%cntFemaleNames )
print( "Percent females with gendered name: %lf"%percentFemaleGendered )
print( "Percent females with diminutive name: %lf"%percentFemaleDiminutive )

file=open(output,'w')
file=codecs.open(output, "w", "utf-8")
file.write('"gen_name", "gen_cat", "count", "gen_per", "gender", "dim", "char_list"\n')
for i in range(len(femaleNames)):
	if(len(femaleNamesList[i])):
		percent=100.0*float(cntFemaleNamesList[i])/float(cntFemaleNames)
		# Write the female instance for this name as a row
		file.write('"%s", "%s", %d, %lf, %d, %d, '%(femaleNames[i], femaleCat[i], cntFemaleNamesList[i], percent, female, femaleDiminutive[i]))
		# Write all the female instance for this name as a string
		file.write('"')
		for j in range(len(femaleNamesList[i])-1):
			file.write('%s | '%femaleNamesList[i][j])
		file.write('%s"\n'%femaleNamesList[i][-1])
for i in range(len(maleNames)):
	if(len(maleNamesList[i])):
		percent=100.0*float(cntMaleNamesList[i])/float(cntMaleNames)
		# Write the male instance for this name as a row
		file.write('"%s", "%s", %d, %lf, %d, %d, '%(maleNames[i], maleCat[i], cntMaleNamesList[i], percent, male, maleDiminutive[i]))
		# Write all the male instance for this name as a string
		file.write('"')
		for j in range(len(maleNamesList[i])-1):
			file.write('%s | '%maleNamesList[i][j])
		file.write('%s"\n'%maleNamesList[i][-1])
file.close()


exit()
