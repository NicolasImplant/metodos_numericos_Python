def Lehmer(a,x,c,m):
    x1 = (a*x + c) % m
    x2 = x1 / (m-1)
    return x1, x2

if __name__ == '__main__':
    try:
        print('Condiciones Banks, Carson, Nelson y Nicol')
        seed = int(input('Digita el valor de la semilla:   '))
        k = int(input('Digita el valor de la constante de k:   ')) 
        g = int(input('Digita el valor de la constante de g:   '))    
        c = int(input('Digita el valor de la constante de aditiva:   '))
        if seed < 10 or k < 10 or g < 10 or c < 10:
            raise ValueError    
        N = int(input('Cantidad de números aleatorios deseada:  '))
        m = (2**g)
        a = 1 + 4*k
        x = [0 for i in range(N)]
        r = [0 for i in range(N-1)]
        x[0] = seed

        for i in range(N-1):
            x[i+1], r[i] = Lehmer(a,x[i],c,m)        
        print(r)
    except ValueError:
        print('Para un ciclo de vida máximo, los valores de las constantes y la semilla deben ser mayores a 10')