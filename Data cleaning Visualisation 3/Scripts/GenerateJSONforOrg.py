#Scripts/GenerateJSONfororg.py Output/NbLinkOrgLevel1.csv Output/OrgInformation.csv


import sys
import json

class JNode:
	def __init__(self, index, links, line):
		self.index = index
		self.links = links
		self.label = line[1]
		self.score = line[2]
		self.id = index
	def toJSON(self):
		return json.dumps({'index':self.index,'links':self.links,'label':self.label,'score':self.score,'id':self.index},separators=(',', ':'),indent=4)

class JLink:
	def __init__(self, source, target, weight):
		self.source = source
		self.target = target
		self.weight = weight
	def toJSON(self):
		return json.dumps({'source':self.source,'target':self.target,'weight':self.weight},separators=(',', ':'),indent=4)


sepChar = ';'

orgDictionary = {};


FileLink = sys.argv[1]
FileOrg = sys.argv[2]

open(FileLink)
linesLink = [line.rstrip('\n') for line in open(FileLink, encoding="utf-8")]
linesOrg = [line.rstrip('\n') for line in open(FileOrg, encoding="utf-8")]


for i in range(1, len(linesOrg)):
	lineList = linesOrg[i].split(sepChar)
	orgDictionary[lineList[1]] = JNode(i,[],lineList)


#write JSON output file
def WriteJSON(nameOutputFile, nodelist, linksList):
	try:
		outputName = nameOutputFile
		outputFile = open(outputName, 'w')
		outputFile.write('{\n')
		outputFile.write('"nodes": [\n');
		for i in range(len(nodelist)-1):
			outputFile.write(nodelist[i].toJSON())
			outputFile.write(',\n')
		outputFile.write(nodelist[len(nodelist)-1].toJSON())
		outputFile.write('\n')
		outputFile.write('],\n')
		outputFile.write('"links":[\n')
		for i in range(len(linksList)-1):
			outputFile.write(linksList[i].toJSON())
			outputFile.write(',\n')
		outputFile.write(linksList[len(linksList)-1].toJSON())
		outputFile.write(']\n')
		outputFile.write('}')
	except:
		print(nameOutputFile)


name = "";
NodeDic = {};
linksList = [];
for i in range(1, len(linesLink)):
	lineList = linesLink[i].split(sepChar)
	curName = lineList[4]
	if(name != curName and len(NodeDic) != 0):
		NodeList = [];
		for key, value in NodeDic.items():
			NodeList.append(value)
		WriteJSON("outputJS/" + name + ".json", NodeList, linksList)
		NodeDic = {};
		linksList = [];
	name = curName

	org1Name = lineList[1]
	org2Name = lineList[2]
	if (not org1Name in NodeDic)  :
		NodeDic[org1Name] = orgDictionary[org1Name]
	if (not org2Name in NodeDic):
		NodeDic[org2Name] = orgDictionary[org2Name]

	org1Index = NodeDic[org1Name].id
	org2Index = NodeDic[org2Name].id

	NodeDic[org1Name].links.append(org2Index)
	linksList.append(JLink(org1Index, org2Index, float(lineList[3])))


NodeList = [];
for key, value in NodeDic.items():
	NodeList.append(value)
WriteJSON("outputJS/" + name + ".json", NodeList, linksList)
NodeDic = {};
linksList = [];
