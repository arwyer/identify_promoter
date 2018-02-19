import sys
import os
import json

def build_gibbs_command(inputFilePath):
    outputFilePath = '/kb/module/work/tmp/gibbs_output.txt'
    #outputFilePath = './temp/gibbs_output.txt'
    length = '8'
    command = 'Gibbs ' + inputFilePath + ' ' + length + ' -n > ' + outputFilePath
    return command

def run_gibbs_command(command):
    os.system(command)

def parse_gibbs_output():
    outputFileDir = '/kb/module/work/tmp'
    #outputFileDir = './temp'
    outputFilePath = outputFileDir + '/gibbs_output.txt'
    gibbsFile = open(outputFilePath,'r')
    motifList = []
    motifDict = {}
    pwmList = []
    processPWM = False
    processLoc = False
    gotSig = False
    motifIncluded = False

    #TODO: keeping p-value as -1 until I understand the output stats better
    for line in gibbsFile:
        if processLoc is True:
            if '********' in line:
                processLoc = False
                gotSig = False
                motifDict['p-value'] = -1.0
                for m in motifList:
                    if motifDict['Iupac_signature'] == m['Iupac_signature']:
                        motifIncluded = True
                if not motifIncluded:
                    motifList.append(motifDict)
                motifDict = {}
                motifIncluded = False
                pwmList = []
                #add motif to list from here
            elif 'Num Motifs' not in line:
                elems = line.split()
                if not gotSig:
                    motif = elems[4]
                    motifDict['Iupac_signature'] = motif
                    gotSig = True
                locList = []
                locList.append(elems[9])
                locList.append(elems[2])
                locList.append(elems[6])
                if elems[8] == 'F':
                    locList.append('+')
                else:
                    locList.append('-')
                motifDict['Locations'] = locList
        if processPWM is True:
            if len(line.split()) == 0:
                processPWM = False
                motifDict['pwm'] = pwmList
            elif '|' in line:
                elems = line.split()
                rowList = []
                rowList.append(('A',float(elems[2])))
                rowList.append(('C',float(elems[4])))
                rowList.append(('G',float(elems[5])))
                rowList.append(('T',float(elems[3])))
                pwmList.append(rowList)


        if 'columns' in line:
            motifLength = int(line.split()[0])
            processLoc = True
        if 'Motif probability model' in line:
            processPWM = True

    jsonFilePath = outputFileDir + '/gibbs.json'
    with open(jsonFilePath,'w') as jsonFile:
        json.dump(motifList,jsonFile)
