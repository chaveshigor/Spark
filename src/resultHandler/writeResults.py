import matplotlib.pyplot as plt
import os 

def showResults(time: list, vb: list, elements: list, writeFiles: bool, dt: float):

    if writeFiles:
        writeResultsInFile(time, vb, elements, dt)

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

def writeResultsInFile(time, vb, elements, dt):

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