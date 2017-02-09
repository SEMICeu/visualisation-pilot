#Scripts/GenerateJSONfororg.py Output/FakeOrg.csv
import sys
import json
import operator

projMin = 1;
projMax = 496;
maxBubblesize = 20;

linksMax = 50;

class JNode:
	def __init__(self, index, links, line, label, country, activity):
		self.index = index
		self.links = links
		self.label = label
		self.score = float(line[9])
		self.id = index
		self.level = 1
		self.country = country
		self.activity = activity

	def toJSON(self):
		return json.dumps({'index':self.index,'links':self.links,'label':self.label,'score':self.score,'id':self.index, 'level':self.level, 'country':self.country, 'activity': self.activity},separators=(',', ':'),indent=4)

	def setScore(self, projectNbr):
		self.score = (((float(projectNbr) - projMin)*(maxBubblesize - 1)) / (projMax - projMin)) + 1
		#NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

	def getID(self):
		return self.id;

class JLink:
	def __init__(self, source, target, weight):
		self.source = source
		self.target = target
		self.weight = weight

	def toJSON(self):
		return json.dumps({'source':self.source,'target':self.target,'weight':self.weight},separators=(',', ':'),indent=4)


errorLog = open('error.log', 'w')

#write JSON output file
def WriteJSON(nameOutputFile, orig_nodelist, linksList):
	try:
		nodelist = sorted(orig_nodelist, key=operator.attrgetter("id"))
		outputName = nameOutputFile
		# TODO: create dynamic file name
		outputFile = open(outputName, 'w')
		outputFile.write('{\n')
		outputFile.write('"nodes": [\n');
		for i in range(len(nodelist)-1):
			outputFile.write(nodelist[i].toJSON())
			outputFile.write(',\n')
		outputFile.write(nodelist[len(nodelist)-1].toJSON())
		#TODO handle the case for no links
		outputFile.write('\n')
		outputFile.write('],\n')
		outputFile.write('"links":[\n')
		if len(linksList) > 0:
			for i in range(len(linksList)-1):
				outputFile.write(linksList[i].toJSON())
				outputFile.write(',\n')
				outputFile.write(linksList[len(linksList)-1].toJSON())
		outputFile.write(']\n')
		outputFile.write('}')
	except Exception as e:
		print(e)
		print(nameOutputFile)
		errorLog.write("-------------------------------------");
		errorLog.write("Error while writing the folowing file: "+nameOutputFile)
		errorLog.write("-------------------------------------");

#define some parameters
sepChar = ';'

def extractForOneOrg(index, linesArray):
	currentOrg = linesArray[index].split(sepChar)[0];
	orgDict = {};
	orgList = [];
	linksList = [];
	count = 0;
	copyIndex = index;
	while(copyIndex < len(linesArray) and currentOrg == linesArray[copyIndex].split(sepChar)[0]):
		lineList = linesArray[copyIndex].split(sepChar);
		#update orgsList if orgs not in
		try:
			value = orgDict[lineList[1]];
		except KeyError:
			orgDict[lineList[1]] = count;
			orgList.append(JNode(count,[],lineList,lineList[1],lineList[3],lineList[5]));
			count += 1
		try:
			value = orgDict[lineList[2]];
		except KeyError:
			if lineList[2] != '':
				orgDict[lineList[2]] = count;
				orgList.append(JNode(count,[],lineList,lineList[2],lineList[4],lineList[6]))
				count += 1
		#add links to JNode objects
		if lineList[2] != '':
			org1Index = orgList[orgDict[lineList[1]]].id
			org2Index = orgList[orgDict[lineList[2]]].id
			orgList[orgDict[lineList[1]]].links.append(org2Index);
			orgList[orgDict[lineList[2]]].links.append(org1Index);
			#create JLink Object
			#NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
			linkWeight = (((float(lineList[9])-1)*(5-1))/(linksMax-1)+1)
			linksList.append(JLink(org1Index, org2Index, linkWeight))
		copyIndex +=1
	currentOrg = currentOrg.replace(' ','_')
	currentOrg = currentOrg.replace('*','')
	currentOrg = currentOrg.replace('/','')
	currentOrg = currentOrg.replace('\'','')
	currentOrg = currentOrg.replace('\"','')
	currentOrg = currentOrg.replace(',','')
	currentOrg = currentOrg.replace('&','')
	WriteJSON("outputJS/" + currentOrg + ".json", orgList, linksList)
	return copyIndex;



#read file
FileLink = sys.argv[1]
#linesLink = [line.rstrip('\n') for line in open(FileLink, encoding="utf-8")]
linesLink = [line.rstrip('\n') for line in open(FileLink,  encoding="utf-8")]

currLine = 1;
while(currLine < len(linesLink)):
	currLine = extractForOneOrg(currLine,linesLink);