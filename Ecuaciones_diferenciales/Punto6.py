import numpy as np
import matplotlib.pyplot as plt

def R(t,i):
    gamma = 0.035
    return gamma*i

def I(t,s,i):
    beta = 0.4
    gamma = 0.035
    mu = 0.005
    N = s + i
    return (beta*s*i)/N - (gamma + mu)*i

def S(t,s,i):
    beta = 0.4
    N = s + i
    return (-beta*s*i)/N

def D(t,i):
    mu = 0.005
    return mu*i

i = [3]
s = [997]
r = [0]
d = [0]
t = [0]
N = 1000
h = 100/(N-1)


for n in range(N):
    t.append(t[n]+h)
    r.append(r[n]+(h/2)*(R(t[n],i[n])+R(t[n]+h,i[n]+h*R(t[n],i[n]))))
    d.append(d[n]+(h/2)*(D(t[n],i[n])+D(t[n]+h,i[n]+h*D(t[n],i[n]))))
    i.append(i[n]+(h/2)*(I(t[n],s[n],i[n])+I(t[n]+h,s[n]+h*I(t[n],s[n],i[n]),i[n]+h*I(t[n],s[n],i[n]))))
    s.append(s[n]+(h/2)*(S(t[n],s[n],i[n])+S(t[n]+h,s[n]+h*S(t[n],s[n],i[n]),i[n]+h*S(t[n],s[n],i[n]))))
  

plt.plot(t,r,'g', label = "R(t)")
plt.plot(t,i,'r', label = "I(t)")
plt.plot(t,s,'b', label = "S(t)")
plt.plot(t,d,'black', label = "D(t)")
plt.grid(True)
plt.legend()