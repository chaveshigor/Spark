from matrixes import *
from inputATPhandler import readInput
from datetime import datetime
from numpy.linalg import inv
import matplotlib.pyplot as plt
import numpy as np
import os

before = datetime.now()

time = []
us = 50
dt = .000001*us
timeToSimulate = 1

#Declaring the elements
inputPath = r'C:\Users\higor\OneDrive\projetos\tcc\Exemplo copy.atp'
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
while True:

    typeOfResponse = input('\nTipos de resultado: \n1 - Tensão\n2 - Corrente\n\nDigite o resultado a ser mostrado: ')

    if typeOfResponse == '1':
        #Printing graphic
        barr = int(input('Digite a barra a se visualizar o resultado: '))

        fig, ax = plt.subplots()
        ax.plot(time[1:10000], vb[barr-1][1:10000])
        ax.set(xlabel='time (ms)', ylabel='voltage (V)', title='Tensão')
        ax.grid()
        plt.show()

        file = open('teste2.txt', 'w')
        for v in vb[barr-1][0:200]:
            file.write('"'+str(v).replace('.', ',')+'"'+'\n')

    elif typeOfResponse == '2':
        for ele in elements:

            if ele.type == 'V':
                continue

            try:
                fig, ax = plt.subplots()
                current = ele.ic

                if len(time)>len(current):
                    ax.plot(time[1:len(current)], current[1:len(current)])
                elif len(current)>len(time):
                    ax.plot(time[1:len(time)], current[1:len(time)])
                else:
                    ax.plot(time[1:len(time)], current[1:len(time)])

                ax.set(xlabel='time (ms)', ylabel='current (A)', title='Corrente '+ele.type+' '+ele.p)
                ax.grid()
                plt.show()
            except Exception as err:
                print(err)
                pass
    
    else:
        break



