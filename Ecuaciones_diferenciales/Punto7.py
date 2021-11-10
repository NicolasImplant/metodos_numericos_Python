import numpy as np
import matplotlib.pyplot as plt

def f(x):
    g = 9.81                                             # m/s
    l = 2                                                # largo del cable
    return (-g/l)*np.sin(x)

def inicio(v,a,dt):                                      # Inicializador Verlet Pendulo Simple
    return a - v * dt + (f(a)/2) * dt**2

def verlet(x_f,N,v,a):
    dt =  x_f/(N-1)                                      # Tamaño del intervalo
    x_s = np.arange(0,x_f+dt,dt)
    y_i = [0 for i in range(len(x_s))]
    y_i[0] = inicio(v,a,dt)
    y_i[1] = a
    for i in range(1,N-1):
        y_i[i+1] = 2*y_i[i] - y_i[i-1] + f(y_i[i])*dt**2
    return y_i

def verlet_f(x_f,N,v,a):
    k = 0.9                                              # Constante de friccion
    m = 4                                                # Masa de la particula
    dt =  x_f/(N-1)                                      # Tamaño del intervalo
    x_s = np.arange(0,x_f+dt,dt)
    y_i = [0 for i in range(len(x_s))]
    v_i = [0 for i in range(len(x_s))]
    y_i[0] = inicio(v,a,dt)
    y_i[1] = a
    v_i[0] = v
    for i in range(1,N-1):
        v_i[i+1] = v_i[i] + ((f(y_i[i])+f(y_i[i+1])))*dt/(2*m)
        y_i[i+1] = 2*y_i[i] - y_i[i-1] + (f(y_i[i])-k*v_i[i])*dt**2
    return y_i

if __name__ == '__main__':
    x_f = 10                                              # Limite superior del intervalo
    N = 1000                                              # Número de itervalos
    v = 0.5                                               # Velocidad inicial
    P_i = 0.5                                             # posición inicial

    plt.figure(figsize=(15,5))
    plt.subplot(1,2,1)
    plt.plot(verlet(x_f,N,v,P_i), 'b', label = "Pendulo simple libre")
    plt.grid(True)
    plt.legend()
    plt.subplot(1,2,2)
    plt.plot(verlet_f(x_f,N,v,P_i), 'r', label = "Pendulo simple con fricción")
    plt.grid(True)
    plt.legend()