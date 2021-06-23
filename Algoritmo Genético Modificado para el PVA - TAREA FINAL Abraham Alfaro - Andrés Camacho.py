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


# Parte 2) Algoritmo genético estandar Modificado(AGM)

# Se leen los las posiciones del archivo 'CoordenadasCiudades.txt'
archivo = 'CoordenadasCiudades.txt'
coordCiudades = np.loadtxt(archivo)


# In[4]:


# Se generan dos funciones: ObtenerLongitudCaminoVecinosMásCercanos(coordCiudades)
# y DistanciaEntreCiudades(nodo1, nodo2, coordCiudades) las cuales son necesarias
# para el correcto funcionamiento del algorimto genético modificado.


# In[5]:


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


# In[28]:


def ObtenerLongitudCaminoVecinosMásCercanos(coordCiudades):
    """
    Esta función obtiene la longitud del camino de los vecinos más cercanos y la trayecoria
    seguida a los vecinos más cercanos para las coordenadas de las ciudades utilizadas con una ciudad inicial seleccionada
    aleatoriamente.
    ---
    Entrada: arreglo de coordenadas de las ciudades
    Salida: La función retorna un arreglo con los índices de la trayectoria del camino a los vecinos más cercanos
    """
    # Parámetros iniciales
    longitudCaminoMasCercano = 0
    nCiudades = len(coordCiudades)
    
    # La ciudad inicial para la iteración se selecciona aleatoriamente
#     ciudadInicial = np.random.randint(nCiudades)
    ciudadInicial = 48
    ciudadActual = ciudadInicial
    ciudadesVisitadas = [ciudadInicial] # Se agrega a la lista la inicial visitada
    
    for iIteracion in range(nCiudades - 1):
        # Se inicializa la longitud al vecino más cercano como un valor muy grande 
        longitudCaminoVecinoMasCercano = 1e4
        
        # Se itera sobre todas las ciudades
        for kCiudad in range(nCiudades):
            # Se calcula la distancia entre la ciudad actual y la kCiudad
            longitudCamino = DistanciaEntreCiudades(ciudadActual, kCiudad, coordCiudades)
        
            if longitudCamino < longitudCaminoVecinoMasCercano and longitudCamino > 0 and kCiudad not in ciudadesVisitadas:
                longitudCaminoVecinoMasCercano = longitudCamino
                ciudadMasCercana = kCiudad
                
        # Se actualizan los valores
        longitudCaminoMasCercano += longitudCaminoVecinoMasCercano
        ciudadActual = ciudadMasCercana
        ciudadesVisitadas.append(ciudadMasCercana)
    
    return ciudadesVisitadas


# In[7]:


#2.a) y 2.b) Inicialización


# In[8]:


#2.e) Operaodor Mutación


# In[9]:


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


# In[10]:


def OperadorMutaciónModificado(cromosoma):
    '''
    Aplica de 3 a 10 mutaciones a los 49 cromosomos restantes
    de la población inicial.
    cromosoma: cromosoma que se ingresa como parámetro para mutar
    return: retorna el cromosoma mutado.
    '''
    # Se hace una copia del parametro que ingresa
    cromosomaMutado = np.copy(cromosoma)
    # Se escoge la cantidad de mutaciones a realizar entre 3 y 10
    cantidadPermutaciones = np.random.randint(3,11)
    # Se aplican las permutaciones
    for mutacion in range(cantidadPermutaciones):
        cromosomaMutado = np.copy(OperadorMutación(cromosomaMutado))
        
    # Se retorna el cromosoma mutado
    return cromosomaMutado


# In[11]:


def InicializaciónModificada(tamañoPoblación, coordCiudades):
    """
    Inicializa la población de individuos para la optimización de una manera modificada. 
    tamañoPoblación: Cantidad de cromosomas (individuos) que tendrá la población.
    coordCiudades: arreglo que contiene a las 50 coordenadas de las 50 ciudades.
    return: un arreglo donde cada fila (cromosoma) tiene 50 posibles ciudades donde 
    el primer individuo tiene el primer elemento escogido de forma aleatoria y  a partir
    de este, se crea la trayectoria a los vecinos más cercanos. Los otros 49 cromosomas son 
    mutados de 3 a 10 mutaciones.
    """
    nCiudades = len(coordCiudades)
    población = []
    
    for iFila in range(tamañoPoblación): # El tamaño es un parámetro ajustable (cantidad de cromosomas)
        iTrayecto = ObtenerLongitudCaminoVecinosMásCercanos(coordCiudades)
        población.append(iTrayecto)
    población = np.copy(población)
    
    # Se aplica la mutación a todos los individuos menos el primero
    for iCromosoma in range(1, tamañoPoblación): # Comienza en 1 pues el inicial debe permanecer inmutable.
        cromosomaAMutar = np.copy(población[iCromosoma])
        cromosomaAMutar = np.copy(OperadorMutaciónModificado(cromosomaAMutar))
        población[iCromosoma] = np.copy(cromosomaAMutar)
        
    return población


# In[12]:


#2.c) Función de ajuste


# In[13]:


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


# In[14]:


#2.d) NO HAY OPERADORES EVOLUCIONARIOS


# # Implementación del Algoritmo Genético Estándar

# In[35]:


def Optimización():
    '''
    Función de optimización estocástica: Algoritmo genético estándar
    Script principal del algoritmo.
    '''

    # Parámetros iniciales
    tamañoPoblación = 100
    probabilidadMutacion = 1
    distanciaMinimaPrueba = 123
    ajusteMaximoPrueba = 1/distanciaMinimaPrueba
    iGenMax = 10000
    valoresAjuste = np.zeros(tamañoPoblación)  # Matriz que contendrá valores de ajuste
    print('Ejecución del algoritmo genético estándar...\tOk')

    "# PASO 1) Inicialización"

    # Población Inicial
    población = InicializaciónModificada(tamañoPoblación, coordCiudades)

    # Lista para guardar el historial de valores de ajuste
    listaValoresAjuste = []
    
    ajusteMax = 0.0
    iGen = 0
    # Ciclo principal. El criterio para determinar el final de la ejecusión
    # algortimo es el número de generaciones.
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

        # Fin de la iteración sobre la población

        # Se guardan los valores de ajuste de la población actual
        listaValoresAjuste.append(np.copy(valoresAjuste))

        # Se imprime información relevante de la iteración sobre la población
        # cada 10 generaciones y la última
        if iGen % 10000 == 0 or iGen + 1 == iGenMax:
            print('\nGeneración {}:'.format(iGen))
            print('\tValor de ajuste máximo: {}'.format(ajusteMax))

        # PASO 3) Formación de la próxima generación

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
        iGen += 1
                
    # Fin de la iteración sobre las generaciones
    ##########################################################################################
    # print('\nResultados finales')
    # print('Puntuación Máxima: {}'.format(ajusteMax))
    return listaValoresAjuste, iMejorIndividuo


# In[33]:


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
print('La distancia más corta recorrida es: {}'.format(distanciaCorta))


# In[ ]:


# Sección de graficación


# In[17]:


def GráficasEvolución(listaValoresAjuste):
    #Procesamiento de los valores de ajuste obtenidos
    arregloValoresAjuste = np.asarray(listaValoresAjuste)
    promedioAjuste = np.mean(arregloValoresAjuste, 1)
    valoresMaximosAjuste = np.max(arregloValoresAjuste, 1)
    
    # Gráficos de la evolución de los valores de ajuste
    fig, ax = plt.subplots(dpi=120)
    ax.plot(promedioAjuste, label = 'ajuste promedio')
    ax.plot(valoresMaximosAjuste, label = 'ajuste máximo')
    
    ax.set_title('Evolución de los valores de ajuste de la población')
    ax.set_xlabel('Generaciones')
    ax.set_ylabel('valores de ajuste')
    ax.legend(loc = 'best')
    plt.show()


# In[18]:


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


# In[34]:


# Se grafican la evolución temporal de los valores de ajuste
GráficasEvolución(listaValoresAjuste)


# In[36]:


# Se grafica el camino
GraficaLaTrayectoria(iMejorIndividuo)


# In[ ]:


# Se guarda el camino más corto encontrado
encabezado = 'Indices de la trayectoria más corta'
matriz=[iMejorIndividuo]
np.savetxt('CaminoMásCorto_AGM.txt', matriz, delimiter=',',newline='\n',  fmt='%d', header= encabezado)


# In[ ]:




