# Métodos Numéricos Computacionales

**Implementación de referencia en Python 3.12 — arquitectura hexagonal, tipado estático**

Colección de métodos numéricos clásicos para la resolución de integrales definidas, ecuaciones diferenciales ordinarias (EDOs) y ecuaciones en derivadas parciales (EDPs). El proyecto sirve como material de estudio para cursos de posgrado en modelamiento matemático, análisis numérico y simulación computacional. Cada algoritmo se implementa como un objeto con tipado estático completo, lo que permite inspeccionar contratos, pre/postcondiciones y flujo de datos con precisión.

---

## Contenido

1. [Métodos de cuadratura numérica](#1-métodos-de-cuadratura-numérica)
2. [Integradores de EDOs](#2-integradores-de-edos)
3. [Métodos de diferencias finitas para EDPs](#3-métodos-de-diferencias-finitas-para-edps)
4. [Catálogo de problemas](#4-catálogo-de-problemas)
5. [Arquitectura del software](#5-arquitectura-del-software)
6. [Instalación y ejecución](#6-instalación-y-ejecución)
7. [Docker y variables de entorno](#7-docker-y-variables-de-entorno)
8. [Referencias](#8-referencias)

---

## 1. Métodos de cuadratura numérica

Se busca aproximar la integral de Riemann

$$I = \int_a^b f(x)\,dx$$

mediante fórmulas de cuadratura compuestas de la forma $\hat{I}_n = \sum_{i} w_i f(x_i)$.

### 1.1 Regla de Simpson 1/3 compuesta

La fórmula de Newton-Cotes de orden 2 aproxima $f$ por polinomios cuadráticos en cada subintervalo $[x_i,\, x_{i+1}]$ de longitud $h = (b-a)/(n-1)$:

$$\hat{I}_n = \frac{h}{6}\sum_{i=0}^{n-2}\left[f(x_i) + 4f\!\left(x_i + \tfrac{h}{2}\right) + f(x_{i+1})\right]$$

**Error global:** Si $f \in C^4[a,b]$, el error compuesto satisface

$$|I - \hat{I}_n| \leq \frac{(b-a)^5}{180\,n^4}\,\max_{\xi\in[a,b]}|f^{(4)}(\xi)| = O(h^4)$$

La convergencia es de **cuarto orden** en $h$, lo que la convierte en el método de cuadratura estándar para funciones suficientemente regulares.

### 1.2 Regla del Trapecio compuesta

$$\hat{I}_n = \frac{h}{2}\sum_{i=0}^{n-2}\left[f(x_i) + f(x_{i+1})\right]$$

**Error global:** $O(h^2)$, con constante proporcional a $\max|f''|$. Para funciones $f$ con singularidades de primer tipo en los extremos (como $f \in C^\infty$ periódica), la regla del trapecio puede exhibir convergencia superalgebraica (efecto Euler-Maclaurin).

### 1.3 Regla del punto medio compuesta

$$\hat{I}_n = h\sum_{i=1}^{n-2} f\!\left(x_i\right), \quad x_i = a + i\,h$$

**Error global:** $O(h^2)$, con constante la mitad de la del trapecio para la misma $f''$. Útil cuando $f$ presenta singularidades en los extremos del intervalo (e.g., $\sin(x^2)/x$ cerca de $x=0$).

---

## 2. Integradores de EDOs

Se considera el problema de valor inicial (PVI) en forma vectorial:

$$\frac{d\mathbf{y}}{dt} = \mathbf{f}(t, \mathbf{y}), \quad \mathbf{y}(t_0) = \mathbf{y}_0, \quad \mathbf{y} \in \mathbb{R}^n$$

con paso uniforme $h = (t_f - t_0)/(N-1)$ y $t_k = t_0 + k\,h$.

### 2.1 Runge-Kutta de orden 4 (RK4)

El método más utilizado en simulación científica. En cada paso se evalúan cuatro pendientes intermedias:

$$k_1 = h\,\mathbf{f}(t_k,\, \mathbf{y}_k)$$
$$k_2 = h\,\mathbf{f}\!\left(t_k + \tfrac{h}{2},\, \mathbf{y}_k + \tfrac{k_1}{2}\right)$$
$$k_3 = h\,\mathbf{f}\!\left(t_k + \tfrac{h}{2},\, \mathbf{y}_k + \tfrac{k_2}{2}\right)$$
$$k_4 = h\,\mathbf{f}(t_k + h,\, \mathbf{y}_k + k_3)$$
$$\mathbf{y}_{k+1} = \mathbf{y}_k + \tfrac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

**Tabla de Butcher:**

$$\begin{array}{c|cccc}
0 & & & & \\
1/2 & 1/2 & & & \\
1/2 & 0 & 1/2 & & \\
1 & 0 & 0 & 1 & \\
\hline
& 1/6 & 2/6 & 2/6 & 1/6
\end{array}$$

**Error de truncamiento local:** $O(h^5)$. **Error global:** $O(h^4)$. La región de estabilidad absoluta contiene el semiplano izquierdo complejo hasta aproximadamente $h\lambda \in [-2.79,\, 0]$ para $\lambda \in \mathbb{R}^-$.

**Número de evaluaciones de $\mathbf{f}$:** 4 por paso.

### 2.2 Método de Heun (RK2 — Trapecio explícito)

Corrector-predictor de dos etapas:

$$\tilde{\mathbf{y}}_{k+1} = \mathbf{y}_k + h\,\mathbf{f}(t_k, \mathbf{y}_k) \quad \text{(predictor Euler)}$$
$$\mathbf{y}_{k+1} = \mathbf{y}_k + \frac{h}{2}\left[\mathbf{f}(t_k, \mathbf{y}_k) + \mathbf{f}(t_{k+1}, \tilde{\mathbf{y}}_{k+1})\right]$$

**Error global:** $O(h^2)$. Número de evaluaciones: 2 por paso. Apropiado para sistemas con dinámica moderada donde el costo por evaluación de $\mathbf{f}$ es elevado y la precisión de segundo orden es suficiente.

### 2.3 Método del punto medio explícito (RK2 — Euler modificado)

$$\mathbf{y}_{k+1/2} = \mathbf{y}_k + \frac{h}{2}\,\mathbf{f}(t_k, \mathbf{y}_k)$$
$$\mathbf{y}_{k+1} = \mathbf{y}_k + h\,\mathbf{f}\!\left(t_k + \tfrac{h}{2},\, \mathbf{y}_{k+1/2}\right)$$

**Error global:** $O(h^2)$, con coeficiente de error ligeramente distinto al de Heun. La constante de error es $\tfrac{1}{6}\|\mathbf{f}_{tt} + \mathbf{f}_{ty}\mathbf{f}\|$. Ambos métodos (Heun y Punto Medio) pertenecen a la misma clase de consistencia de orden 2 pero difieren en sus regiones de estabilidad.

### 2.4 Integrador Störmer-Verlet

Diseñado para sistemas Hamiltonianos de la forma $H(q, p) = T(p) + V(q)$, escritos como

$$\dot{q} = \frac{\partial H}{\partial p} = v, \qquad \dot{v} = -\frac{\partial H}{\partial q} = a(q)$$

El esquema de Verlet de posición es:

$$q_{k+1} = 2q_k - q_{k-1} + h^2\,a(q_k)$$

con velocidad recuperada por diferencia central:

$$v_k = \frac{q_{k+1} - q_{k-1}}{2h} + O(h^2)$$

**Propiedades geométricas clave:**
- **Simplecticidad:** Preserva el área en el espacio de fases $dq \wedge dp = \text{const}$, lo que implica conservación exacta (no aproximada) de una energía modificada $\tilde{H} = H + O(h^2)$.
- **Reversibilidad temporal:** El mapa $\Phi_h$ satisface $\Phi_{-h} \circ \Phi_h = \text{Id}$, propiedad que Runge-Kutta estándar no posee.
- **Error global:** $O(h^2)$ para posición y velocidad, pero el error en energía se mantiene acotado $O(h^2)$ para todos los tiempos (sin deriva secular), a diferencia de métodos no simpléticos.

**Nota de implementación:** El primer paso requiere un bootstrapping (Euler) para obtener $q_1$ a partir de $q_0$ y $v_0$, ya que el método es de tres niveles.

---

## 3. Métodos de diferencias finitas para EDPs

### 3.1 Ecuación de difusión (calor) — Esquema FTCS

La ecuación de difusión 1D:

$$\frac{\partial u}{\partial t} = D\,\frac{\partial^2 u}{\partial x^2}, \quad x \in [0, L],\; t \in [0, T]$$

se discretiza mediante la aproximación *Forward Time, Centered Space* (FTCS):

$$\frac{u_m^{n+1} - u_m^n}{\Delta t} = D\,\frac{u_{m+1}^n - 2u_m^n + u_{m-1}^n}{\Delta x^2}$$

que resulta en el esquema explícito:

$$u_m^{n+1} = u_m^n + r\left(u_{m+1}^n - 2u_m^n + u_{m-1}^n\right), \qquad r = \frac{D\,\Delta t}{\Delta x^2}$$

**Análisis de estabilidad de Von Neumann:** Sustituyendo el modo de Fourier $u_m^n = \xi^n e^{im\theta}$ se obtiene el factor de amplificación

$$\xi(\theta) = 1 - 4r\sin^2\!\left(\frac{\theta}{2}\right)$$

Para estabilidad ($|\xi| \leq 1$ para todo $\theta$) se requiere:

$$r = \frac{D\,\Delta t}{\Delta x^2} \leq \frac{1}{2}$$

Esta condición limita severamente $\Delta t$ cuando $\Delta x$ es pequeño. El esquema es **consistente** ($O(\Delta t) + O(\Delta x^2)$) y **convergente** cuando es estable (Lax-equivalencia).

**Orden global:** $O(\Delta t + \Delta x^2)$. Para obtener $O(\Delta x^2)$ en tiempo se requiere $\Delta t \sim \Delta x^2$, llevando a $O(\Delta x^2)$ global con el esquema de Crank-Nicolson (no implementado aquí).

### 3.2 Ecuación de onda — Diferencias finitas de tres niveles

La ecuación de onda 1D:

$$\frac{\partial^2 u}{\partial t^2} = c^2\,\frac{\partial^2 u}{\partial x^2}$$

se discretiza con diferencias centradas en ambas dimensiones:

$$\frac{u_m^{n+1} - 2u_m^n + u_m^{n-1}}{\Delta t^2} = c^2\,\frac{u_{m+1}^n - 2u_m^n + u_{m-1}^n}{\Delta x^2}$$

que produce el esquema explícito:

$$u_m^{n+1} = 2u_m^n - u_m^{n-1} + \nu^2\left(u_{m+1}^n - 2u_m^n + u_{m-1}^n\right)$$

donde $\nu = c\,\Delta t / \Delta x$ es el **número de Courant-Friedrichs-Lewy (CFL)**.

**Condición de estabilidad CFL:**

$$\nu = \frac{c\,\Delta t}{\Delta x} \leq 1$$

El análisis de Von Neumann da $|\xi|^2 = 1$ cuando $\nu \leq 1$ (esquema no disipativo exacto en modos puramente oscilatorios), y $|\xi| > 1$ cuando $\nu > 1$ (inestabilidad exponencial).

**Orden global:** $O(\Delta t^2 + \Delta x^2)$.

---

## 4. Catálogo de problemas

### Integrales definidas

| ID | Integral | Método implementado | Valor exacto |
|:--:|:---------|:-------------------:|:------------:|
| 1 | $\displaystyle\int_0^{40} e^{-x/3}\cos(x)\,dx$ | Simpson 1/3 | — |
| 2 | $\displaystyle\int_{-1}^{1} \sqrt{1-x^2}\,dx$ | Trapecio | $\pi/2$ |
| 3 | $\displaystyle\int_0^{100} \frac{\sin(x^2)}{x}\,dx$ (tipo Fresnel) | Punto medio | — |
| 4 | $\displaystyle\int_0^{\pi} \sin(x)\,dx$ | Simpson 1/3 | $2$ |
| 5 | $\displaystyle\int_{-\pi/2}^{\pi/2} \ln(\cos x)\,dx$ | Simpson 1/3 | $-\pi\ln 2$ |

### Ecuaciones diferenciales ordinarias

#### Problema 1 — Modelo de Lotka-Volterra (RK4)

Sistema depredador-presa con dinámica Hamiltoniana:

$$\frac{dx}{dt} = \alpha x - \beta xy, \qquad \frac{dy}{dt} = \delta xy - \gamma y$$

con $\alpha=3$, $\beta=\gamma=1$, $\delta=1$; $x(0)=1$, $y(0)=2$; $t \in [0, 20]$.

El sistema posee el invariante de primera integral:

$$H(x,y) = \delta x - \gamma \ln x + \beta y - \alpha \ln y = \text{const}$$

Las órbitas en el espacio de fases son curvas cerradas (ciclos límite). RK4 no es simpléctic y exhibe deriva secular en $H$; Verlet preservaría $H$ sin deriva.

#### Problema 2 — Modelo SIR epidemiológico (Heun)

Sistema de Kermack-McKendrick (1927):

$$\frac{dS}{dt} = -\beta SI, \quad \frac{dI}{dt} = \beta SI - \gamma I, \quad \frac{dR}{dt} = \gamma I$$

con $\beta = 1.407 \times 10^{-3}$, $\gamma = 0.6$; $S(0)=995$, $I(0)=5$, $R(0)=0$; $t \in [0, 24]$.

El número reproductivo básico $\mathcal{R}_0 = \beta S_0/\gamma \approx 2.34 > 1$ garantiza un brote epidémico. La conservación $S+I+R = N = \text{const}$ reduce el sistema a 2 grados de libertad efectivos. El umbral de inmunidad de rebaño es $S^* = \gamma/\beta$.

#### Problema 3 — Atractor de Lorenz (Punto Medio)

Sistema tridimensional de Lorenz (1963):

$$\frac{dx}{dt} = \sigma(y - x), \quad \frac{dy}{dt} = x(\rho - z) - y, \quad \frac{dz}{dt} = xy - \tfrac{8}{3}z$$

con $\sigma=10$, $\rho=27$, $\beta=8/3$; condiciones iniciales $(1, 0, 0)$; $t \in [0, 50]$.

Los parámetros corresponden al régimen caótico ($\rho > \rho_c \approx 24.74$). El sistema exhibe un **atractor extraño** con dimensión fractal de Hausdorff $d_H \approx 2.06$ y exponentes de Lyapunov $\lambda_1 \approx 0.906$, $\lambda_2 = 0$, $\lambda_3 \approx -14.57$, con suma $\lambda_1+\lambda_2+\lambda_3 = -(\sigma+1+8/3) < 0$ (disipatividad). La sensibilidad a condiciones iniciales implica que el error numérico crece como $e^{\lambda_1 t}$; toda solución es **cualitativamente correcta** sólo en tiempos cortos.

#### Problema 4 — Oscilador de Van der Pol forzado (RK4)

EDO de segundo orden no autónoma:

$$\ddot{x} - \mu(1 - x^2)\dot{x} + x = A\sin(\omega t)$$

con $\mu = 8.53$, $A = 1.2$, $\omega = 2\pi/10$; $x(0)=0.5$, $\dot{x}(0)=0$; $t \in [0, 100]$.

Reducción al sistema de primer orden con $y = \dot{x}$:

$$\dot{x} = y, \qquad \dot{y} = A\sin(\omega t) - x + \mu(1-x^2)y$$

Para $\mu \gg 1$ el sistema es de **tipo stiff**: las escalas de tiempo rápidas $(\sim 1/\mu)$ y lentas $(\sim 1)$ coexisten. RK4 requiere paso $h \lesssim 2.79/(\mu |\lambda_\text{max}|)$ para estabilidad, imponiéndose la escala rápida. El sistema puede exhibir **resonancia no lineal** y ciclos límite en función de $A/\omega$.

#### Problema 5 — Ecuación de Jerk (Punto Medio)

Sistema de tercer orden autónomo caótico (Sprott, 1997):

$$\dddot{x} + A\ddot{x} - x\dot{x}^2 + x^3 = 0, \qquad A = 3.6$$

Reducción con $y = \dot{x}$, $z = \ddot{x}$:

$$\dot{x} = y, \quad \dot{y} = z, \quad \dot{z} = xy^2 - x^3 - Az$$

La palabra "jerk" denomina la derivada tercera de la posición. Con $A = 3.6$ el sistema exhibe un atractor caótico de dimensión fractal baja y estructura topológica más simple que Lorenz. El sistema requiere $N = 10^6$ pasos para $t \in [0, 200]$; la discretización de punto medio introduce disipación numérica artificial proporcional a $h^2$, afectando levemente la estructura del atractor.

#### Problema 6 — Modelo SIRD (Heun)

Extensión del SIR con compartimento de fallecidos:

$$\frac{dS}{dt} = -\frac{\beta SI}{N}, \quad \frac{dI}{dt} = \frac{\beta SI}{N} - (\gamma+\mu)I, \quad \frac{dR}{dt} = \gamma I, \quad \frac{dD}{dt} = \mu I$$

con $\beta=0.4$, $\gamma=0.035$, $\mu=0.005$, $N(t)=S(t)+I(t)$ (población variable); $S(0)=997$, $I(0)=3$; $t \in [0, 100]$.

La tasa de letalidad de caso (CFR) asintótica es $\mu/(\gamma+\mu) \approx 12.5\%$. $N(t)$ decrece a medida que $D(t)$ crece, haciendo el sistema no conservativo; la incidencia normalizada $\beta SI/N$ satura naturalmente para poblaciones grandes.

#### Problema 7 — Péndulo simple (Verlet)

Ecuación del movimiento para ángulo $\theta$:

**Sin fricción:**
$$\ddot{\theta} = -\frac{g}{L}\sin\theta, \qquad g=9.81\,\text{m/s}^2,\; L=2\,\text{m}$$

**Con fricción viscosa:**
$$\ddot{\theta} = -\frac{g}{L}\sin\theta - \frac{k}{m}\dot{\theta}, \qquad k=0.9,\; m=4\,\text{kg}$$

La linealización $\sin\theta \approx \theta$ produce el oscilador simple con período $T_0 = 2\pi\sqrt{L/g} \approx 2.84\,\text{s}$. Para ángulos grandes, el período exacto se expresa mediante la integral elíptica completa de primera especie:

$$T = 4\sqrt{\frac{L}{g}}\,K\!\left(\sin\frac{\theta_0}{2}\right)$$

El integrador de Verlet es **obligatorio** para el sistema sin fricción: preserva el área en el espacio de fases $(\theta, \dot\theta)$ y mantiene la amplitud constante. Un método Euler explícito produciría crecimiento exponencial de la energía; uno Euler implícito, decaimiento espurio. Con fricción se usa velocity-Verlet (equivalente).

---

### Ecuaciones en derivadas parciales

| ID | Ecuación | Esquema | Condiciones |
|:--:|:---------|:-------:|:------------|
| 1 | Difusión calor $u_t = D u_{xx}$ | FTCS ($r=0.05$) | Dirichlet $u(0)=u(L)=0$ |
| 2 | Difusión calor en barra | FTCS ($r=0.01$) | Neumann libre en $x=0$ |
| 3 | Onda $u_{tt} = c^2 u_{xx}$ | 3 niveles | Dirichlet ambos extremos |
| 4 | Onda extremo libre | 3 niveles | Dirichlet-Neumann |
| 5 | Onda oscilante | 3 niveles | Dirichlet ambos extremos |

---

## 5. Arquitectura del software

El proyecto adopta **arquitectura hexagonal** (Ports & Adapters, Cockburn 2005), separando la lógica matemática de los detalles de infraestructura:

```
src/metodos_numericos/
│
├── domain/                     ← núcleo matemático puro
│   ├── models/                 ← tipos de datos: IntegralProblem, ODEProblem, PDEProblem,
│   │                              IntegralResult, ODEResult, PDEResult (dataclasses inmutables)
│   └── ports/                  ← interfaces abstractas (ABC):
│                                  IntegralSolverPort, ODESolverPort, PDESolverPort,
│                                  VisualizerPort
│
├── application/
│   ├── factories/
│   │   └── solver_factory.py   ← Factory Method: mapea (Enum → instancia de solver)
│   └── use_cases/              ← orquestación: SolveIntegralUseCase, SolveODEUseCase,
│                                  SolvePDEUseCase (inyección de dependencias)
│
└── infrastructure/             ← implementaciones concretas (reemplazables)
    ├── config/settings.py      ← pydantic-settings: variables de entorno con validación
    ├── problems/               ← registro de los 17 problemas del proyecto
    ├── solvers/                ← SimpsonSolver, TrapezoidalSolver, MidpointRectSolver,
    │                              RungeKutta4Solver, HeunSolver, MidpointSolver,
    │                              VerletSolver, ExplicitEulerHeatSolver, WaveEquationSolver
    └── visualizers/            ← MatplotlibVisualizer (backend Agg para entornos headless)
```

**Invariante de dependencias:** las capas de dominio y aplicación no importan nada de infraestructura. Un nuevo solver (e.g., Adams-Bashforth, Runge-Kutta-Fehlberg) se agrega implementando el puerto correspondiente y registrándolo en `SolverFactory`, sin modificar ninguna otra clase.

---

## 6. Instalación y ejecución

**Requisitos:** Python ≥ 3.12, pip.

```bash
# Clonar e instalar (modo editable con dependencias de desarrollo)
git clone https://github.com/NicolasImplant/metodos_numericos_Python.git
cd metodos_numericos_Python
pip install -e ".[dev]"

# Ejecutar la suite de tests (24 tests)
pytest

# Resolver Lotka-Volterra con RK4 (configuración por defecto en .env)
python -m metodos_numericos

# Integral ∫₀^π sin(x) dx con Simpson — resultado exacto: 2
NM_PROBLEM_TYPE=integral NM_PROBLEM_ID=4 NM_NUM_STEPS=200 python -m metodos_numericos

# Atractor de Lorenz con Método del Punto Medio
NM_PROBLEM_TYPE=ode NM_PROBLEM_ID=3 NM_ODE_METHOD=midpoint NM_NUM_STEPS=50000 python -m metodos_numericos

# Ecuación de difusión de calor
NM_PROBLEM_TYPE=pde NM_PROBLEM_ID=1 NM_PDE_METHOD=explicit_euler_heat python -m metodos_numericos

# Visualización interactiva (requiere entorno con display)
NM_VISUALIZATION_BACKEND=display python -m metodos_numericos
```

Las gráficas se guardan en `./output/` como `{tipo}_p{id}.png`.

---

## 7. Docker y variables de entorno

Todas las variables usan el prefijo `NM_` y son validadas por pydantic-settings en tiempo de arranque.

| Variable | Tipo | Valores | Default |
|:---------|:----:|:--------|:-------:|
| `NM_PROBLEM_TYPE` | `str` | `integral` \| `ode` \| `pde` | `ode` |
| `NM_PROBLEM_ID` | `int` | 1–5 (integral), 1–7 (ode), 1–5 (pde) | `1` |
| `NM_INTEGRAL_METHOD` | `str` | `simpson` \| `trapezoidal` \| `midpoint_rect` | `simpson` |
| `NM_ODE_METHOD` | `str` | `runge_kutta4` \| `heun` \| `midpoint` \| `verlet` | `runge_kutta4` |
| `NM_PDE_METHOD` | `str` | `explicit_euler_heat` \| `wave_equation` | `explicit_euler_heat` |
| `NM_NUM_STEPS` | `int` | ≥ 2 | `10000` |
| `NM_VISUALIZATION_BACKEND` | `str` | `file` \| `display` | `file` |
| `NM_OUTPUT_DIR` | `path` | cualquier ruta | `output` |
| `NM_FIGURE_DPI` | `int` | 72–600 | `150` |
| `NM_LOG_LEVEL` | `str` | `DEBUG` \| `INFO` \| `WARNING` | `INFO` |

```bash
# Construir imagen (multi-stage: app + test)
docker compose build

# Resolver Atractor de Lorenz → output/ode_p3.png
docker compose up lorenz

# Integral con Simpson → output/integral_p4.png
docker compose up integral-simpson

# Ecuación de calor → output/pde_p1.png
docker compose up heat-pde

# Suite de tests dentro del contenedor
docker compose up tests

# Problema arbitrario en tiempo de ejecución
docker compose run solver \
  -e NM_PROBLEM_TYPE=ode \
  -e NM_PROBLEM_ID=6 \
  -e NM_ODE_METHOD=heun \
  -e NM_NUM_STEPS=5000
```

Los archivos PNG se montan en `./output/` mediante un volumen Docker.

---

## 8. Referencias

- **Burden, R. L. & Faires, J. D.** (2010). *Numerical Analysis* (9th ed.). Brooks/Cole. — Fundamento de cuadratura y RK.
- **Hairer, E., Nørsett, S. P. & Wanner, G.** (1993). *Solving Ordinary Differential Equations I: Nonstiff Problems* (2nd ed.). Springer. — Teoría de métodos Runge-Kutta, tablas de Butcher.
- **Hairer, E., Lubich, C. & Wanner, G.** (2006). *Geometric Numerical Integration* (2nd ed.). Springer. — Integradores simpléticos, análisis backward error, Verlet.
- **Lorenz, E. N.** (1963). Deterministic nonperiodic flow. *Journal of the Atmospheric Sciences*, 20(2), 130–141.
- **Kermack, W. O. & McKendrick, A. G.** (1927). A contribution to the mathematical theory of epidemics. *Proceedings of the Royal Society A*, 115(772), 700–721.
- **Sprott, J. C.** (1997). Some simple chaotic jerk functions. *American Journal of Physics*, 65(6), 537–543.
- **LeVeque, R. J.** (2007). *Finite Difference Methods for Ordinary and Partial Differential Equations*. SIAM. — Análisis de Von Neumann, CFL, FTCS.
- **Cockburn, A.** (2005). *Hexagonal Architecture*. — Patrón de arquitectura de software.
- **Strogatz, S. H.** (2015). *Nonlinear Dynamics and Chaos* (2nd ed.). Westview Press. — Sistemas Hamiltonianos, bifurcaciones, atractores.
