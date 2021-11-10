import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

def u(x,y,z):
    return np.sin(np.pi*x*y/z)

N = 50
f = 900
c = N
L = 10
T = 1000
a = 0.01

h_x = L/(c-1)
h_t = T/(f-1)

M = np.zeros((f,c))
M[:,0] = 0
M[:,-1] = 0

for n in range(c-1):
    M[0,n] = u(n,h_x,L)

for n in range(f-1):
    for m in range(1,c-1):
        M[n+1,m] = M[n,m] + a*(h_t/h_x**2)*(M[n,m+1]-2*M[n,m]+M[n,m-1])
        M[n+1,0] = M[n+1,1]
        M[n+1,c-1] = M[n+1,c-2]

x = np.linspace(0,L,c)
plt.plot(x,M[0,:])
plt.grid(True)
plt.show()

for k in range(f):
    plt.plot(x,M[k,:])
    plt.grid(True)


fig, ax = plt.subplots()
ax.set_xlim((0,L))
ax.set_ylim((0,1))
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