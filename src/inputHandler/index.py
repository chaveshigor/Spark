# Importing all entities
from entities.capacitance import Capacitor
from entities.resistence import Resistor
from entities.indutance import Indutance
from entities.source import Source

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
            r = line[colR[0]-1:colR[1]]
            l = line[colL[0]-1:colL[1]]
            c = line[colC[0]-1:colC[1]]
            n1 = line[coln1[0]-1:coln1[1]]
            n2 = line[coln2[0]-1:coln2[1]]
            
            if len(r) == 0 and len(l) == 0 and len(c) == 0:
                continue

            if n1 == '      ' or n1 == '     ' or n1 == '    ':
                n1 = '0'

            if n2 == '      ' or n2 == '     ' or n2 == '    ':
                n2 = '0'
                #print('eu')

            if len(r) > 0:
                try:
                    r = float(r)
                    elementsTemp.append(['r', r])
                except:
                    pass
            
            if len(l) > 0:
                try:
                    l = float(l)
                    elementsTemp.append(['l', l])
                except:
                    pass

            if len(c) > 0:
                try:
                    c = float(c)*10**-6
                    elementsTemp.append(['c', c])
                except:
                    pass               

            
            #More than one element in the line of the input file
            if len(elementsTemp) > 1:

                for k in range(len(elementsTemp)):
                    
                    #First element of the line
                    if k == 0:
                        
                        if n1 not in nodes:
                            nodes[n1] = str(nodeCounter)
                            nodeCounter += 1

                        n2 = str(nodeCounter)
                        # print('n2 =', n2)
                        nodes[n2] = str(nodeCounter)
                        #nodeCounter += 1

                        currentNode = nodes[n1]+'-'+nodes[n2]

                        if elementsTemp[k][0] == 'r':
                            elements.append(Resistor(currentNode, elementsTemp[k][1]))
                        if elementsTemp[k][0] == 'l':
                            elements.append(Indutance(currentNode, elementsTemp[k][1], 0, 0, dt))
                        if elementsTemp[k][0] == 'c':
                            elements.append(Capacitor(currentNode, elementsTemp[k][1], 0, 0, dt))

                    #Last element of the line
                    elif k == len(elementsTemp)-1:
                        n1 = str(nodeCounter)
                        nodes[n1] = str(nodeCounter)
                        nodeCounter += 1

                        n2 = line[coln2[0]-1:coln2[1]]
                        if n2 == '      ' or n2 == '     ' or n2 == '    ':
                            n2 = '0'

                        if n2 not in nodes:
                            nodes[n2] = str(nodeCounter)
                            #nodeCounter += 1

                        currentNode = nodes[n1]+'-'+nodes[n2]

                        if elementsTemp[k][0] == 'r':
                            elements.append(Resistor(currentNode, elementsTemp[k][1]))
                        if elementsTemp[k][0] == 'l':
                            elements.append(Indutance(currentNode, elementsTemp[k][1], 0, 0, dt))
                        if elementsTemp[k][0] == 'c':
                            elements.append(Capacitor(currentNode, elementsTemp[k][1], 0, 0, dt))
                    
                    #Some midle element of the line
                    else:
                        # print(elementsTemp[k], nodeCounter)
                        n1 = str(nodeCounter)
                        nodes[n1] = str(nodeCounter)
                        nodeCounter += 1

                        n2 = str(nodeCounter)
                        nodes[n2] = str(nodeCounter)
                        #nodeCounter += 1

                        currentNode = nodes[n1]+'-'+nodes[n2]

                        if elementsTemp[k][0] == 'r':
                            elements.append(Resistor(currentNode, elementsTemp[k][1]))
                        if elementsTemp[k][0] == 'l':
                            elements.append(Indutance(currentNode, elementsTemp[k][1], 0, 0, dt))
                        if elementsTemp[k][0] == 'c':
                            elements.append(Capacitor(currentNode, elementsTemp[k][1], 0, 0, dt))


            #Just one element in the line of the input file
            else:

                if n1 not in nodes:
                    nodes[n1] = str(nodeCounter)
                    nodeCounter += 1
                if n2 not in nodes:
                    nodes[n2] = str(nodeCounter)
                    nodeCounter += 1
                
                currentNode = nodes[n1]+'-'+nodes[n2]

                if elementsTemp[0][0] == 'r':
                    elements.append(Resistor(currentNode, elementsTemp[0][1]))
                if elementsTemp[0][0] == 'l':
                    elements.append(Indutance(currentNode, elementsTemp[0][1], 0, 0, dt))
                if elementsTemp[0][0] == 'c':
                    elements.append(Capacitor(currentNode, elementsTemp[0][1], 0, 0, dt))

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

    elements, nodes = readInput(r'C:\Users\higor\OneDrive\projetos\tcc\Exemplo copy.atp', .0001)
    #print(nodes)
    #print(nodes)

    for i in elements:
        print(i.p, i.type)