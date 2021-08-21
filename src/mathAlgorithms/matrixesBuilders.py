import numpy as np

def calculateDimension(elements):

    dimension = 0

    for element in elements:
        n1 = int(element.p.split('-')[0])
        n2 = int(element.p.split('-')[1])

        if n1 > dimension:
            dimension = n1
        if n2 > dimension:
            dimension = n2

        if element.type == 'Ideal Transformer':
            n1 = int(element.s.split('-')[0])
            n2 = int(element.s.split('-')[1])

            if n1 > dimension:
                dimension = n1
            if n2 > dimension:
                dimension = n2

    return dimension

class AdmitancesMatrix:

    def __init__(self, elements):
        self.elements = elements
        self.buildAdmitancesMatrix()


    def buildAdmitancesMatrix(self):
        
        #Counting how much nodes the circuit has
        dimension = calculateDimension(self.elements)

        gm = np.zeros((dimension, dimension))
        
        #Saving elements positions
        nodes = {}

        for element in self.elements:
            p1 = int(element.p.split('-')[0])
            p2 = int(element.p.split('-')[1])

            try:
                nodes[p1].append(element)
            except:
                nodes[p1] = [element]
                
            try:
                nodes[p2].append(element)
            except:
                nodes[p2] = [element]

            if element.type == 'Ideal Transformer':
                p1 = int(element.s.split('-')[0])
                p2 = int(element.s.split('-')[1])

                try:
                    nodes[p1].append(element)
                except:
                    nodes[p1] = [element]
                    
                try:
                    nodes[p2].append(element)
                except:
                    nodes[p2] = [element]
        
        #Building the matrix
        for i in range(dimension):
            for j in range(dimension):
                
                # Main diagonal
                if i == j:
                    for element in nodes[i+1]:
                        # Dont consider current sources
                        if element.type == 'I':
                            continue
                        elif element.type == 'R' or element.type == 'L' or element.type == 'C' or element.type == 'V':
                            gm[i][j] += element.Y
                        elif element.type == 'Ideal Transformer' and not element.s1 == str(i+1):
                            gm[i][j] += element.yp
                        elif element.type == 'Ideal Transformer' and element.s1 == str(i+1):
                            gm[i][j] = gm[i][j]*element.a**2 + element.a**2*element.yp + element.ys
                            #gm[i][j] = element.a**2*element.yp + element.ys
                            
                else:
                    for element in nodes[j+1]:
                        # Dont consider current sources
                        if element.type == 'I':
                            continue
                        elif element in nodes[i+1]:
                            if element.type == 'R' or element.type == 'L' or element.type == 'C' or element.type == 'V':
                                gm[i][j] -= element.Y
                            elif element.type == 'Ideal Transformer':
                                gm[i][j] -= element.a*element.ys
        self.gm = gm


class CurrentMatrix:

    def __init__(self, elements):

        self.elements = elements 
        
        #Saving elements positions
        self.sources = {}

        for element in self.elements:
        
            k = 1

            if element.type == 'R':
                continue

            p1 = int(element.p.split('-')[0])
            p2 = int(element.p.split('-')[1])

            if p1 == 0:

                if element.type != 'V' and element.type != 'I':
                    k = -1
    

                try:
                    self.sources[p2].append((element, k))
                    continue
                except:
                    self.sources[p2] = [(element, k)]
                    continue

            if p2 == 0:

                if element.type != 'V' and element.type != 'I':
                    k = -1

                try:
                    self.sources[p1].append((element, k))
                    continue
                except:
                    self.sources[p1] = [(element, k)]
                    continue

            try:
                self.sources[p1].append((element, -1))
            except:
                self.sources[p1] = [(element, -1)]
                
            try:
                self.sources[p2].append((element, 1))
            except:
                self.sources[p2] = [(element, 1)]

        
    def buildCurrentMatrix(self):
        
        #Counting how much nodes the circuit has
        dimension = calculateDimension(self.elements)

        im = np.zeros((dimension, 1))
        #print(self.sources)
        for i in range(dimension):
            try:
                for source in self.sources[i+1]:
                    im[i][0] += source[1] * source[0].ih[-1]
            except:
                im[i][0] += 0
        return im

class NodesMatrix:

    def __init__(self, elements):

        self.elements = elements
        self.nodes = []

        dimension = calculateDimension(self.elements)

        for i in range(dimension):
            self.nodes.append([])
        
    