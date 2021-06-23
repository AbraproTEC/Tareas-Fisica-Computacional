#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Tarea S15: AG aplicado al problema del vendedor ambulante (PVA)
# Estudiantes: Abraham Alfaro Alvarado / Andrés Camacho Alvarado
# Profesores: Esteban Pérez Hidalgo / Álvaro Amador Jara


# In[2]:


# Importación de los paquetes necesarios
import numpy as np
import matplotlib.pyplot as plt


# In[3]:


# Parte 1) Algoritmo genético estandar (AG)

# Se leen los las posiciones del archivo 'CoordenadasCiudades.txt'
archivo = 'CoordenadasCiudades.txt'
coordCiudades = np.loadtxt(archivo)


# In[4]:


#1.a) Inicialización


# In[5]:


#1.b) Codificación de los cromosomas


# In[6]:


def Codificación(tamañoPoblación, coordCiudades):
    """
    Inicializa y codifica la población de individuos para la optimización. 
    tamañoPoblación: Cantidad de cromosomas (individuos) que tendrá la población.
    coordCiudades: arreglo que contiene a las 50 coordenadas de las 50 ciudades.
    return: un arreglo donde cada fila (cromosoma) tiene 50 posibles ciudades
    ordenadas aleatoriamente.
    """
    nCiudades = len(coordCiudades)
    población = []
    
    # Ciclo para crear los cromosomas (posibles trayectorias)
    for iFila in range(tamañoPoblación): # El tamaño es un parámetro ajustable
        iTrayecto = []
        for ciudad in range(nCiudades):
            iTrayecto.append(ciudad)
        # Se permutan aleatoriamente todas las posiciones a visitar
        trayectoPermutado = np.random.permutation(iTrayecto)
        población.append(trayectoPermutado)
    # Se retorna la población inicializada
    return población


# In[7]:


#1.c) Función de ajuste


# In[8]:


def DistanciaEntreCiudades(nodo1, nodo2, coordCiudades):
    '''
    Cálculo de la longitud euclídea entre dos ciudades
    ---
    Entradas:nodo1, nodo2: enteros, índices de las ciudades a calcular; arreglo de las ciudades
    '''
    
    deltaX = coordCiudades[nodo2,0] - coordCiudades[nodo1,0]
    deltaY = coordCiudades[nodo2,1] - coordCiudades[nodo1,1]
    
    longitudTrayectoria = np.sqrt(deltaX**2 + deltaY**2)
    
    return longitudTrayectoria


# In[9]:


def FuncionDeAjuste(cromosoma, coordCiudades):
    '''
    Calcula el valor del ajuste para cada cromosoma (posible trayectoria)
    y le asigna un valor que es el inverso de la longitud euclideana de 
    la trayectoria seguida.
    cromosoma: individuo a evaluar (calcular el ajuste)
    coordCiudades: arreglo con las coordenadas de las 50 ciudades.
    return: el ajuste que es el inverso de la longitud euclideana de 
    la trayectoria seguida.
    '''
    
    # Se inicializa la longitud en cero
    longitudCamino = 0
    nCiudades = len(coordCiudades) # nCiudades = 50
    
    # Los cromosomas contienen las posiciones de las ciudades
    for kCiudad in range(nCiudades): # kCiudades = 0, 1, 2, ..., 49
        
        if kCiudad == (nCiudades - 1): # Si estoy en la última ciudad (49) sume la distancia al origen.
            # cromosoma[0] = coordenada primera ciudad
            # cromosoma[-1] = coordenada última ciudad
            kdistancia = DistanciaEntreCiudades(cromosoma[0] , cromosoma[-1], coordCiudades)
            longitudCamino += kdistancia 
        else:
            kdistancia = DistanciaEntreCiudades(cromosoma[kCiudad] , cromosoma[kCiudad+1], coordCiudades)
            longitudCamino += kdistancia
            
    # retornamos el ajuste   
    return 1/longitudCamino


# In[10]:


#1.d) NO HAY OPERADORES EVOLUCIONARIOS SOLO EL DE MUTACIÓN


# In[11]:


#1.e) Operaodor Mutación


# In[12]:


def OperadorMutación(cromosoma):
    """
    Intercambia las posiciones de dos genes de un cromosoma
    cromosoma: trayecto escogido para ser mutado
    return: retorna el trayecto original con dos posiciones permutadas.
    """
    nGenes = len(cromosoma) # nGenes = 50
    # -------------------------------------#
    # Se escogen aleatoriamente dos genes a permutar
    primerGen = np.random.randint(nGenes)
    segundoGen = np.random.randint(nGenes)
    # -------------------------------------#
    genNuevo1 = cromosoma[primerGen]
    genNuevo2 = cromosoma[segundoGen]
    # -------------------------------------#
    cromosoma[primerGen] = genNuevo2
    cromosoma[segundoGen] = genNuevo1
    # -------------------------------------#
    return cromosoma


# # Implementación del Algoritmo Genético Estándar

# In[75]:


def Optimización():
    '''
    Función de optimización estocástica: Algoritmo genético estándar
    Script principal del algoritmo.
    '''

    # Parámetros iniciales
    tamañoPoblación = 100
    probabilidadMutacion = 1
    # Distancia mínima a buscar (se usan varios valores para estudiar el comportamiento)
    distanciaMinimaPrueba = 350
    ajusteMaximoPrueba = 1/distanciaMinimaPrueba
    iGenMax = 100000
    valoresAjuste = np.zeros(tamañoPoblación)  # Matriz que contendrá valores de ajuste
    print('Ejecución del algoritmo genético estándar...\tOk')

    "# PASO 1) Inicialización"

    # Población Inicial
    población = Codificación(tamañoPoblación, coordCiudades)

    # Lista para guardar el historial de valores de ajuste
    listaValoresAjuste = []
    ajusteMax = 0.0
    
    # Ciclo principal. El criterio para determinar el final de la ejecusión
    # algortimo es el número de generaciones.
    iGen = 0
    
    # El ciclo principal se ejecutará si el ajusteMax es menor al ajusteMaximoPrueba
    # y si las interaciones (generaciones) son diferentes a las iGenMax
    while ajusteMax < ajusteMaximoPrueba and iGen < iGenMax:

        "# PASO 2) Evaluación (Calificación de los candidatos)"

        # Iteración sobre la población para asignar un valor de ajuste a cada individuo
        for iInd in range(tamañoPoblación):
            cromosoma = np.copy(población[iInd])  # Accedo a un individuo a la vez

            # Se evaluan las trayectorias y se almacenan
            valoresAjuste[iInd] = FuncionDeAjuste(cromosoma, coordCiudades)

            # Se prueba si el individuo es el mejor de su generación
            if valoresAjuste[iInd] > ajusteMax:
                ajusteMax = valoresAjuste[iInd]
                iMejorIndividuo = población[iInd]
                iMejorIndividuoIndice = iInd

        # Fin de la iteración sobre la población

        # Se guardan los valores de ajuste de la población actual
        listaValoresAjuste.append(np.copy(valoresAjuste))

        # Se imprime información relevante de la iteración sobre la población
        # cada 1000 generaciones y la última
        if iGen % 10000 == 0 or iGen + 1 == iGenMax:
            print('\nGeneración {}:'.format(iGen))
            print('\tValor de ajuste máximo: {}'.format(ajusteMax))

        '# PASO 3) Formación de la próxima generación'

        # Se crea una matriz para guardar la población nueva
        poblaciónTemporal = np.copy(población)

        # Mutaciones en los nuevos cromosomas
        # Iteración sobre la problación para aplicar el operador mutación
        for iInd in range(tamañoPoblación):
            # Se obtiene el cromosoma correspondiente a la iteración
            cromosomaOriginal = np.copy(poblaciónTemporal[iInd, :])
            nAleatorio = np.random.random()
            if nAleatorio < probabilidadMutacion:
                cromosomaMutado = OperadorMutación(cromosomaOriginal)
                # Se guarda el cromosoma mutado
                poblaciónTemporal[iInd, :] = np.copy(cromosomaMutado)
            else:
                # Se guarda el cromosoma sin mutar
                poblaciónTemporal[iInd, :] = np.copy(cromosomaOriginal)

        # Fin de la iteración sobre la población
        # Se almacena la nueva población
        población = np.copy(poblaciónTemporal)
        
        # Se suma una generación al contador
        iGen +=1
        
    # Fin de la iteración sobre las generaciones
    ##########################################################################################
    # print('\nResultados finales')
    # print('Puntuación Máxima: {}'.format(ajusteMax))
    return listaValoresAjuste, iMejorIndividuo


# In[85]:


# Se obtiene la lista de valores de ajuste
# del algoritmo de optimización
listaValoresAjuste, iMejorIndividuo = Optimización()

# El camino más corto será
print('La mejor forma de recorrer las ciudades es: {}'.format(iMejorIndividuo))

# El ajuste:
ajusteMax = FuncionDeAjuste(iMejorIndividuo, coordCiudades)
print('El ajuste máximo es: {}'.format(ajusteMax))

# La distancia recorrida es:
distanciaCorta = 1 / ajusteMax 
print('La distancia más corta recorrida es: {} unidades'.format(distanciaCorta))


# In[ ]:


# Sección de graficación


# In[86]:


def GráficasEvolución(listaValoresAjuste):
    #Procesamiento de los valores de ajuste obtenidos
    arregloValoresAjuste = np.asarray(listaValoresAjuste)
    promedioAjuste = np.mean(arregloValoresAjuste, 1)
    valoresMaximosAjuste = np.max(arregloValoresAjuste, 1)
    
    # Gráficos de la evolución de los valores de ajuste
    fig, ax = plt.subplots(dpi=120)
    ax.plot(promedioAjuste, label = 'ajuste promedio')
    ax.plot(valoresMaximosAjuste, label = 'ajuste máximo por generación')
    
    ax.set_title('Evolución de los valores de ajuste de la población')
    ax.set_xlabel('Generaciones')
    ax.set_ylabel('valores de ajuste')
    ax.legend(loc = 'best')
    plt.show()


# In[87]:


def GraficaLaTrayectoria(trayectoria):
    trayectoria = np.copy(trayectoria)
    coordenadas_a_graficar=[]
    for i in range (len(trayectoria)):
        indice = trayectoria[i]
        coordenadas_a_graficar.append(coordCiudades[indice])
    primerindice = trayectoria[0]
    coordenadas_a_graficar.append(coordCiudades[primerindice])
    coordenadas_a_graficar = np.asarray(coordenadas_a_graficar).T

    # Grafica la trayectoria
    fig, ax = plt.subplots(dpi=120)

    ax.plot(coordenadas_a_graficar[0][0], coordenadas_a_graficar[1][0], marker='o', color='darkgreen', label='inicio')
    ax.plot(coordenadas_a_graficar[0],coordenadas_a_graficar[1], marker = '.',markerfacecolor = 'green', color='khaki',label='camino')
    ax.plot(coordenadas_a_graficar[0][-2], coordenadas_a_graficar[1][-2], marker='o', color='crimson', label='final')
    ax.set_title('Trayectoria recorrida')
    ax.set_xlabel('coordenada en x')
    ax.set_ylabel('coordenada en y')
    ax.legend(loc='best')
    plt.show()
    return


# In[88]:


# Se grafican la evolución temporal de los valores de ajuste
GráficasEvolución(listaValoresAjuste)


# In[89]:


# Se grafica el camino
GraficaLaTrayectoria(iMejorIndividuo)


# In[90]:


# Se guarda en un archivo txt el camino
encabezado = 'Indices de la trayectoria más corta'
matriz=[iMejorIndividuo]
np.savetxt('CaminoMásCorto_AGE.txt', matriz, delimiter=',',newline='\n',  fmt='%d', header= encabezado)


# In[ ]:




