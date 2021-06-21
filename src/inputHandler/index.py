# Importing all entities
from entities.resistence import Resistor
from entities.indutance import Indutance
from entities.capacitance import Capacitance
from entities.source import Source
from inputHandler.rlcReader import rlcReader

# Declaring the main function
def readInput(inputPath, dt):

    elements = []
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
            print(listOfElementsInThisRow)
            for entity in listOfElementsInThisRow:
                try:
                    n1 = nodes[listOfElementsInThisRow[entity]['nodes'][0]]
                    n2 = nodes[listOfElementsInThisRow[entity]['nodes'][1]]
                    value = listOfElementsInThisRow[entity]['value']
                except:
                    print('err')
                if entity == 'r' and listOfElementsInThisRow[entity]['value'] != None:
                    elements.append(Resistor(n1+'-'+n2, value))
                elif entity == 'l' and listOfElementsInThisRow[entity]['value'] != None:
                    elements.append(Indutance(n1+'-'+n2, value, 0, 0, dt))
                elif entity == 'c' and listOfElementsInThisRow[entity]['value'] != None:
                    elements.append(Capacitance(n1+'-'+n2, value, 0, 0, dt))
                else:
                    continue

        if analyzeType == '/SOURCE':
            
            sourceType = line[0:2]
            n1 = line[coln1[0]-1:coln1[1]]
            n2 = 0
            vm = line[colAmp[0]-1:colAmp[1]]
            f = line[colf[0]-1:colf[1]]
            phase = line[colPh[0]-1:colPh[1]]
            tStart = line[colTStart[0]-1:colTStart[1]]
            tStop = line[colTStop[0]-1:colTStop[1]]

            if sourceType == '18':
                n2 = nodes[n1]
                n1 = elements[-1].p.split('-')[1]
                currentNodes = str(n2)+'-'+str(n1)
                elements[-1].p = currentNodes

                # currentNodes = str(n2)+'-'+str(0)
                # print(currentNodes)
                # elements.append(Resistor(currentNodes, 0.0000000001))
                continue

            if len(n1) == 0:
                continue

            if '          ' in vm:
                continue

            if '         ' in tStart:
                tStart = 0.0
            else:
                try:
                    tStart = float(tStart)
                    tStop = float(tStop)

                    if tStart == -1.0:
                        tStart = 0.0
                    
                except:
                    pass

            if '         ' in phase:
                phase = 0.0
            else:
                try:
                    phase = float(phase)
                except:
                    pass

            try:
                vm = float(vm)
                f = float(f)
                #print(vm, f, phase, tStart, tStop)
                #declarar elemento aqui
                if n1 not in nodes:
                    nodes[n1] = str(nodeCounter)
                    nodeCounter += 1
                currentNodes = str(0)+'-'+str(nodes[n1])
                sourceAC = Source(currentNodes, 'CA', [vm, 0.00000000001, f, phase], dt)
                elements.append(sourceAC)
            except:
                pass




    return elements, nodes

if __name__ == '__main__':

    elements, nodes = readInput(r'C:\Users\higor\OneDrive\projetos\Spark\inputExamples\Exemplo.atp', .0001)
    #print(elements)
    #print(nodes)

    # for i in elements:
    #     print(i.p, i.type)