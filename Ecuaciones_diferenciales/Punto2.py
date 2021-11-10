import numpy as np
import matplotlib.pyplot as plt

def R(t,x):
      return 0.6*x

def I(t,x,y):
  return -0.6*x+0.001407*y*x

def S(t,x,y):
  return -0.001407*y*x

i = [5]
s = [995]
r = [0]
t = [0]
N = 10000
h = 20/(N-1)


for n in range(N):
  t.append(t[n]+h)
  r.append(r[n]+(h/2)*(R(t[n],i[n])+R(t[n]+h,i[n]+h*R(t[n],i[n]))))
  i.append(i[n]+(h/2)*(I(t[n],i[n],s[n])+I(t[n]+h,i[n]+h*I(t[n],i[n],s[n]),s[n]+h*I(t[n],i[n],s[n]))))
  s.append(s[n]+(h/2)*(S(t[n],i[n],s[n])+S(t[n]+h,i[n]+h*S(t[n],i[n],s[n]),s[n]+h*S(t[n],i[n],s[n]))))

plt.plot(t,r,'b', label = "R(t)")
plt.plot(t,i,'r', label = "I(t)")
plt.plot(t,s,'g', label = "S(t)")
plt.grid(True)
plt.xlabel('Tiempo', fontsize = 10 )
plt.legend()