def rlcReader(colR:list, colL:list, colC:list, coln1:list, coln2:list, line:str, nodes:dict, nodeCounter:int):

    # Declaring the entities in this row of the ATP input file
    listOfElementsInThisRow = {
        'r': {'value': None, 'nodes':[None, None]},
        'l': {'value': None, 'nodes':[None, None]},
        'c': {'value': None, 'nodes':[None, None]}
    }

    # Declaring the values (string format) of the entities usint their position on the ATP input file
    r = line[colR[0]-1:colR[1]]
    l = line[colL[0]-1:colL[1]]
    c = line[colC[0]-1:colC[1]]
    n1 = line[coln1[0]-1:coln1[1]]
    n2 = line[coln2[0]-1:coln2[1]]
    
    # Checking for ground nodes
    if n1 == '      ':
        n1 = '0'

    if n2 == '      ':
        n2 = '0'

    # Creating a function to convert the values of the elements to float
    def getValue(string):
        try:
            return float(string)
        except:
            return False

    # Converting the values and saving this info in the list of entities
    if getValue(r):
        listOfElementsInThisRow['r']['value'] = getValue(r)
    
    if getValue(l):
        listOfElementsInThisRow['l']['value'] = getValue(l)*10**-3

    if getValue(c):
        listOfElementsInThisRow['c']['value'] = getValue(c)*10**-6
    
    if listOfElementsInThisRow['r']['nodes'] == None and listOfElementsInThisRow['l']['nodes'] == None and listOfElementsInThisRow['c']['nodes'] == None:
        return None

    # Saving the first node position
    if listOfElementsInThisRow['r']['value'] != None:
        listOfElementsInThisRow['r']['nodes'][0] = n1
        firstNodePosition = 0

    elif listOfElementsInThisRow['l']['value'] != None:
        listOfElementsInThisRow['l']['nodes'][0] = n1
        firstNodePosition = 1

    else:
        listOfElementsInThisRow['c']['nodes'][0] = n1
        firstNodePosition = 2


    # Saving the second node position
    if listOfElementsInThisRow['c']['value'] != None:
        listOfElementsInThisRow['c']['nodes'][1] = n2
        secondNodePosition = 2

    elif listOfElementsInThisRow['l']['value'] != None:
        listOfElementsInThisRow['l']['nodes'][1] = n2
        secondNodePosition = 1

    else:
        listOfElementsInThisRow['r']['nodes'][1] = n2
        secondNodePosition = 0

    # Declaring the function to save the nodes in the dict nodes
    def addNode(entity, nodes, counter):
        first = listOfElementsInThisRow[entity]['nodes'][0]
        second = listOfElementsInThisRow[entity]['nodes'][1]
        aux = 0

        if first not in nodes:
            nodes[first] = str(counter)
            counter += 1
            aux += 1
        if second not in nodes:
            nodes[second] = str(counter)
            counter += 1
            aux += 1

        return nodes, aux

    # Saving the position of the middle nodes and incrementing the nodes dictionary
    for count, entity in enumerate(listOfElementsInThisRow):
        if listOfElementsInThisRow[entity]['value'] == None:
            continue
        if (secondNodePosition - firstNodePosition) != 0:
            if count == firstNodePosition:
                listOfElementsInThisRow[entity]['nodes'][1] = str(nodeCounter)
            elif count == secondNodePosition:
                listOfElementsInThisRow[entity]['nodes'][0] = str(nodeCounter-1)
            elif listOfElementsInThisRow[entity]['value'] != None:
                listOfElementsInThisRow[entity]['nodes'][0] = str(nodeCounter-1)
                listOfElementsInThisRow[entity]['nodes'][1] = str(nodeCounter)

            nodes, aux = addNode(entity, nodes, nodeCounter)
            nodeCounter += aux

        else:
            nodes, aux = addNode(entity, nodes, nodeCounter)
            nodeCounter += aux


    return listOfElementsInThisRow, nodes, nodeCounter
