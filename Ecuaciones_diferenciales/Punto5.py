import numpy as np
import matplotlib.pyplot as plt

def dz(t,x,y,z):
    A = 3.6
    return x*(y**2) - (x**3) - A*z

def dy(t,x,y,z):
    return z

def dx(t,x,y,z):
    return y

t = [0]
z = [1]
y = [0]
x = [0]
N = 10**6
h = 200/(N-1)

for n in range(N):
    t.append(t[n]+h)
    x.append(x[n]+h*dx(t[n]+(h/2),x[n]+(h/2)*dx(t[n],x[n],y[n],z[n]),y[n]+(h/2)*dx(t[n],x[n],y[n],z[n]),z[n]+(h/2)*dx(t[n],x[n],y[n],z[n]))) 
    y.append(y[n]+h*dy(t[n]+(h/2),x[n]+(h/2)*dy(t[n],x[n],y[n],z[n]),y[n]+(h/2)*dy(t[n],x[n],y[n],z[n]),z[n]+(h/2)*dy(t[n],x[n],y[n],z[n])))
    z.append(z[n]+h*dz(t[n]+(h/2),x[n]+(h/2)*dz(t[n],x[n],y[n],z[n]),y[n]+(h/2)*dz(t[n],x[n],y[n],z[n]),z[n]+(h/2)*dz(t[n],x[n],y[n],z[n])))

plt.plot(x,y,'b', label = "x(t) vs y(t)")
plt.grid(True)
plt.legend()