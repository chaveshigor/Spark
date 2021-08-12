import math

class CurrentSource:

    def __init__(self, p, typeOf, params, dt):
        
        self.type = 'I'
        self.typeOf = typeOf
        self.params = params
        self.p = p
        self.ih = []
        self.dt = dt
        self.ic = []
        
        if self.typeOf == 'CC':
            self.im = params[0]
            self.current = lambda t: self.im

        elif self.typeOf == 'CA':
            self.im = params[0]
            self.f = params[1]
            self.phase = params[2] * math.pi/180
            self.current = lambda t: self.im*math.sin(2*math.pi*self.f*t + self.phase)

        self.ihf = lambda i: self.current(self.dt*i)
        
    def resolveInitialConditions(self):
        pass

    def resolveIh(self, i):
        if i == 0:
            self.ih.append(0)
        else:
            if i < 10:
                print(self.ihf(i))
            self.ih.append(self.ihf(i))

    def resolveV(self, v):
        pass

    def resolveI(self):
        self.ic.append(self.ih[-1])