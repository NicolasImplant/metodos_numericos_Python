import matplotlib.pyplot as plt
import numpy as np

def f(x):
  return np.sin(x)

def integral(N, n = []):
  a = 0
  b = np.pi
  h = (b-a)/(N-1)
  x = a
  area = 0
  for i in range(N):
    area += h*(f(x)+f(x+h))/2
    n.append(area)
    x += h
  return area, n

def error(list):
  error = []
  for i in range(1, len(list)):
    error.append(abs((list[i]-list[i-1])/list[i]))
  return error

v = []
x, v = integral(20,v)

print(f'El área bajo la curva de la intregal es {x}')
plt.plot(v,'b', label = "Área")
plt.plot(error(v), 'r', label = "error")
plt.grid(True)
plt.xlabel("Iteraciones", fontsize = 15)
plt.legend()
plt.show()