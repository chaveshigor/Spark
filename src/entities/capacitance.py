from numpy.linalg import inv
import numpy as np
import math

class Capacitance:

    def __init__(self, p, C, v0, i0, dt):

        self.p = p
        self.p1 = p.split('-')[0]
        self.p2 = p.split('-')[1]
        self.C = C
        self.v0 = v0
        self.i0 = i0
        self.dt = dt
        self.R = dt/(2*C)
        self.Y = 1/self.R
        self.ic = []
        self.ih = []
        self.vc = []
        self.type = 'C'

    def resolveInitialConditions(self):
        
        self.vc.append(self.v0)
        self.ic.append(self.i0)
        self.ih.append(0)

        return self.vc, self.ic, self.ih

    def resolveIh(self):

        Rc = self.R
        vc = self.vc
        ic = self.ic

        ih = float(-1/Rc*vc[-1] - ic[-1])
        self.ih.append(ih)
        return ih

    def resolveV(self, vm):

        p1 = int(self.p1)
        p2 = int(self.p2)

        if p1 == 0:
            ddp = vm[p2-1][0]
        if p2 == 0:
            ddp = vm[p1-1][0]
        if p1 != 0 and p2 != 0:
            ddp = vm[p1-1][0] - vm[p2-1][0]
        
        vct = float(ddp)
        self.vc.append(vct)
        return vct

    def resolveI(self):

        Rc = self.R
        vc = self.vc
        ic = self.ic
        ih = self.ih

        ict = float(1/Rc * vc[-1] + ih[-1])
        self.ic.append(ict)

    def resolve(self, gm, im, i):

        Rc = self.R
        vc = self.vc
        ic = self.ic
        ih = self.ih

        zm = inv(gm)
        #Pensar em como definir as condições iniciais
        if i == 0:
            self.vc.append(self.v0)
            self.ic.append(self.i0)
            self.ih.append(0)
            return self.vc, self.ic, self.ih

        #Pensar em como fazer essa forma uzando as matrizes de corrente e tensão
        #print(self.vc, ic, ih)
        
        iht = float(-1/Rc*vc[-1] - ic[-1])
        vct = float(np.matmul(zm, im(self.dt*i, iht))) #Fazer o produto das duas matrizes
        ict = float(1/Rc * vct + iht)

        self.vc.append(vct)
        self.ic.append(ict)
        self.ih.append(iht)

        return vc, ic, ih

