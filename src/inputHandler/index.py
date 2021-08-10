# Importing all entities
from entities.resistence import Resistor
from entities.indutance import Indutance
from entities.capacitance import Capacitance
from entities.source import Source
from entities.currentSource import CurrentSource
from inputHandler.rlcReader import rlcReader
from inputHandler.sourceReader import sourceReader

# Declaring the main function
def readInput(inputPath, dt):

    elements = []
    sourcesTemp = []
    nodes = {'0':'0'}

    coln1 = [3, 8]
    coln2 = [9, 14]
    colref1 = [15, 20]
    colref2 = [21, 26]
    colR = [27, 32]
    colL = [33, 38]
    colC = [39, 44]
    colAmp = [11, 20]
    colf = [21, 30]
    colPh = [31, 40]
    colSig = [9, 10]
    colTStart = [61, 70]
    colTStop = [71, 80]

    file = open(inputPath, 'r')
    content = file.readlines()
    analyzeType = ''

    nodeCounter = 1

    for line in content:
        
        elementsTemp = []

        #Getting the type of data to analyze
        if 'C' in line[0]:
            continue
        if 'POWER FREQUENCY' in line:
            analyzeType = 'POWER FREQUENCY'
        if '/BRANCH' in line:
            analyzeType = '/BRANCH'
        if '/SWITCH' in line:
            analyzeType = '/SWITCH'
        if '/SOURCE' in line:
            analyzeType = '/SOURCE'

        #Alanyzing the data in the input file
        if analyzeType == 'POWER FREQUENCY':
            pass

        if analyzeType == '/BRANCH':
            # Reading the RLC elements
            listOfElementsInThisRow, nodes, nodeCounter = rlcReader(colR, colL, colC, coln1, coln2, line, nodes, nodeCounter)
            for entity in listOfElementsInThisRow:
                try:
                    n1 = nodes[listOfElementsInThisRow[entity]['nodes'][0]]
                    n2 = nodes[listOfElementsInThisRow[entity]['nodes'][1]]
                    value = listOfElementsInThisRow[entity]['value']
                except:
                    pass
                if entity == 'r' and listOfElementsInThisRow[entity]['value'] != None:
                    elements.append(Resistor(n1+'-'+n2, value))
                elif entity == 'l' and listOfElementsInThisRow[entity]['value'] != None:
                    elements.append(Indutance(n1+'-'+n2, value, 0, 0, dt))
                elif entity == 'c' and listOfElementsInThisRow[entity]['value'] != None:
                    elements.append(Capacitance(n1+'-'+n2, value, 0, 0, dt))
                else:
                    continue

        if analyzeType == '/SOURCE':
            # Reading the tension sources
            sourcesTemp = []
            sourcesTemp, nodes, nodeCounter = sourceReader(nodes, nodeCounter, line, coln1, colAmp, colf, colPh, colSig, colTStart, colTStop, sourcesTemp)
            for source in sourcesTemp:
                if source['type'] == None:
                    continue
                currentNodes = source['nodes'][0] + '-' + source['nodes'][1]
                signal = source['signal']
                vm = source['amplitude']

                if source['type'] == 'CA':
                    f = source['frequency']
                    phase = source['phase']
                    if signal == 'current':
                        sourceAC = CurrentSource(currentNodes, 'CA', [vm, f, phase], dt)
                    else:
                        sourceAC = Source(currentNodes, 'CA', [vm, 0.00000000001, f, phase], dt)
                    elements.append(sourceAC)
                    #continue

                elif source['type'] == 'CC':
                    if signal == 'current':
                        sourceDC = CurrentSource(currentNodes, 'CC', [vm], dt)
                    else:
                        sourceDC = Source(currentNodes, 'CC', [vm, 0.00000000001], dt)
                    elements.append(sourceDC)
                    #continue
                



    for ele in elements:
        print(ele.type, ele.p)
    return elements, nodes

if __name__ == '__main__':

    elements, nodes = readInput(r'C:\Users\higor\OneDrive\projetos\Spark\inputExamples\Exemplo.atp', .0001)
    #print(elements)
    #print(nodes)

    # for i in elements:
    #     print(i.p, i.type)