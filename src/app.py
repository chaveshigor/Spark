# Importing the project dependences
from datetime import datetime
import numpy as np
from numpy.linalg import inv

# Importing the project functions 
from mathAlgorithms.matrixesBuilders import *
from inputHandler.index import readInput
from resultHandler.writeResults import showResults

before = datetime.now()

time = []
us = 50
dt = .000001*us
timeToSimulate = 1
writeResults = False

# Declaring the elements
inputPath = r'inputExamples\Exemplo.atp'
elements, allNodes, tensionOutputs = readInput(inputPath, dt)

# Declaring admitances matrix
gm = AdmitancesMatrix(elements).gm
zm = inv(gm)

# Declaring the nodes tensions matrix
vb = NodesMatrix(elements).nodes
for i in range(len(vb)):
    vb[i].append(0)
    
# Declaring currents matrix
Im = CurrentMatrix(elements)
a = 0

# Main loop
while True:

    # Getting the current time
    now = datetime.now()

    if (now - before).total_seconds() >= timeToSimulate:
        print('Duração da simulação: '+str((now - before).total_seconds()))
        break

    # Declaring and incrementing the time matrix
    t = dt * a
    time.append(t)

    # Solving initial conditions
    if a == 0:
        for element in elements:
            element.resolveInitialConditions()
        
        a += 1
        continue

    # Solving Ih
    for element in elements:
        if element.type == 'V' or element.type == 'I':
            element.resolveIh(a)
        else:
            element.resolveIh()
    
    # Solving Tensions
    iNow = Im.buildCurrentMatrix()
    vNow = np.matmul(zm, iNow)
   
    for i in range(len(vNow)):
        vb[i].append(vNow[i][0])
        
    # Solving elements tensions
    for element in elements:
        k = element.resolveV(vNow)

    # resolveIc
    for element in elements:
        element.resolveI()

    a += 1

#Showing the results
showResults(time, vb, elements, writeResults, tensionOutputs, dt)
