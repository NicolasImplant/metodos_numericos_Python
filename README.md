# metodos_numericos_Python
Resolviendo derivadas, integrales, y ecuaciones diferenciales de primer y segundo orden en lenguaje Python

# Integrales

-- Punto 1 --

Integral definida entre 0 y 40 de: e^(-x/3)*cos(x)

-- Punto 2 --

Integral definida entre -1 y 1 de: raiz(1-x^2)

-- Punto 3 --

Integral definida entre 0 y 100 de: Sen(x^2)/x

-- Punto 4 -- 

Integral definida entre 0 y pi de: Sen(x)

-- Punto 5 --

Integral definida entre pi/2 y -pi/2 de: log(cos(x))

# Ecuaciones diferenciales

-- Punto 1 --

Modelo cazador presa de la forma: dx/dt = 3x - xy | dy/dt = xy - 2y ; con condiciones iniciales: x(0) = 1 ; y(0) = 2 ; 
y para un intervalo de tiempo 0 < t < 20. Metodo de solución : Runge Kutta.

-- Punto 2 --

Modelo epidemiologico SIR (Suceptibles, infectados, recuperados) de la forma: dR/dt = 0.6I | dI/dt = -0.6I + 0.001407S*I |
dS/dt = -0.001407S*I; con codiciones iniciales: I(0) = 5; S(0) = 995; R(0) = 0; para un intervalo de tiempo 0 < t < 24. Metodo 
de solución: Heun

-- Punto 3 --

Atractor de Lorenz de la forma: dx/dt = 10(x-y) | dy/dt = x(27-z) | dz/dt = xy - (8/3)z ; con condiciones iniciales: 
x(0) = 1 ; y(0) = 0 ; z(0) = 0 ; par un intervalo de tiempo 0 < t < 50. Metodo de solución: Punto Medio.



