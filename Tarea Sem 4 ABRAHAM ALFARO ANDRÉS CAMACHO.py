import scipy.integrate as spy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pds

def F(y,p):
    ''' Se define la función del lado derecho de la ecuacion diferencial
     que depende de la altura (y) y de la presión (p)

    Parámetros:

    y: representa la variable independiente (altura)
    p: representa la variable dependiente (presión)

    Salida de la función:

    Devuelve el lado derecho de la ecuacion diferencial a resolver '''

    dp_dy = -(M*g*p)/(R*(293.0-(y/200.0)))
    return dp_dy

# Se inicializan las constantes a utilizar

M = 0.0289647 # Note que hay que convertir la constante dada para que
              # concuerden las unidades.
R = 8.314462
g = 9.8

# Se definen los parámetros que se especifican en el problema

altura_inicial = 0.0
altura_final = 3000.0
p0 = 101325.0

# Se realiza la creación del arreglo de alturas

cantidad_de_intervalos = int((altura_final-altura_inicial)/100)
y = np.linspace(altura_inicial, altura_final, cantidad_de_intervalos+1)


def RK4(funcion, presion_inicial, y):
    ''' Se define la función que realizará el método Runge-Kutta

    Parámetros:

    funcion: representa la funcion del lado derecho de la ecuación
    diferencial a resolver

    presion_inicial: reporesenta el valor inicial de la presion
    y: representa el arreglo de alturas creado anteriormente

    Salida de la función:

    Devuelve el arreglo de presiones aproximadas mediante el método
    Runge-Kutta 4'''

    h = 100.0
    p = np.zeros(len(y))
    p[0]= presion_inicial
    for i in range (len(y)-1):
        K1 = h * funcion(y[i], p[i])
        K2 = h * funcion(y[i] + h/2, p[i] + K1 / 2)
        K3 = h * funcion(y[i] + h / 2, p[i] + K2 / 2)
        K4 = h * funcion(y[i] + h, p[i] + K3)
        p[i+1] = p[i] + (K1 + 2 * K2 + 2 * K3 + K4) / 6
    return p

# Se realiza la aproximación mediante la función "solve_ivp" de
# la biblioteca scipy.integrate

p_aprox_RK45 = spy.solve_ivp(F, [altura_inicial, altura_final], [p0],\
                             t_eval= y,method='RK45')
p_aprox_RK45_resultados = p_aprox_RK45.y[0]

# Se define el arreglo que resulta de la solución analítica

p_exacta = ((-y / 200 + 293) ** (200 * M * g / R)) * ((101325) / \
            ((293) ** (200 * M * g / R)))

# Se imprimen los datos deseados

print('Mediante método Runge-Kutta 4 \n\n', RK4(F,p0,y),\
      '\n\nmediante la función de la biblioteca scipy \n\n',\
      p_aprox_RK45_resultados,'\n\nmediante la solución analítica \n\n', p_exacta)

# Se crea una gráfica y una tabla con los resultados de los dos métodos y
# la solución analitica

plt.suptitle('Comparacion de los valores exactos con las aproximaciones obtenidas')

plt.subplot2grid((2,2),(0,0), rowspan=2)
plt.title('Solución exacta vs RK4')
plt.plot(y, p_exacta,marker = 'o', color = 'r', label='Valor exacto')
plt.plot(y, RK4(F,p0,y), color = 'b', label='Valor aproximado RK4')
plt.axis([altura_inicial, altura_final, 70000, 102000])
plt.xlabel("y (m)")
plt.ylabel("p (Pa)")
plt.grid(True)
plt.legend(loc='upper right')

plt.subplot2grid((2,2),(0,1), rowspan=2)
plt.title('Solución exacta vs RK45')
plt.plot(y, p_exacta,marker = 'o', color = 'r', label='Valor exacto')
plt.plot(y, p_aprox_RK45_resultados, color = 'g', label='Valor aproximado RK45')
plt.axis([altura_inicial, altura_final, 70000, 102000])
plt.xlabel("y (m)")
plt.ylabel("p (Pa)")
plt.grid(True)
plt.legend(loc='upper right')

plt.show()


conjuntodatos = pds.DataFrame({'altura': y, 'Aprox. RK4': RK4(F,p0,y),\
                               'Aprox. RK45': p_aprox_RK45_resultados, 'P analitico': p_exacta}\
                              , columns=['altura', 'Aprox. RK4', 'Aprox. RK45', 'P analitico'])

print(conjuntodatos)

### FIN DEL CÓDIGO ###
