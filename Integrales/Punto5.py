import matplotlib.pyplot as plt
import numpy as np

def f(x):
  return np.log(np.cos(x))

def integral(N):
  a = -np.pi/2
  b = np.pi/2
  h = (b-a)/(N-1)
  x = a + h
  area = 0
  for i in range(N-2):
    area+=h*f(x)
    x += h  
  return area

def error(list):
  error = []
  for i in range(1, len(list)):
    error.append(abs((list[i]-list[i-1])/list[i]))
  return error

m = 1000
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