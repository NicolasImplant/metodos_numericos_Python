from functions import constantMultiplier, primeNumber

# Función que ejecuta de manera ciclica y recursiva el algoritmo de productos medios, debido a que es similar al multiplicador
# constante, es posible ejecutar el mismo algoritmo variando el parametro del multiplicador. 

# Function that cyclically and recursively executes the mean products algorithm, since it is similar to the multiplier
# constant, it is possible to execute the same algorithm by varying the multiplier parameter.

def pseudoRandNumbers(seeds:list, random_numbers:list):
    for i in range(1,N-1):
        seeds[i+1] , random_numbers[i] = constantMultiplier(seeds[i],seeds[i-1])
    return random_numbers


if __name__ == '__main__':

# Área en la que debemos ingresar los parametros del modelo, en este caso se utilizan números primos de cuatro cifras para las semillas. 

# Area in which we must enter the parameters of the model, in this case four-digit prime numbers are used for the seeds.

    seed1 = primeNumber()
    seed2 = primeNumber()
    N = int(input('Ingresa la cantidad de valores aleatorios:     ')) + 2
    seeds = [0 for i in range(N)]    
    seeds[0] = seed1
    seeds[1] = seed2
    random_numbers = [0 for i in range(N-1)]
    print(pseudoRandNumbers(seeds, random_numbers))