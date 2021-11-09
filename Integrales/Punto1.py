import matplotlib.pyplot as plt
import numpy as np

def f(x):
  return np.exp(-x/3)*np.cos(x)

def integral(N):
  x = [0 for i in range(N)]
  a = 0
  b = 40
  h = (b-a)/(N-1)
  area = 0
  for n in range(N-1):
    x[n+1]=x[n]+h
    area+=(h/6)*(f(x[n])+4*f(x[n]+h/2)+f(x[n+1]))
  return area

def error(list):
  error = []
  for i in range(1, len(list)):
    error.append(abs((list[i]-list[i-1])/list[i]))
  return error

m = 200
A = []

for i in range(2,m):
  A.append(integral(i))

print(f'El área bajo la curva de la intregal es {integral(i)}')
plt.plot(A,'b', label = "Área")
plt.plot(error(A), 'r', label = "error")
plt.grid(True)
plt.xlabel("Iteraciones", fontsize = 15)
plt.legend()
plt.show()