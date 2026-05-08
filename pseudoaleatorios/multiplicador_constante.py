from functions import constantMultiplier, primeNumber

# Función que itera de manera cíclica y recursiva el algoritmo de generación de pseudoaleatorios. 
# Function that cyclically and recursively iterates the pseudo-random generation algorithm.

def pseudoRandomNumbers(mult:int, seeds:list, random_numbers:list, N:int) -> list:
    for i in range(N-1):
        seeds[i+1] , random_numbers[i] = constantMultiplier(mult,seeds[i])
    return random_numbers


if __name__ == '__main__':

# Inicializador del algoritmo, el usuario ingresa la cantidad de números deseados por el usuario.
# Algorithm initializer, the user enters the number of numbers desired by the user

    mult = primeNumber()
    N = int(input('Ingresa la cantidad de valores aleatorios:     ')) + 1
    seeds = [0 for i in range(N)]    
    seeds[0] = primeNumber()
    random_numbers = [0 for i in range(N-1)]
    print(pseudoRandomNumbers(mult, seeds, random_numbers, N))