import numpy as np
import matplotlib.pyplot as plt

def dx(t,x,y):
      return 10*(y-x)

def dy(t,x,y,z):
  return x*(27-z)-y

def dz(t,x,y,z):
  return x*y-(8/3)*z

x = [1]
y = [0]
z = [0]
t = [0]
N = 10000
h = 50/(N-1)

for n in range(N):
    t.append(t[n]+h)
    x.append(x[n]+h*dx(t[n]+(h/2),x[n]+(h/2)*dx(t[n],x[n],y[n]),y[n]+(h/2)*dx(t[n],x[n],y[n])))  
    y.append(y[n]+h*dy(t[n]+(h/2),x[n]+(h/2)*dy(t[n],x[n],y[n],z[n]),y[n]+(h/2)*dy(t[n],x[n],y[n],z[n]),z[n]+(h/2)*dy(t[n],x[n],y[n],z[n])))
    z.append(z[n]+h*dz(t[n]+(h/2),x[n]+(h/2)*dz(t[n],x[n],y[n],z[n]),y[n]+(h/2)*dz(t[n],x[n],y[n],z[n]),z[n]+(h/2)*dz(t[n],x[n],y[n],z[n])))

plt.plot(t,x,'b', label = "x(t)")
plt.plot(t,z,'g', label = "z(t)")
plt.grid(True)
plt.legend()
plt.show()
plt.plot(x,z,'r', label = "z(t) x(t)")
plt.grid(True)
plt.legend()
plt.show()