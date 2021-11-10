import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

def u(x,y,z):
    return np.sin(np.pi*x*y/z)

def v(x,y,z):
    return np.cos(np.pi*x*y/z)

f = 450
c = 15
c_1 = 0.3
L = 10
T = 1000

h_x = L/(c-1)
h_t = T/(f-1)

M = np.zeros((f,3*c))

for n in range(3*c):
    if n*h_x >= 0 and n*h_x <= c:
        M[0,n] = u(n,h_x,L)
        M[1,n] = M[0,n] - ((h_t*c_1*np.pi)/L)*v(n,h_x,L)
    if n*h_x > c and n*h_x <= 2*c:
        M[1,n] = M[0,n]
    if n*h_x > 2*c and n*h_x <= 3*c:
        M[0,n] = u(n,h_x,L)
        M[1,n] = M[0,n] + ((h_t*c_1*np.pi)/L)*v(n,h_x,L)
      
for n in range(2,f-1):
    for m in range(1,3*c-1):    
        M[n+1,m] = 2*M[n,m] - M[n-1,m] + (((h_t*c_1)/h_x)**2)*(M[n,m-1]-2*M[n,m]+M[n,m+1])
        M[n,0] = 0
        M[n,3*c-1] = M[n,3*c-2]

x = np.linspace(0,3*L,3*c)

plt.plot(x,M[0,:])
plt.plot(x,M[1,:])
plt.grid(True)
plt.show()

for k in range(f):
    plt.plot(x,M[k,:])
    plt.grid(True)

fig, ax = plt.subplots()
ax.set_xlim((0,3*L))
ax.set_ylim((-5,5))
ax.grid(True)
line, = ax.plot([],[], lw=3, color = 'b')
ax.set_title('Solución U(x)')

def init():
  line.set_data([],[])
  return (line,)

def animate(i):
  y = M[i,:]
  line.set_data(x,y)
  return (line,)

anim = FuncAnimation(fig, animate, init_func=init, frames=f, interval = 50, blit = True)
HTML(anim.to_html5_video())