from functions import cuadratico

# Función que ejecuta de manera cíclica y recursiva el algoritmo congruencial multiplicativo, los parámetros k y g se manipularon
# para garantizar el ciclo de vida máximo del generador

# Function that cyclically and recursively executes the multiplicative congruential algorithm, the parameters k and g were manipulated
# to ensure maximum generator life cycle

def pseudoRandNumbers(seed:int, a:int, b:int, c:int, g:int, N:int):
    m = 2**g
    x = [0 for i in range(N)]
    random_numbers = [0 for i in range(N)]
    x[0] = seed

    for i in range(N-1):
        x[i+1], random_numbers[i] = cuadratico(x[i],a,b,c,m)

    return random_numbers

# Área de ingreso de los parámetros del modelo.  

# Entry area of ​​the model parameters.

if __name__ == '__main__':
    
    try:
        seed = int(input('Digita el valor de la semilla:   '))    
        a = int(input('Digita el valor de la constante de a:   '))
        b = int(input('Digita el valor de la constante de b:   '))
        c = int(input('Digita el valor de la constante de c:   '))
        if a == 1 and b == 0 and c == 0:
            raise ValueError  
        g = int(input('Digita el valor de la constante de g (m = 2^g) :   '))
        N = int(input('Digita la cantidad de números aleatorios requerida:  ')) + 1
        print(pseudoRandNumbers(seed,a,b,c,g,N))
    except ValueError:
        print('Para a = 1, b = 0, y c = 0; aplicar el agoritmo Blum, Blum y Shub')