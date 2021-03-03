#FÍSICA COMPUTACIONAL I
#ESTUDIANTES: JOSÉ ABRAHAM ALFARO ALVARADO / ANDRÉS CAMACHO ALVARADO
#PROFESORES: JOSÉ ESTEBAN PEREZ HIDALGO / ÁLVARO AMADOR JARA
#TAREA SEMANA 02: INTEGRACIÓN Y DERIVACIÓN NUMÉRICA

#----------------------IMORTACIÓN DE PAQUETES-------------------#
import math
#----------------------PRIMERA PARTE INTEGRACIÓN NUMÉRICA-------------------#
def Velocidad(t):
    '''
    Devuelve la velocidad con respecto al tiempo evaluado, de la
    función a analizar.
    t: parametro que representa al eje del tiempo (variable independiente).
    '''
    return (0.005*t+0.5)

def Integrar_Metodo_Rectangulos(num_intervalos):
    '''
    Integrar mediante la regla del rectángulo de Newton-Cotes
    para aproximar el desplazamiento de un móvil.

    num_intervalos: el metodo requiere la cantidad
    de veces a particionar el intervalo de integración.
    '''

    # Inicialización de las variables a utilizar en el método.
    t_Inicial = 0
    t_Final = 100
    h = (t_Final - t_Inicial) / num_intervalos
    desplazamientoAproximado = 0
    valor_exacto = 75
    # Método iterativo para el calculo aproximado del desplazamiento.
    for i in range(num_intervalos):
        iTiempo = t_Inicial + i*h
        velocidad_t = Velocidad(iTiempo)
        iesimoDesplazamiento = h*velocidad_t
        desplazamientoAproximado = desplazamientoAproximado + iesimoDesplazamiento
        error = ((valor_exacto - desplazamientoAproximado)/valor_exacto)*100
    print('La integral es aprox: {} y un {} % de error'.format(desplazamientoAproximado , error))

#----------------------SEGUNDA PARTE DERIVACIÓN NUMÉRICA-------------------#

def PosicionConRespectoAlTimepo(t):
    '''
    Devolver la posición con respecto al tiempo de la función a analizar
    t: Parametro que representa al eje del tiempo (variable independiente)
    '''
    return (0.005) * (t ** 2) - 5


def derivada(funcion, valor_evaluacion, h=0.05):
    '''
    Calcular la derivada de una funcion
    funcion: funcion a derivar
    valor_evaluacion: valor en el que se evaluará la derivada de la funcion
    h: valor del ancho de la diferencia en las abscisas
    '''
    return ((funcion(valor_evaluacion + h) - funcion(valor_evaluacion - h)) / (2 * h))


def ceros_NewtonRapshon(tiempo_aproximado_anterior, tolerancia=0.01):
    '''
    La funcion retornara la aproximacion encontrada para el cero y el error relativo.
    tiempo_aproximado_anterior: Valor elegido como aproximacion inicial
    tolerancia: Cuanto se tolerara para el valor del error relativo
    '''

    # Inicializacion de variables.
    i = 0
    error = 1
    valor_exacto = math.sqrt(1000)

    # Método iterativo para el calculo aproximado del tiempo cuando la posicion es cero.
    while error > tolerancia:
        tiempo_aproximado = tiempo_aproximado_anterior - (
                    PosicionConRespectoAlTimepo(tiempo_aproximado_anterior) / derivada(PosicionConRespectoAlTimepo,
                                                                                       tiempo_aproximado_anterior))
        error = abs(tiempo_aproximado - valor_exacto) / abs(valor_exacto)
        tiempo_aproximado_anterior = tiempo_aproximado
        i = i + 1

    print(
        'El valor aproximado del tiempo cuando la posición es 0 es: {} s, con un error de: {} %, en {} iteraciones'.format(
            tiempo_aproximado, error * 100, i))

