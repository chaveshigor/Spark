def sourceReader(nodes:list, nodeCounter:int, line:str, coln1:list, colAmp:list, colf:list, colPh:list, colSig:list, colTStart:list, colTStop:list, sources:list):

    # Declaring the source
    sourceInThisRow = {
        'type': None,
        'signal': None,
        'amplitude': None,
        'frequency': None,
        'start time': None,
        'stop time': None,
        'phase': None,
        'nodes': [None, '0']
    }

    # Creating a function to convert the values of the elements to float
    def getValue(string):
        try:
            return float(string)
        except:
            return False

    setNewSource = True
    sourceType = line[0:2]
    node = line[coln1[0]-1:coln1[1]]
    vm = getValue(line[colAmp[0]-1:colAmp[1]])
    f = getValue(line[colf[0]-1:colf[1]])
    phase = getValue(line[colPh[0]-1:colPh[1]])
    signal = line[colSig[0]-1:colSig[1]]
    tStart = getValue(line[colTStart[0]-1:colTStart[1]])
    tStop = getValue(line[colTStop[0]-1:colTStop[1]])

    def saveNode(node, nodes, nodeCounter):
        if node not in nodes:
            nodes[node] = str(nodeCounter)
            nodeCounter += 1
        return nodes

    # Check if it is a tension or current source
    if '-1' in signal:
        sourceInThisRow['signal'] = 'current'
    else:
        sourceInThisRow['signal'] = 'tension'
    

    # AC Positive terminal
    if sourceType == '14':
        nodes = saveNode(node, nodes, nodeCounter)
        sourceInThisRow['type'] = 'CA'
        sourceInThisRow['frequency'] = f
        if phase == False:
            phase = 0.0
        sourceInThisRow['phase'] = phase
        sourceInThisRow['nodes'][0] = nodes[node]
    
    # DC positive terminal
    elif sourceType == '11':
        nodes = saveNode(node, nodes, nodeCounter)
        sourceInThisRow['type'] = 'CC'
        sourceInThisRow['nodes'][0] = nodes[node]

    # Negative terminal
    elif sourceType == '18':
        if '  ' in node:
            node = '0'
        sources[-1]['nodes'][1] = nodes[node]
        setNewSource = False
    
    sourceInThisRow['amplitude'] = vm
    sourceInThisRow['start time'] = tStart
    sourceInThisRow['stop time'] = tStop

    if setNewSource:
        sources.append(sourceInThisRow)

    return sources, nodes, nodeCounter
