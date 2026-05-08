# Generadores de Números Pseudoaleatorios

**Implementación de referencia en Python 3.12 — arquitectura hexagonal, tipado estático**

Colección de generadores de números pseudoaleatorios (GNPA) clásicos, implementados como objetos con contratos explícitos y validación estadística integrada. El proyecto sirve como material de estudio para cursos de posgrado en simulación estocástica, modelamiento computacional y estadística computacional. Cada algoritmo documenta sus condiciones de período máximo, sus invariantes algebraicos y sus limitaciones conocidas.

---

## Contenido

1. [Fundamentos teóricos](#1-fundamentos-teóricos)
2. [Generadores implementados](#2-generadores-implementados)
3. [Pruebas estadísticas de calidad](#3-pruebas-estadísticas-de-calidad)
4. [Arquitectura del software](#4-arquitectura-del-software)
5. [Instalación y uso](#5-instalación-y-uso)
6. [Variables de entorno](#6-variables-de-entorno)
7. [Referencias](#7-referencias)

---

## 1. Fundamentos teóricos

### 1.1 Definición y requisitos

Un **generador de números pseudoaleatorios** es un algoritmo determinista

$$G : \mathbb{Z} \to \{x_0, x_1, x_2, \ldots\}$$

que, a partir de una **semilla** $x_0$, produce una secuencia periódica de enteros que imita estadísticamente una muestra i.i.d. de la distribución uniforme discreta. La secuencia normalizada

$$r_n = \frac{x_n}{m} \in [0, 1)$$

debe aproximar realizaciones de $U(0,1)$. Todo generador de números aleatorios no nulos en sistemas físicos finitos es por definición periódico; la calidad se mide por la longitud del período y la superación de pruebas estadísticas de uniformidad e independencia.

### 1.2 Período y ciclo de vida

Sea $\mathbf{x} = (x_0, x_1, x_2, \ldots)$ la secuencia generada. El **período** $p$ es el menor entero positivo tal que $x_{n+p} = x_n$ para todo $n$ suficientemente grande. El **período máximo teórico** para un generador con módulo $m$ es $m$ (para generadores lineales con $c \neq 0$) o $m/4$ (para generadores multiplicativos con $m = 2^g$).

Un período corto implica repetición prematura; en simulación estocástica se recomienda $p \gg N$ donde $N$ es el número total de muestras requeridas. La detección del período se implementa mediante la primera colisión en la secuencia.

### 1.3 Distribución objetivo y normalización

La normalización estándar para módulo $m$ es:

$$r_n = \frac{x_n}{m - 1} \quad \Rightarrow \quad r_n \in \left[0, 1\right]$$

o en su variante semicerrada:

$$r_n = \frac{x_n}{m} \quad \Rightarrow \quad r_n \in \left[0, 1\right)$$

Los métodos de cuadrados/productos medios usan $m = 10^4$ (4 dígitos decimales); los métodos congruenciales usan $m = 2^g$ (potencia de 2 elegida para eficiencia en aritmética binaria).

---

## 2. Generadores implementados

### 2.1 Cuadrados medios (Von Neumann, 1946)

El generador más antiguo de la era computacional, propuesto por John Von Neumann para el proyecto ENIAC:

$$x_{n+1} = \text{middle}_4\!\left(x_n^2\right)$$

donde $\text{middle}_4(\cdot)$ extrae los 4 dígitos centrales del entero de 8 dígitos obtenido al elevar al cuadrado (rellenando con ceros a la izquierda si es necesario):

$$x_n^2 \xrightarrow{\text{zfill}(8)} \underbrace{d_7 d_6}_{\text{descartar}} \underbrace{d_5 d_4 d_3 d_2}_{\text{conservar}} \underbrace{d_1 d_0}_{\text{descartar}}$$

**Normalización:** $r_n = x_{n+1} / 10^4$.

**Propiedades y limitaciones:**

- Período teórico máximo: $\leq 10^4 = 10\,000$, frecuentemente mucho menor.
- Puntos fijos conocidos: $x = 0$ (degeneración absoluta), $x = 100$, $x = 2500$, entre otros.
- El período depende críticamente de la semilla; algunas semillas producen ciclos de longitud 1 o 2.
- **No recomendado** para simulación estocástica seria; incluido por completitud histórica y pedagógica.

**Requerimientos:** semilla de 4 dígitos ($1000 \leq x_0 \leq 9999$).

---

### 2.2 Multiplicador constante

Variante del método de Von Neumann donde el cuadrado es reemplazado por el producto con una constante fija:

$$x_{n+1} = \text{middle}_4\!\left(c \cdot x_n\right)$$

con $c$ un número primo de 4 dígitos (elegido aleatoriamente si no se especifica).

**Propiedades:** Período mayor que cuadrados medios para semillas no degeneradas, pero igualmente inadecuado para aplicaciones serias. El multiplicador primo reduce la probabilidad de ciclos degenerados.

**Requerimientos:** semilla de 4 dígitos; `config.multiplier` (0 = auto-primo vía Criba de Eratóstenes).

---

### 2.3 Productos medios

Generalización a dos semillas donde el producto cruzado reemplaza al cuadrado:

$$x_{n+1} = \text{middle}_4\!\left(x_n \cdot x_{n-1}\right)$$

La secuencia requiere dos valores iniciales $x_0$ y $x_1$ (ambos primos de 4 dígitos por defecto). La estructura de dos semillas incrementa la complejidad del espacio de estados pero no garantiza períodos largos.

**Requerimientos:** `config.seed` = $x_0$; `config.multiplier` = $x_1$ (0 = auto-primo).

---

### 2.4 Generador congruencial lineal — GCL (Lehmer, 1951)

El método más ampliamente utilizado en la práctica. Define la recurrencia:

$$x_{n+1} = (a \cdot x_n + c) \bmod m$$

con $r_n = x_n / (m - 1)$.

**Teorema de Hull y Dobell (1962) — condiciones de período completo** ($p = m$):

Sea $m > 0$, $0 < a < m$, $0 \leq c < m$, $0 \leq x_0 < m$. Entonces el GCL tiene período $m$ si y sólo si:

1. $\gcd(c, m) = 1$
2. Si $p$ es primo y $p \mid m$, entonces $p \mid (a - 1)$
3. Si $4 \mid m$, entonces $4 \mid (a - 1)$

**Condiciones Banks-Carson-Nelson-Nicol** para $m = 2^g$:

$$a = 1 + 4k, \quad c \text{ impar}, \quad g \geq 3$$

Bajo estas condiciones el período es exactamente $m = 2^g$.

**Parámetros clásicos** (Numerical Recipes, Press et al.):

| $a$ | $c$ | $m$ | Referencia |
|:---:|:---:|:---:|:----------|
| 1 664 525 | 1 013 904 223 | $2^{32}$ | Numerical Recipes in C |
| 6 364 136 223 846 793 005 | 1 442 695 040 888 963 407 | $2^{64}$ | PCG family |
| 1 103 515 245 | 12 345 | $2^{31}$ | glibc (BSD `rand`) |

**Requerimientos:** `seed`, `count`, `modulus` ($= 2^g$), `multiplier` ($a$), `increment` ($c \neq 0$).

---

### 2.5 Generador congruencial multiplicativo — GCM

Caso especial del GCL con $c = 0$:

$$x_{n+1} = a \cdot x_n \bmod m$$

**Período máximo** con $m = 2^g$: el período es a lo más $m/4$ (nunca período completo para $c = 0$ y $m$ potencia de 2). Se alcanza cuando:

$$a \equiv 5 \pmod{8} \quad \Longleftrightarrow \quad a = 5 + 8k, \quad k \geq 1$$

y la semilla es **impar** (requisito necesario: $\gcd(x_0, m) = 1$, que para $m = 2^g$ equivale a $x_0$ impar).

**Demostración (sketch):** La secuencia $\{a^n x_0 \bmod 2^g\}$ genera el subgrupo $\langle a \rangle \leq (\mathbb{Z}/2^g\mathbb{Z})^*$. El grupo $(\mathbb{Z}/2^g\mathbb{Z})^*$ tiene orden $\phi(2^g) = 2^{g-1}$, pero no es cíclico para $g \geq 3$; se descompone como $\mathbb{Z}/2 \times \mathbb{Z}/2^{g-2}$. El generador $a \equiv 5 \pmod{8}$ tiene orden $2^{g-2}$ en este grupo, que es el máximo alcanzable, equivalente a $m/4$.

**Comparación con GCL:** Más eficiente (sin suma), pero período máximo $m/4$ en lugar de $m$.

**Requerimientos:** `seed` (impar), `count`, `modulus` ($= 2^g$), `multiplier` ($a = 5 + 8k$).

---

### 2.6 Generador congruencial aditivo — Fibonacci retrasado (Lagged Fibonacci Generator)

$$x_{n} = \left(x_{n-1} + x_{n-\ell}\right) \bmod m$$

donde $\ell \geq 2$ es el **retardo** (*lag*) determinado por el tamaño del vector inicial. Requiere los $\ell$ valores semilla $x_0, x_1, \ldots, x_{\ell-1}$.

**Período teórico:** Para $m = 2^g$ y vector inicial no nulo, el período puede alcanzar $(2^\ell - 1) \cdot 2^{g-1}$, exponencialmente mayor que el GCL. Pares $(p, q)$ de retardos con propiedades óptimas son conocidos: $(17, 5)$, $(31, 13)$, $(55, 24)$, $(521, 32)$, $(1279, 418)$ (Fibonacci Additive con propiedades verificadas de período maximal).

**Relación con sucesiones de Fibonacci:** Para $m \to \infty$, $\ell = 2$, $x_0 = x_1 = 1$:

$$x_n = F_n \quad \text{(números de Fibonacci)}$$

El cociente $x_{n+1}/x_n \to \varphi = (1+\sqrt{5})/2$ (razón áurea), lo que sugiere buenas propiedades de equidistribución en dimensión 2.

**Debilidad:** Las primeras $\ell$ muestras son determinadas directamente por las semillas; es necesario descartar los primeros $10\ell$ valores (warm-up) para convergencia estadística.

**Requerimientos:** `count`, `modulus`, `lag_vector` (tupla de enteros, longitud $\geq 2$).

---

### 2.7 Generador congruencial cuadrático

Generalización no lineal de la recurrencia congruencial:

$$x_{n+1} = \left(a x_n^2 + b x_n + c\right) \bmod m$$

con $r_n = x_n / (m - 1)$.

**Caso degenerado $a = 1, b = 0, c = 0$:** Reduce a $x_{n+1} = x_n^2 \bmod m$, conocido como el **generador cuadrático puro** o precursor del generador Blum-Blum-Shub (BBS). En BBS, $m = p \cdot q$ con $p, q \equiv 3 \pmod{4}$ primos de Blum, lo que garantiza propiedades criptográficas (dificultad computacional bajo la hipótesis de factorización). Esta implementación rechaza el caso degenerado y remite a una implementación BBS dedicada.

**Análisis de período:** A diferencia del caso lineal, no existe un teorema general de período completo. El período depende de las raíces del polinomio $f(x) = ax^2 + bx + c$ sobre $\mathbb{Z}/m\mathbb{Z}$. Para $m$ primo, el período máximo es $m - 1$ cuando $f(x)$ no tiene raíces en $\mathbb{F}_m$.

**Requerimientos:** `seed`, `count`, `modulus`, `coeff_a` ($a$), `coeff_b` ($b$), `coeff_c` ($c$), con $(a, b, c) \neq (1, 0, 0)$.

---

## 3. Pruebas estadísticas de calidad

La calidad de un GNPA se evalúa mediante pruebas estadísticas que buscan falsificar las hipótesis nulas $H_0$ de uniformidad e independencia. Un generador de buena calidad **supera** estas pruebas; uno de mala calidad las falla sistemáticamente.

### 3.1 Prueba chi-cuadrado de Pearson (uniformidad)

Divide el intervalo $[0, 1)$ en $k$ subintervalos iguales y cuenta los valores observados en cada celda:

$$O_i = \#\{r_n \in [i/k,\; (i+1)/k)\}, \quad i = 0, \ldots, k-1$$

Bajo $H_0 : r_n \sim U[0,1)$, el número esperado por celda es $E = N/k$. El estadístico:

$$\chi^2 = \sum_{i=0}^{k-1} \frac{(O_i - E)^2}{E} \xrightarrow{N \to \infty} \chi^2_{k-1}$$

sigue asintóticamente una distribución chi-cuadrado con $k-1$ grados de libertad. Se rechaza $H_0$ al nivel $\alpha = 0.05$ si $\chi^2 > \chi^2_{k-1;\, 0.95}$:

| $k$ | $\chi^2_{k-1;\, 0.95}$ |
|:---:|:----------------------:|
| 5   | 11.070                 |
| 10  | 16.919                 |
| 20  | 30.144                 |

**Implementación:** sin dependencias externas; valor crítico interpolado de tabla fija.

### 3.2 Prueba de rachas (independencia)

Evalúa la independencia serial de la secuencia. Una **racha** es una sucesión maximal de valores consecutivos todos por encima o todos por debajo de la media muestral $\bar{r}$.

Sea $n_1$ el número de valores $\geq \bar{r}$ y $n_2 = N - n_1$ los valores $< \bar{r}$. Bajo $H_0$ (independencia), el número de rachas $R$ sigue aproximadamente:

$$R \sim \mathcal{N}\!\left(\mu_R,\; \sigma_R^2\right)$$

con:

$$\mu_R = \frac{2n_1 n_2}{N} + 1, \qquad \sigma_R^2 = \frac{2n_1 n_2 (2n_1 n_2 - N)}{N^2(N-1)}$$

El estadístico de prueba es:

$$Z = \frac{R - \mu_R}{\sigma_R} \xrightarrow{d} \mathcal{N}(0, 1)$$

Se rechaza $H_0$ al nivel $\alpha = 0.05$ (bilateral) si $|Z| > 1.96$.

**Interpretación:** Demasiadas rachas ($Z \gg 0$) indica alternancia sistemática (correlación negativa); pocas rachas ($Z \ll 0$) indica agrupamiento (correlación positiva). Ambos casos implican dependencia serial.

### 3.3 Interpretación conjunta

| Prueba chi² | Prueba rachas | Diagnóstico |
|:-----------:|:-------------:|:------------|
| PASA | PASA | Generador adecuado para esta $N$ |
| FALLA | PASA | No uniforme — revisar módulo y multiplicador |
| PASA | FALLA | Dependencia serial — período corto o patrón estructural |
| FALLA | FALLA | Generador deficiente — descartar |

Las pruebas implementadas son **necesarias pero no suficientes**. La batería completa de Diehard (Marsaglia, 1995) y TestU01 (L'Ecuyer & Simard, 2007) comprenden decenas de pruebas adicionales.

---

## 4. Arquitectura del software

```
pseudoaleatorios/
│
├── src/pseudoaleatorios/
│   │
│   ├── domain/                       ← núcleo matemático puro (sin dependencias)
│   │   ├── models/
│   │   │   └── generator_config.py   ← GeneratorConfig, GeneratorResult (frozen dataclasses)
│   │   └── ports/
│   │       └── generator.py          ← PseudorandomGeneratorPort (ABC)
│   │
│   ├── application/
│   │   ├── factories/
│   │   │   └── generator_factory.py  ← GeneratorFactory (Factory Method: Enum → instancia)
│   │   └── use_cases/
│   │       └── generate_sequence.py  ← GenerateSequenceUseCase (generación + análisis)
│   │
│   └── infrastructure/
│       ├── config/settings.py        ← pydantic-settings: variables de entorno PRN_*
│       ├── generators/
│       │   ├── _digit_utils.py       ← middle_extract, detect_period, Criba de Eratóstenes
│       │   ├── middle_squares.py     ← Von Neumann (1946)
│       │   ├── constant_multiplier.py
│       │   ├── middle_products.py
│       │   ├── linear_congruential.py     ← Lehmer (1951), Hull-Dobell
│       │   ├── multiplicative_congruential.py
│       │   ├── additive_congruential.py   ← Lagged Fibonacci
│       │   └── quadratic_congruential.py
│       └── analysis/
│           └── statistics.py         ← chi-square, runs test, reporte estadístico
│
└── tests/
    ├── conftest.py                   ← fixtures: LCG clásico, MCG, semilla cuadrados medios
    ├── infrastructure/
    │   └── test_generators.py        ← rangos, errores esperados, pruebas estadísticas
    └── application/
        └── test_factory.py           ← todos los métodos registrados en la factory
```

**Invariante de dependencias:** `domain` no importa nada de `infrastructure`. Un nuevo generador (e.g., Mersenne Twister, xoshiro256\*\*, PCG) se agrega implementando `PseudorandomGeneratorPort` y añadiendo un caso en `GeneratorFactory`.

---

## 5. Instalación y uso

```bash
# Desde el directorio pseudoaleatorios/
pip install -e ".[dev]"

# Suite de tests (24 tests)
pytest

# GCL clásico de Numerical Recipes — 1000 valores
PRN_METHOD=linear_congruential \
PRN_SEED=1234 \
PRN_COUNT=1000 \
PRN_MULTIPLIER=1664525 \
PRN_INCREMENT=1013904223 \
PRN_MODULUS_EXPONENT=32 \
python -m pseudoaleatorios

# Cuadrados medios (Von Neumann)
PRN_METHOD=middle_squares PRN_SEED=6521 PRN_COUNT=200 python -m pseudoaleatorios

# Congruencial multiplicativo — a=5+8×3=29, m=2^31, semilla impar
PRN_METHOD=multiplicative_congruential \
PRN_SEED=1235 PRN_MULTIPLIER=29 PRN_MODULUS_EXPONENT=31 \
python -m pseudoaleatorios

# Fibonacci retrasado — vector de 5 semillas
PRN_METHOD=additive_congruential \
PRN_LAG_VECTOR="1009,2011,3001,4001,5003" \
PRN_MODULUS_EXPONENT=7 \
PRN_COUNT=500 \
python -m pseudoaleatorios

# Cuadrático — x_{n+1} = (3x² + 5x + 7) mod 2^16
PRN_METHOD=quadratic_congruential \
PRN_SEED=7 PRN_COEFF_A=3 PRN_COEFF_B=5 PRN_COEFF_C=7 \
PRN_MODULUS_EXPONENT=16 PRN_COUNT=1000 \
python -m pseudoaleatorios
```

---

## 6. Variables de entorno

Todas las variables usan el prefijo `PRN_` y son validadas por pydantic-settings en el arranque.

| Variable | Tipo | Descripción | Default |
|:---------|:----:|:------------|:-------:|
| `PRN_METHOD` | `str` | Algoritmo generador | `linear_congruential` |
| `PRN_SEED` | `int` | Semilla $x_0$ | `1234` |
| `PRN_COUNT` | `int` | Cantidad de valores a generar | `1000` |
| `PRN_MULTIPLIER` | `int` | Multiplicador $a$ (0 = auto-primo) | `0` |
| `PRN_INCREMENT` | `int` | Constante aditiva $c$ | `0` |
| `PRN_MODULUS_EXPONENT` | `int` | Exponente $g$ tal que $m = 2^g$ | `31` |
| `PRN_COEFF_A` | `int` | Coeficiente cuadrático $a$ | `3` |
| `PRN_COEFF_B` | `int` | Coeficiente lineal $b$ | `5` |
| `PRN_COEFF_C` | `int` | Término independiente $c$ | `7` |
| `PRN_LAG_VECTOR` | `str` | Vector semilla (CSV) | `1009,2011,3001,4001,5003` |
| `PRN_RUN_STATISTICS` | `bool` | Ejecutar pruebas estadísticas | `true` |
| `PRN_LOG_LEVEL` | `str` | `DEBUG` \| `INFO` \| `WARNING` | `INFO` |

**Métodos disponibles:** `middle_squares` · `constant_multiplier` · `middle_products` · `linear_congruential` · `multiplicative_congruential` · `additive_congruential` · `quadratic_congruential`

---

## 7. Referencias

- **Von Neumann, J.** (1951). Various techniques used in connection with random digits. *Applied Mathematics Series*, 12, 36–38. — Método de cuadrados medios.
- **Lehmer, D. H.** (1951). Mathematical methods in large-scale computing units. *Proceedings of the 2nd Symposium on Large-Scale Digital Computing Machinery*, 141–146. — GCL original.
- **Hull, T. E. & Dobell, A. R.** (1962). Random number generators. *SIAM Review*, 4(3), 230–254. — Teorema de período completo para GCL.
- **Knuth, D. E.** (1997). *The Art of Computer Programming, Vol. 2: Seminumerical Algorithms* (3rd ed.). Addison-Wesley. — Análisis exhaustivo de GCL/GCM, pruebas estadísticas, espectral.
- **L'Ecuyer, P.** (1999). Tables of linear congruential generators of different sizes and good lattice structure. *Mathematics of Computation*, 68(225), 249–260. — Parámetros óptimos verificados espectralmente.
- **Marsaglia, G.** (1995). *Diehard battery of tests of randomness*. Florida State University. — Batería de pruebas estándar de la industria.
- **L'Ecuyer, P. & Simard, R.** (2007). TestU01: A C library for empirical testing of random number generators. *ACM Transactions on Mathematical Software*, 33(4), 22. — Suite de pruebas moderna (BigCrush, SmallCrush).
- **Blum, L., Blum, M. & Shub, M.** (1986). A simple unpredictable pseudo-random number generator. *SIAM Journal on Computing*, 15(2), 364–383. — Generador cuadrático criptográfico (BBS).
- **Press, W. H., Teukolsky, S. A., Vetterling, W. T. & Flannery, B. P.** (2007). *Numerical Recipes: The Art of Scientific Computing* (3rd ed.). Cambridge University Press. — Parámetros GCL de referencia, prueba de rachas.
- **Panneton, F., L'Ecuyer, P. & Matsumoto, M.** (2006). Improved long-period generators based on linear recurrences modulo 2. *ACM Transactions on Mathematical Software*, 32(1), 1–16. — Contexto moderno: xorshift, WELL, Mersenne Twister.
