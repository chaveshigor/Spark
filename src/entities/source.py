import math

class Source:

    def __init__(self, p, typeOf, params, dt):
        
        self.type = 'V'
        self.typeOf = typeOf
        self.params = params
        self.p = p
        self.ih = []
        self.dt = dt

        if self.typeOf == 'CC':
            self.vm = params[0]
            self.Zin = params[1]
            self.v = lambda t: self.vm

        elif self.typeOf == 'CA':
            self.vm = params[0]
            self.Zin = params[1]
            self.f = params[2]
            self.phase = params[3] * math.pi/180
            self.v = lambda t: 2**.5*self.vm*math.sin(2*math.pi*self.f*t + self.phase)

        self.Y = 1/self.Zin
        self.ihf = lambda i: self.v(self.dt*i)/self.Zin

    def resolveInitialConditions(self):
        pass

    def resolveIh(self, i):
        if i == 0:
            self.ih.append(0)
        else:
            self.ih.append(self.ihf(i))

    def resolveV(self, v):
        pass

    def resolveI(self):
        pass