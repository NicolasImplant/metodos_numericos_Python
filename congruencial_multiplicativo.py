from functions import multiplicativo


# Función que ejecuta de manera cíclica y recursiva el algoritmo congruencial multiplicativo, los parámetros k y g se manipularon
# para garantizar el ciclo de vida máximo del generador


# Function that cyclically and recursively executes the multiplicative congruential algorithm, the parameters k and g were manipulated
# to ensure maximum generator life cycle

def pseudoRandNumbers(seed:int, k:int, g:int, N:int) -> list:
    a = 5 + 8*k
    m = 2**g
    x = [0 for i in range(N)]
    random_numbers = [0 for i in range(N)]
    x[0] = seed

    for i in range(N-1):
        x[i+1], random_numbers[i] = multiplicativo(a,x[i],m)
    return random_numbers

if __name__ == '__main__':

# Área de ingreso de los parámetros del modelo.  

# Entry area of ​​the model parameters.

    try:
        seed = int(input('Digita el valor de la semilla:   '))    
        k = int(input('Digita el valor de la constante de k:   '))
        g = int(input('Digita el valor de la constante de g:   '))
        if seed < 10 or k < 10 or g < 10:
            raise ValueError  
        N = int(input('Digita la cantidad de números aleatorios requerida:  ')) + 1
        print(pseudoRandNumbers(seed,k,g,N))
    except ValueError:
        print('Para un ciclo de vida máximo, los valores de las constantes y la semilla deben ser mayores a 10')