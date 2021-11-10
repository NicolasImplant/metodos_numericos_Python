import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

def u(x,y):
    return np.sin(x*y)

f = 1000
c = 15
c_1 = 3
L = np.pi
T = 10

h_x = L/(c-1)
h_t = T/(f-1)

M = np.zeros((f,c))

for n in range(c):
    M[0,n] = (n**2)*h_x*(np.pi-n*h_x)
    M[1,n] = M[0,n] + h_t*u(n,h_x)

for n in range(2,f-1):
    for m in range(1,c-1):
        M[n+1,m] = 2*M[n,m] - M[n-1,m] + (((h_t*c_1)/h_x)**2)*(M[n,m-1]-2*M[n,m]+M[n,m+1])
        M[n,0] = 0
        M[n,c-1] = 0

x = np.linspace(0,L,c)
plt.plot(x,M[0,:])
plt.grid(True)
plt.show()

for k in range(f):
    plt.plot(x,M[k,:])
    plt.grid(True)

fig, ax = plt.subplots()
ax.set_xlim((0,L))
ax.set_ylim((-600,600))
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