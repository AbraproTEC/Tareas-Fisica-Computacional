# Curso: Física Computacional I
# Estudiantes: Abraham Alfaro Alvarado / Andrés Camacho Alvarado
# Tarea Semana 13 Parte 1: Difusión de un fotón en el sol (camino aleatorio)

import numpy as np
import matplotlib.pyplot as plt

def PasoAleatorio(lista_posicion, camino_libre_medio):
    '''Genera un vector con longitud l y dirección aleatoria, respecto al punto anterior.

    Parametros
    lista_posicion: La lista en componentes xyz a partir de donde se dará el paso.
    camino_libre_medio: La longitud entre choque y choque del fotón.

    Retorno: La nueva posición despues de dar un paso de radio l, en una lista de componentes xyz.'''

    #Se genera un vector aleatorio a partir de valores aleatorios entre -1 y 1 para las componentes xyz.
    paso_x = (np.random.random()-0.5)*2
    paso_y = (np.random.random()-0.5)*2
    paso_z = (np.random.random()-0.5)*2

    #Se calcula la norma del vector generado anteriormente.
    norma = (paso_x ** 2 + paso_y ** 2 + paso_z ** 2) ** (1 / 2)

    #Se normaliza el vector generado y se multiplica por la longitud del paso deseada.
    paso_x = camino_libre_medio * paso_x / norma
    paso_y = camino_libre_medio * paso_y / norma
    paso_z = camino_libre_medio * paso_z / norma

    #Se suma el paso a las coordenadas anteriores.
    nueva_posicion_x = lista_posicion[0][0] + paso_x
    nueva_posicion_y = lista_posicion[1][0] + paso_y
    nueva_posicion_z = lista_posicion[2][0] + paso_z

    #Se actualiza la lista con las nuevas coordenadas.
    lista_posicion[0][0] = nueva_posicion_x
    lista_posicion[1][0] = nueva_posicion_y
    lista_posicion[2][0] = nueva_posicion_z

    return lista_posicion

def CaminoAleatorio(radio, camino_libre_medio, pasosParada, listaFinal):
    '''Genera un camino de pasos aleatorios.

    Parametros
    listaFinal: Lista de pasos a graficar.
    pasosParada: Cantidad Máxima de pasos (esto se hizo para que el bucle no se alargue demasiado y se ralentice la computadora).
    radio: distancia de parada del fotón.
    camino_libre_medio: La longitud entre choque y choque del fotón.

    Retorno: Una lista de todos los pasos a graficar y la cantidad de pasos que dió el fotón.'''

    #Se inicializan las variables a utilizar.
    distancia=0
    paso=0
    multiplicador = 1
    k=1 #Variable contador para los checkpoints.
    inicio = [[0.], [0.], [0.]]

    #Se crea el bucle sobre el cual se darán los pasos.
    while distancia < radio:
        paso = paso + 1 #Se realiza el conteo de pasos.
        inicio=PasoAleatorio(inicio, camino_libre_medio) #Se llama a la funcion que haace un paso aleatorio a partir del pasado.
        x, y, z = inicio[0][0], inicio[1][0], inicio[2][0]
        distancia = (x ** 2 + y ** 2 + z ** 2) ** (1 / 2)   #Se hace el cálculo de la distancia del centro al paso generado anteriormente.

        #Condicional para no graficar todos los pasos y ahorrar memoria (para que no se ralentice tanto la computadora).
        if paso == multiplicador*100:

            #Se anade el punto a la lista a graficar.
            listaFinal[0].append(inicio[0][0])
            listaFinal[1].append(inicio[1][0])
            listaFinal[2].append(inicio[2][0])

            #CHECKPOINTS para saber que todo corre bien.
            if multiplicador / 1000000 == k:
                print(distancia, paso)
                k=k+1

            #Se hace el conteo del multipliacador.
            multiplicador = multiplicador + 1

        #Condicional de parada por pasos máximos.
        elif paso == pasosParada*1000000 + 1:
            break

    return listaFinal, paso

def PromedioPasos(replicas, radio, camino_libre_medio):
    '''Genera caminos de pasos aleatorios con iteraciones que duran menos tiempo, ya que no hay que guardar listas para graficar.

    Parametros
    replicas: cantidad de veces que se va a correr el camino aleatorio para promediar el número de pasos.
    radio: distancia de parada del fotón.
    camino_libre_medio: La longitud entre choque y choque del fotón.

    Retorno: Una lista con los pasos totales recorridos en cada camino aleatorio'''

    #Se incializa la lista donde se guardarán los pasos dados en cada camino.
    lista = []

    #Se hace el bucle para que se hagan las replicas.
    for replica in range (replicas):
        #Se inicializan las variables a utilizar.
        distancia = 0
        paso = 0
        inicio = [[0.], [0.], [0.]]

        # Checkpoints para saber que todo va bien.
        print('Espere, solo faltan', replicas - replica, 'replicas')

        #Se inicia el bucle para que se hagan los caminos en un tiempo optimizado.
        while distancia < radio:
            paso = paso + 1 #Conteo de pasos.
            inicio=PasoAleatorio(inicio, camino_libre_medio) #Se agrega un paso al camino.
            x, y, z = inicio[0][0], inicio[1][0], inicio[2][0]
            distancia = (x ** 2 + y ** 2 + z ** 2) ** (1 / 2) #Cacula la distancia al centro.

        #Se agrega la cantidad de pasos totales a la lista de pasos totales
        lista.append(paso)

    return lista

#Usando el concepto de la raiz cuadrática media R=N^1/2 *rms se calculan los pasos las distancias y los tiempos.

#PARTE B
print('Usando el concepto de la raiz cuadrática media R=N^1/2 *rms.')

R = 0.1
rms = 0.00005
N = (R/rms)**2
print('El valor teorico de pasos es', int(N),'pasos para un radio externo de', R, 'm.')


#PARTE C
replicas_a_promediar = 5
print('Ahora se calcula el promedio de pasos en', replicas_a_promediar, 'replicas')
listapasos = PromedioPasos(replicas_a_promediar, R, rms)
print('El promedio de pasos de', replicas_a_promediar,'replicas fue de', np.mean(listapasos), 'pasos.')

#PARTE B realista
print('Para una simulacion realista de la difusión de un fotón del centro del sol')
R = 5*(10**8) #m
rms = 5*(10**(-5)) #m
N = (R / rms)**2 #pasos
print('Con un R =',R, 'm y rms =', rms, 'm, se obtiene un N =', N, 'pasos.')


#PARTE D realista
distancia = N * rms #m
print('El fotón recorrió una distancia de', distancia, 'm.')

c = 3*(10**8) #m/s    Velocidad del fotón.
tiempo_s = distancia / c #s
tiempo_h = tiempo_s / 3600 #h
tiempo_d = tiempo_h / 24 #días
tiempo_a = tiempo_d / 365 #años
print('Por lo tanto, El fotón dura', int(tiempo_a),'años aproximadamente, para alcanzar un radio de', R, 'm.')

#PARTE E
#Se inicializan las constantes a utilizar para la graficacion del camino recorrido por el fotón.
radio_externo = 0.1 #Radio considerable para que la simulación no dure demasiado.
l = 0.00005 #Longitud del paso.
maximo_pasos = 30 #Cantidad de pasos para que se detenga la simulación (en milones).
centro_del_sol = [[0.], [0.], [0.]]
listaGraficar, N = CaminoAleatorio(radio_externo, l, maximo_pasos, centro_del_sol)

# Gráfico en 3d
lado_del_grafico = radio_externo
fig = plt.figure(figsize=(20, 20))
ax = fig.gca(projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_xlim3d(-lado_del_grafico, lado_del_grafico)
ax.set_ylim3d(-lado_del_grafico, lado_del_grafico)
ax.set_zlim3d(-lado_del_grafico, lado_del_grafico)
ax.plot(listaGraficar[0], listaGraficar[1], listaGraficar[2], c='m')
ax.set_title('Fotón saliendo del sol, con un radio externo de {} m en {} pasos.'.format(radio_externo,N))
plt.show()