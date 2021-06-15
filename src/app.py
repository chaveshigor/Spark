# Importing the project dependences
from datetime import datetime
import numpy as np
from numpy.linalg import inv
import os

# Importing the project functions 
from matrixesBuilders import *
from inputHandler.index import readInput
from resultHandler.writeResults import showResults

before = datetime.now()

time = []
us = 50
dt = .000001*us
timeToSimulate = 1

#Declaring the elements
inputPath = r'C:\Users\higor\OneDrive\projetos\Spark\inputExamples\Exemplo.atp'
elements, allNodes = readInput(inputPath, dt)
#print(allNodes)

# for ele in elements:
#     print(ele.type, ele.p)

#Declaring admitances matrix
gm = AdmitancesMatrix(elements).gm
zm = inv(gm)

#Declaring the nodes tensions matrix
vb = NodesMatrix(elements).nodes
for i in range(len(vb)):
    vb[i].append(0)
    
#Declaring currents matrix
Im = CurrentMatrix(elements)
a = 0

#Main loop
while True:

    #Getting the current time
    now = datetime.now()

    if (now - before).total_seconds() >= timeToSimulate:
        print('Duração da simulação: '+str((now - before).total_seconds()))
        break

    #Declaring and incrementing the time matrix
    t = dt * a
    time.append(t)

    #Solving initial conditions
    if a == 0:
        for element in elements:
            element.resolveInitialConditions()
        
        a += 1
        continue

    #Solving Ih
    for element in elements:
        if element.type == 'V':
            element.resolveIh(a)
        else:
            element.resolveIh()
    
    #Solving Tensions
    iNow = Im.buildCurrentMatrix()
    vNow = np.matmul(zm, iNow)
   
    for i in range(len(vNow)):
        vb[i].append(vNow[i][0])
        
    #Solving elements tensions
    for element in elements:
        k = element.resolveV(vNow)

    #resolveIc
    for element in elements:
        element.resolveI()

    a += 1

#Writing the results in folders
folders = os.listdir()
if 'tensions' not in folders:
    os.mkdir('tensions')
if 'currents' not in folders:
    os.mkdir('currents')

counter = 1
for bar in vb:
    file = open('tensions/Barra '+str(counter)+'.txt', 'w')
    for v in bar:
        file.write(str(v).replace('.', ',')+'\n')
    file.close()
    counter += 1

for ele in elements:
    if ele.type == 'V':
        continue
    try:
        currents = ele.ic
        file = open('currents/'+str(ele.type)+' '+str(ele.p)+' .txt', 'w')
        for i in currents:
            file.write(str(i).replace('.', ',')+'\n')
        file.close()
    except:
        pass

for i in range(len(time)):
    time[i] = time[i]/dt*1000

#Showing the results
showResults(time, vb, elements)
