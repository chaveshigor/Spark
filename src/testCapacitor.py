####Developer: Higor Chaves
import matplotlib.pyplot as plt
from numpy.linalg import inv
import numpy as np
import matplotlib
import math

#Declaring the main variables
dt = .000001
finalTime = .1
Vin = lambda t: 100*math.sin(2*math.pi*60*t)
Vin = lambda t: 100

Zin = 10
C = 10**-6
Rc = dt/(2*C)

#Creating the impedances, admitances and time matrixes
gm = np.array([[1/Zin + 2*C/dt]])
zm = inv(gm)
tm = np.arange(0, finalTime, dt)
im = np.zeros(tm.shape)
ih = np.zeros(tm.shape)
vb = np.zeros(tm.shape)
ic = np.zeros(tm.shape)

#Starting the main loop
for i in range(int(finalTime/dt)+1):
    
    t = i*dt

    if i == 0:
        ic[i] = Vin(t)/Zin
        vb[i] = 0
        ih[i] = 0
        continue

    Iin = Vin(t)/Zin

    ih[i] = -1/Rc*vb[i-1] - ic[i-1]
    vb[i] = zm[0][0]*(Iin - ih[i])
    ic[i] = 1/Rc * vb[i] + ih[i]

#print(vb[int(0.001/dt)])
print('ih', ih[0], ih[1], ih[2], ih[3])
print('vb', vb[0], vb[1], vb[2], vb[3])
print('ic', ic[0], ic[1], ic[2], ic[3])
fig, ax = plt.subplots()
ax.plot(tm, vb)
ax.set(xlabel='time (s)', ylabel='voltage (V)', title='Tensão')
ax.grid()
plt.show()

#multiplying matrixes
#np.matmul(g, v(0))