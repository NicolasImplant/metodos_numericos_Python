from functions import square_mean, primeNumber

# Función que itera de manera cíclica y recursiva el algoritmo de generación de pseudoaleatorios. 
# Function that cyclically and recursively iterates the pseudo-random generation algorithm.

def Pseudorandom_numbers(seeds:list,randoms:list,N:int) ->list:
    for i in range(N-1):
        seeds[i+1], randoms[i] = square_mean(seeds[i])
    return randoms

if __name__ == '__main__':

# Inicializador del algoritmo, el usuario ingresa la cantidad de números deseados por el usuario.
# Algorithm initializer, the user enters the number of numbers desired by the user

    N = int(input('Enter how many random numbers do you require:     '))
    seeds = [0 for i in range(N)]
    random_numbers = [0 for i in range(N-1)]
    seeds[0] = primeNumber()

    print(Pseudorandom_numbers(seeds,random_numbers,N))    