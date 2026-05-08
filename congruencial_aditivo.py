def aditivo(n,m,mod):
    x = (n+m) % mod
    r = x / (mod - 1)
    return x,r    

if __name__ == '__main__':
    x = [0 for i in range(5)]
    for i in range(5):
        x[i] = int(input(f'Ingresa la posición {i+1} del vector inicial:   '))

    N = int(input('Cantidad de números aleatorios deseada:  '))
    m = 100
    r = [0 for i in range(N-1)]

    for i in range(N-1):
        n, r[i] =  aditivo(x[i],x[-1],m)
        x.append(n)

print(r)