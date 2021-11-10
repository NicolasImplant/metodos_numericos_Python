import numpy as np
import matplotlib.pyplot as plt

def f(t,x,y):
  return 3*x - x*y

def g(t,x,y):
  return x*y - 2*y

N = 10000
h = 20/(N-1)

x = [1]
y = [2]
t = [0]


for n in range(N):
  t.append(t[n]+h)
  kx1 = f(t[n],x[n],y[n])
  ky1 = g(t[n],x[n],y[n])
  kx2 = f(t[n]+(h/2),x[n]+(h*kx1)/2,y[n]+(h*ky1)/2)  
  ky2 = g(t[n]+(h/2),x[n]+(h*kx1)/2,y[n]+(h*ky1)/2)
  kx3 = f(x[n]+(h/2),x[n]+(h*kx2)/2,y[n]+(h*ky2)/2)
  ky3 = g(x[n]+(h/2),x[n]+(h*kx2)/2,y[n]+(h*ky2)/2)
  kx4 = f(x[n]+(h/2),x[n]+(h*kx3)/2,y[n]+(h*kx3)/2)
  ky4 = g(x[n]+(h/2),x[n]+(h*kx3)/2,y[n]+(h*kx3)/2)
  x.append(x[n]+(h/6)*(kx1+2*kx2+2*kx3+kx4))
  y.append(y[n]+(h/6)*(ky1+2*ky2+2*ky3+ky4)) 

plt.plot(t,x,'b', label='x')
plt.plot(t,y,'r', label="y")
plt.grid(True)
plt.show()
plt.plot(x,y,'g', label = 'x(t),y(t)')
plt.grid(True)