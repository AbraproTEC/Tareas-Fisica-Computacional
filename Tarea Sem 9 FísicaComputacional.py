#FÍSICA COMPUTACIONAL
#RESOLUCIÓN DE LA ECUACIÓN DE DIFUSIÓN
#TAREA SEMANA 9
#ESTUDIANTES: JOSÉ ABRAHAM ALFARO ALVARADO Y ANDRÉS CAMACHO
#FECHA: 27/04/2021

#IMPORTACIÓN DE PAQUETES NECESARIOS
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps

def DifusionInicialFourier(x, l):
    '''
    Se define la difusión inicial como condición inicial que existe cuando t = 0.0

    Parámetros de la función
    ------------------------
    x: posición a lo largo de la barra unidimensional
    l: constante que tiene presenta unidades lineales al cuadrado

    Salida de la función
    --------------------
    valorDifusion0: Valor de la difusión al inicial del tiempo
    '''
    valorDifusionInicial = A*np.exp(-(x - x0)**2/l)
    return valorDifusionInicial

def CalculoCoeficiente(m_termino, longitud_barra):
    '''
    Calcula los coeficientes b_m del teorema trigonométrico de Fourier

    Parámetros de la función
    ------------------------
    m_término: iterador que representa el término en el que se encuentra
    realizando el cálculo de la aproximación
    longitud_barra: longitud en la dimensión x en la que se integran los valores
    de los coeficientes. (Periodo espacial del teorema de Fourier)

    Salida de la función
    --------------------
    coeficiente_bm: Retorna el valor del coeficiente calculado en relación con el término
    de la suma
    '''
    coeficiente_bm = (2/longitud_barra)*simps(DifusionInicialFourier(x, l) * np.sin(x * np.pi * m_termino / longitud_barra), x)
    return coeficiente_bm

def AproxFourier(x, t, longitud_barra, nt):
    '''Calcula el valor aproximado de la difusión en el punto (x, t)

    Parámetros de la función
    ------------------------
    x : posición en el eje x (o posiciones si se suministra un arreglo)
    t : posición en el tiempo (o posiciones si se suministra un arreglo)
    longitud_barra : arista longitud de la barra unidimensional
    nt : número de términos que tendrá el cálculo de la difusión (debe ser
           mayor o igual que 1)

    Salida de la función
    --------------------
    valorAproxRhoXT : valor de la difusión en el punto (x, t)
    '''
    # Se inicializa el valor de la difusión a calcular
    valorAproxRhoXT = 0

    # Se realiza la sumatoria que corresponde con el número de términos dado
    for m_termino in range(1, nt + 1):
        valorAproxRhoXT += CalculoCoeficiente(m_termino, longitud_barra) * np.exp(-D * t * (m_termino * np.pi \
                                                                                            / longitud_barra) ** 2) * np.sin(m_termino*np.pi*x/longitud_barra)
    return valorAproxRhoXT

# Se define el valor de la longitud de la barra en la que se calculará la difusión
longitud_barra = 10.0

# Longitud del intervalo temporal finito
eje_tiempo = 20.0

#Se indica el número de términos para el cálculo de la aproximación del potencial eléctrico
numeroterminos1 = 50
numeroterminos2 = 3
D = 0.5
A = 2.0
x0 = 5.0
l = 1.5

# Se define la malla de puntos para evaluar el comportamiento de la difusión
puntos_malla = 40
x = np.linspace(0, longitud_barra, puntos_malla)
t = np.linspace(0, eje_tiempo, puntos_malla)
X, T = np.meshgrid(x, t)


# Se calcula el valor aproximado del comportamiento de la difusión en la
# barra unidimensional y en el tienpo.

Z1=AproxFourier(X, T, longitud_barra, numeroterminos1)
Z2=AproxFourier(X, T, longitud_barra, numeroterminos2)


#BLOQUES DE GRAFICACIÓN
fig = plt.figure(figsize=(10, 6))
fig.suptitle('Aproximación de la difusión en la barra unidimensional \
utilizando el método de Fourier', color = 'green')
ax1 = fig.add_subplot(122, projection='3d')
ax1.set_xlabel('x (m)', color = 'r')
ax1.set_ylabel('t (s)', color = 'r')
ax1.set_zlabel('Difusión', color = 'r')
ax1.plot_surface(X, T, Z1, rstride=1, cstride=1, cmap='YlGnBu_r', edgecolor='black')
ax1.set_title('Con n =' +' '+ str(numeroterminos1), color = 'blue')

ax2 = fig.add_subplot(121, projection='3d')
ax2.set_xlabel('x (m)', color = 'r')
ax2.set_ylabel('t (s)', color = 'r')
ax2.set_zlabel('Difusión', color = 'r')
ax2.plot_surface(X, T, Z2, rstride=1, cstride=1, cmap='YlGnBu_r', edgecolor='black')
ax2.set_title('Con n =' +' '+ str(numeroterminos2), color = 'blue')
fig.tight_layout()
plt.show()

#Se genera el codigo para comparar la presición entre series de fourier de diferente cantidad de términos

#Se define la cantidad de términos que se quieren para la serie de fourier con más términos
terminos=15

#Se inicializan los arreglos correspondientes a los ejes del gráfico de análisis cuantitativo
diferencias_entre_mallas=np.zeros(terminos-1)
eje_terminos=np.zeros(terminos-1)

#Se crea el bucle que añadirá los elementos a los arreglos
for numero_terminos in range (2,terminos+1):

    #Se genera el arreglo del eje horizonatal
    eje_terminos[numero_terminos-2]  =numero_terminos

    #se calculan las mallas con diferente número de términos
    Z_anterior = AproxFourier(X, T, longitud_barra, numero_terminos - 1)
    Z_actual = AproxFourier(X, T, longitud_barra, numero_terminos)

    #Se reinicia la sumatoria
    sumatoria_diferencias = 0

    #Se crea el bucle que recorre las mallas
    for i in range (puntos_malla):
        for j in range (puntos_malla):

            #Se hace la diferencia en valor absoluto entre mallas en el punto i,j y se añade a la suma
            sumatoria_diferencias += np.abs(Z_actual[i][j]-Z_anterior[i][j])

    #Se añade la sumatoria de las diferencias al arreglo para el eje de suma de diferencias
    diferencias_entre_mallas[numero_terminos-2] = sumatoria_diferencias


#Se grafican los resultados

fig1 = plt.figure()
plt.plot(eje_terminos,diferencias_entre_mallas)
plt.title('Análisis cuantitativo del método')
plt.xlabel("Términos en la serie de fourier")
plt.ylabel("Suma de las diferencias entre mallas")
plt.show()


def DifusionInicialDiferenciasFinitas(x):

    '''Calcula el valor inicial de la matriz (x, t)

    Parámetros de la función
    ------------------------
    x : puntos del eje x donde se evaluan las condiciones iniciales

    Salida de la función
    --------------------
    rho_xt_inicial : matriz inicial (x, t) .
    '''

    # Se crea la matriz de ceros en la malla x,t
    rho_xt_inicial = np.zeros((puntost, puntosx), float)

    # Se recorre la primera columna asignando los valores de condicion inicial
    for i in range(1, puntosx - 1):
        rho_xt_inicial[0][i] = A * np.exp((-(x[i] - x0) ** 2) / l)
    return rho_xt_inicial

def AproxDiferenciasFinitas(niter):

    '''Calcula el valor aproximado de la difusión en el punto (x, t)

    Parámetros de la función
    ------------------------
    niter : número de iteraciones que se desean

    Salida de la función
    --------------------
    rho_xt : valor de la difusión en el punto (x, t) a niter iteraciones.
    '''

    #Se define la constante a utilizar
    constante = (D*Dt)/(Dx*Dx)

    #Se iguala la matriz a tratar a la matriz de valores iniciales
    #Esto se hace aquí para que se reinicie la matriz de valores iniciales
    rho_xt = DifusionInicialDiferenciasFinitas(x)

    #Se crea el bucle de iteraciones
    for iteracion in range (1, niter+1):

        #Se crea la condición para que se calcule la primera malla solo a partir de la primera columna
        if iteracion == 1:

            for it in range(0, puntost-1):
                for ix in range(1, puntosx-1):

                    rho_xt[it+1][ix] = rho_xt[it][ix] + constante*(rho_xt[it][ix+1] + rho_xt[it][ix-1] - 2*rho_xt[it][ix])

        #Se calculan las siguientes mallas a partir de las mallas anteriores y no solo de la primera columna
        else:

            for it in range(0, puntost - 1):
                for ix in range(1, puntosx - 1):

                    rho_xt[it][ix]=(1/(1-2*constante))*(rho_xt[it+1][ix]-constante*(rho_xt[it][ix+1]+rho_xt[it][ix-1]))

    return rho_xt


# Se define el valor de la longitud de la barra en la que se calculará la difusión
longitudbarra= 10
# Longitud del intervalo temporal finito
eje_tiempo = 3
# Se indica el número de términos para el cálculo de la aproximación del potencial eléctrico
D = 0.5
A = 2.0
x0 = 5.0
l = 1.5
# Se define la malla de puntos para evaluar el comportamiento de la difusión
puntost = 600
puntosx = 120
Dt = eje_tiempo / puntost
Dx = longitudbarra / puntosx

x = np.linspace(0, longitudbarra, puntosx)
t = np.linspace(0, eje_tiempo, puntost)
X, T = np.meshgrid(x, t)

#SE CALCULA EL VALOR APROXIMADO DEL COMPORTAMIENTO DE LA DIFUSIÓN
# EN LA BARRA UNIDIMENSIONAL
niter1 =0
R1 = AproxDiferenciasFinitas(niter1)

niter2 = 1
R2 = AproxDiferenciasFinitas(niter2)

#BLOQUE DE GRAFICACIÓN'''

fig = plt.figure(figsize=(10, 6))
fig.suptitle('Aproximación de la difusión en la barra unidimensional utilizando el método de Gauss-Seidel', color = 'green')

ax1 = fig.add_subplot(121, projection = '3d')
ax1.set_xlabel('x(m)', color = 'r')
ax1.set_ylabel('t(s)', color = 'r')
ax1.set_zlabel('Difusión', color = 'r')
ax1.plot_surface(X, T, R1, rstride=1, cstride=1, cmap='YlGnBu_r', edgecolor='black')
ax1.set_title('Con'+' '+str(niter1)+' iteraciones', color = 'blue')


ax2 = fig.add_subplot(122, projection = '3d')
ax2.set_xlabel('x(m)', color = 'r')
ax2.set_ylabel('t(s)', color = 'r')
ax2.set_zlabel('Difusión', color = 'r')
ax2.plot_surface(X, T, R2, rstride=1, cstride=1, cmap='YlGnBu_r', edgecolor='black')
ax2.set_title('Con'+' '+str(niter2 )+' iteraciones', color = 'blue')

plt.show()

#Se genera el codigo para comparar la presición entre series de fourier de diferente cantidad de términos

#Se define la cantidad de términos que se quieren para la serie de fourier con más términos
iteraciones=4

#Se inicializan los arreglos correspondientes a los ejes del gráfico de análisis cuantitativo
diferencias_entre_mallas=np.zeros(iteraciones)
eje_iteraciones=np.zeros(iteraciones)

#Se crea el bucle que añadirá los elementos a los arreglos
for iteracion in range (1, iteraciones + 1):

    #Se genera el arreglo del eje horizonatal de iteraciones
    eje_iteraciones[iteracion - 1] = iteracion

    #se calculan las mallas con diferente número de iteraciones
    R_anterior = AproxDiferenciasFinitas(iteracion - 1)
    R_actual = AproxDiferenciasFinitas(iteracion)

    #Se reinicia la sumatoria
    sumatoria_diferencias = 0

    #Se crea el bucle que recorre las mallas
    for i in range (puntost):
        for j in range (puntosx):

            #Se hace la diferencia en valor absoluto entre mallas en el punto i,j y se añade a la suma
            sumatoria_diferencias += np.abs(R_actual[i][j] - R_anterior[i][j])

    #Se añade la sumatoria de las diferencias al arreglo para el eje de suma de diferencias
    diferencias_entre_mallas[iteracion - 1] = sumatoria_diferencias


#Se grafican los resultados

fig1 = plt.figure()
plt.plot(eje_iteraciones, diferencias_entre_mallas)
plt.title('Análisis cuantitativo del método')
plt.xlabel("Número de iteraciones")
plt.ylabel("Suma de las diferencias entre mallas")
plt.show()

