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

Integral definida entre π/2 y -π/2 de: log(cos(x))

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

-- Punto 4 --

Ecuación difrencial de segundo orden de la forma: d^2x/dt^2 - µ(1 - x^2)dx/dt + x = Asen(ωt); con condiciones iniciales:
x(0) = 0.5; dx/dt(0) = 0; ω(0) = 2π/10; µ = 8.53; A = 1.2; Para un intervalo de tiempo: 0 < t < 100. Metodo de solución: Runge Kutta


-- Punto 5 --

Ecuacion de Jerk (Orden superior) de la forma: d^3x/dt^3 + A d^2x/dt^2 - x(dx/dt)^2 + x^3 = 0; con condicones iniciales A = 3.6;
x(0) = 0; dx/dt(0) = 0; d^2x/dt^2(0) = 1; Metodo de solución: Punto Medio.

-- Punto 6 --

Modelo epidemiologico SIRD (Suceptibles, infectados, recuperados, fallecidos) de la forma: dS/dt = -β(SI/N) | 
dI/dt = β(SI/N) - (γ+µ)I | dR/dt = γI | dD/dt = µI; con condiciones iniciales: S(0) = 997; I(0) = 3; R(0) = 0; D(0) = 0; con los
parametros: β = 4, γ = 0.035; µ = 0.005; N = S(t) + I(t); para un intervalo de tiempo: 0 < t < 100. Metodo de solución: Heun