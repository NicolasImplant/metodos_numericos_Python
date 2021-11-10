import numpy as np
import matplotlib.pyplot as plt

def dy(t,x,y):
    A = 1.2
    w = 2**np.pi/10 
    m = 8.53
    return A*np.sin(w*t) - x + m*(1-x**2)*y

def dx(t,x,y):
    return y

y = [0]
x = [0.5]
t = [0]
N = 100000
h = 100/(N-1)

for n in range(N):
    t.append(t[n]+h)
    kx1 = dx(t[n],x[n],y[n])
    ky1 = dy(t[n],x[n],y[n])

    kx2 = dx(t[n]+(h/2),x[n]+(h*kx1)/2,y[n]+(h*ky1)/2)  
    ky2 = dy(t[n]+(h/2),x[n]+(h*kx1)/2,y[n]+(h*ky1)/2)

    kx3 = dx(t[n]+(h/2),x[n]+(h*kx2)/2,y[n]+(h*ky2)/2)
    ky3 = dy(t[n]+(h/2),x[n]+(h*kx2)/2,y[n]+(h*ky2)/2)  

    kx4 = dx(t[n]+(h/2),x[n]+(h*kx3)/2,y[n]+(h*ky3)/2)
    ky4 = dy(t[n]+(h/2),x[n]+(h*kx3)/2,y[n]+(h*ky3)/2) 
  
    x.append(x[n]+(h/6)*(kx1+2*kx2+2*kx3+kx4))
    y.append(y[n]+(h/6)*(ky1+2*ky2+2*ky3+ky4)) 
    

plt.figure(figsize=(15,5))
plt.subplot(1,3,1)
plt.plot(t,x,'b', label = "x(t)")
plt.grid(True)
plt.legend()
plt.subplot(1,3,2)
plt.plot(t,y,'g', label = "y(t)")
plt.grid(True)
plt.legend()
plt.subplot(1,3,3)
plt.plot(y,x,'r', label = "dx/dt(t) vs x(t)")
plt.grid(True)
plt.legend()