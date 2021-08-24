def outputReader(tensionOutputs, line, coln1, allNodes):
    node = line[coln1[0]-1:coln1[1]]
    
    # Searching for tension nodes output
    if node in allNodes:
        tensionOutputs.append(int(allNodes[node]))

    return tensionOutputs