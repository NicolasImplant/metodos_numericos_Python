import random as rd

# Función que recibe un número entero y regresa una lista con todas sus cifras
# Function that receives an integer and returns a list with all its figures

def numero(x:int,n:list=[]) -> list:
    num1 = x % 10
    num2 = x // 10
    n.append(num1)
    if num2 != 0:
        return numero(num2,n)
    else:
        return n[::-1]

# Función que recibe una lista de 4 itmes y regresa un número entero
# Function that receives a list of 4 items and returns an integer

def vector(v:list) -> int:
    if sum(v) < 1:
        return 0
    return v[0]*1000 + v[1]*100 + v[2]*10 + v[3]*1

# Función que recibe la semilla y aplica el algoritmo de cuadrados medios retorna el número aleatorio y la nueva semilla
# Function that receives the seed and applies the mean squares algorithm returns the random number and the new seed    

def square_mean(Seed:int, v:list=[], random:dict={}) -> list:
    try:
        return random[Seed]
    except KeyError:
        w = []
        v = numero(Seed**2,w)
        while len(v) % 2 != 0:
            v.append(0)
            v = v[-1::] + v[:-1:]
        if len(v) == 8:        
            v = v[2:-2]
        else:
            v = v[int((8-len(v))/2):int(-(8-len(v))/2)]
    random[Seed] = [vector(v),vector(v)/(10**4)]        
    return random[Seed]

# Función que recibe la semilla y aplica el algoritmo de multiplicador constante retorna el número aleatorio y la nueva semilla
# Function that receives the seed and applies the constant multiplier algorithm returns the random number and the new seed    

def constantMultiplier(mult:int, Seed:int, v:list=[], random:dict={}) -> list:
    try:
        return random[Seed*mult]
    except KeyError:
        w = [] 
        v = numero(mult*Seed,w)
        while len(v) % 2 != 0:
            v.append(0)
            v = v[-1::] + v[:-1:]
        if len(v) == 8:
            v = v[2:-2]
        else:
            v = v[int(8-len(v)/2):int(-(8-len(v)/2))]
    random[Seed*mult] = [vector(v), vector(v)/(10**4)]
    return random[Seed*mult]


# Función que recibe la semilla y aplica el algoritmo de productos medios retorna el número aleatorio y la nueva semilla
# Function that receives the seed and applies the product mean algorithm returns the random number and the new seed  


def product_mean(Seed1:int,Seed2:int, v:list=[], random:dict={}) -> list:
    try:
        return random[Seed1*Seed2]
    except KeyError:
        w = [] 
        v = numero(Seed1*Seed2,w)
        while len(v) % 2 != 0:
            v.append(0)
            v = v[-1::] + v[:-1:]
        if len(v) == 8:
            v = v[2:-2]
        else:
            v = v[int(8-len(v)):int(-(8-len(v)))]
    random[Seed1*Seed2] = [vector(v),vector(v)/(10**4)]
    return random[Seed1*Seed2]    

# Función que genera números primos de cuatro cifras para generar semillas.
# Function that generates four-digit prime numbers to generate seeds.

def primeNumber(primes:list=[]) -> list:
    x = {n:[i for i in range(1,n+1) if n % i == 0] for n in range(2000,6000)}
    for key, value in x.items():
        if len(value) == 2:
            primes.append(key)
    return primes[rd.randint(0,len(primes))]


# Función que genera el numero aleatorio y lo regresa junto con el siguiente paso.
# Function that generates the random number and returns it along with the next step.

def multiplicativo(a:int, x:int ,m:int, random:dict ={}) -> int:
    try: 
        return random[a,x,m]
    except KeyError:
        random[a,x,m] = [ (a*x) % m, ((a*x) % m)/(m-1) ]
        return random[a,x,m] 

# Función que genera el numero aleatorio y lo regresa junto con el siguiente paso.
# Function that generates the random number and returns it along with the next step.

def cuadratico(x:int,a:int,b:int,c:int,m:int,random:dict={}) -> list:
    try:
        return random[x,a,b,c,m]
    except KeyError:
        random[x,a,b,c,m] = [((a*x**2) + (b*x) + c) % m, (((a*x**2) + (b*x) + c) % m) / (m-1)]
    return random[x,a,b,c,m]
