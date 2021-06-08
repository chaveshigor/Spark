class Resistor:

    def __init__(self, p, R):

        self.type = 'R'
        self.p = p
        self.p1 = p.split('-')[0]
        self.p2 = p.split('-')[1]
        self.R = R
        self.Y = 1/R
        self.v = []
        self.ic = []

    def resolveInitialConditions(self):
        # self.v.append(0)
        # self.i.append(0)
        pass

    def resolveIh(self):
        pass

    def resolveV(self, vm):
        
        p1 = int(self.p1)
        p2 = int(self.p2)

        if p1 == 0:
            ddp = vm[p2-1][0]
        if p2 == 0:
            ddp = vm[p1-1][0]
        if p1 != 0 and p2 != 0:
            ddp = vm[p1-1][0] - vm[p2-1][0]
        
        vr = float(ddp)
        self.v.append(vr)
        return vr

    def resolveI(self):
        
        ir = float(self.v[-1]/self.R)
        self.ic.append(ir)