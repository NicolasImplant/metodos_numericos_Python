import matplotlib.pyplot as plt
import numpy as np

def f(x):
  return (1-x**2)**(1/2)

def integral(N):
  a = -1
  b = 1
  h = (b-a)/(N-1)
  x = a
  area = 0
  A = []
  for i in range(N):
    area += (h/2)*(f(x)+f(x+h))
    x += h
  return area

def error(list):
  error = []
  for i in range(1,len(list)):
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