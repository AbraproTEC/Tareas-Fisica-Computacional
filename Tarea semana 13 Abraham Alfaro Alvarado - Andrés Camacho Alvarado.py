# Curso: Física Computacional I
# Estudiantes: Abraham Alfaro Alvarado / Andrés Camacho Alvarado
# Tarea Semana 13 Parte 2: Simulación Metrópolis-Monte Carlo: Propiedades termodinámicas de un modelo de Ising en 1-D

# Se importan las bibliotecas necesarias
import numpy as np
import matplotlib.pyplot as plt


# # Ejecusión principal del algoritmo para el Modelo de Isind 1-D
# # a) Modifique la simulación para calcular la energía interna y magnetización del sistema de espines.
# # d) Realice las simulaciones para diferentes configuraciones iniciales de los espines (todos en una sola dirección arriba y abajo, así como la configuración inicial aleatoria)

# SE ESCOJE QUE ESTADO INICIAL SE LE QUIERE DAR A LOS ESPINES
estado_inicial = str(input('Estado inicial del sistema: (arriba), (abajo), (aleatorios): '))
#--------------------------------------------------------------------------------------------------
def EnergiaIsing(arreglo_espines, valorJ):
    '''
    -------
    Cálcula la energía del sistema de espines
    arreglo_espines: contiene los espines con valores de 1 (arriba) o -1 (abajo)
    valorJ: valor flotante que representa a la constante de cambio (exchange constant)
    -------
    return: devuele un valor flotante que indica la energía del estado de espines que ingresó.
    '''
    valorEnergia = 0

    for i in range(len(arreglo_espines)-1):
        valorEnergia += arreglo_espines[i] * arreglo_espines[i + 1]
    return -valorJ*valorEnergia
#--------------------------------------------------------------------------------------------------
def MagnetizacionIsing(arreglo_espines):
    '''
    -------
    Cálcula la magnetización del sistema de espines
    arreglo_espines: espines a ser evaluados mediante la formula de magnetización
    -------
    return: devuelve un valor flotante correspondiente a la magnetización
    '''
    valorMagnetizacion = 0
    
    # Este ciclo itera sobre los espines y suma sus valores (arriba = 1 o abajo = -1)
    for i in range(len(arreglo_espines)-1):
        valorMagnetizacion += arreglo_espines[i]
        
    return valorMagnetizacion
#--------------------------------------------------------------------------------------------------
def EspinesAleatorios(nEspines):
    '''
    ------
    Genera un arreglo de espines en orientaciones aleatorias arriba (1) o abajo (-1).
    nEspines: cantidad de espines que se desea que tenga el sistema
    ------
    return: un arreglo con numeros aleatorios 1 o -1.
    '''
    arreglo_espines = np.random.randint(-1, 1, size=nEspines) # Esta definición no incluye al 1: [-1, 0, 1[
    for i in range(nEspines):
        if arreglo_espines[i] == 0: # Esto pues la definición del arreglo involucra al cero y debemos quitarlo
            if np.random.random() > 0.5:
                arreglo_espines[i] = +1
            else:
                arreglo_espines[i] = -1
    return arreglo_espines
#--------------------------------------------------------------------------------------------------
def ModeloIsing1d(temperatura, nPasos, estado_inicial = 'arriba'):
    '''
    -------
    Ejecuta el algoritmo de metrópolis para el análsis del modelo de Ising
    en 1D
    temperatura: temperatura del sistema de Ising (baño térmico)
    nPasos: cantidad de iteraciones a evolucionar el estado del sistema
    estado_inicial: configuración inicial de los espines (por defecto 'arriba')
    -------
    return: retorna los siguientes arreglos: magnetización, energía y energía al cuadrado.
    '''
    #Parámetros de la simulación
    kBoltzmann = 1
    nEspines = 100
    valorJ = 1

    # Determinación del arreglo inicial
    if estado_inicial == 'arriba':
        # inicialización de espines hacia arriba
        arregloEspines = np.ones([nEspines], int)
    elif estado_inicial == 'abajo':
        # inicialización de espines hacia abajo
        arregloEspines = np.ones([nEspines], int)*-1
    elif estado_inicial == 'aleatorios':
        # inicialización de espines aleatorios
        arregloEspines = EspinesAleatorios(nEspines)

    # Cálculo de la energía inicial del sistema de espines
    energia_ini = EnergiaIsing(arregloEspines, valorJ)

    # Cálculo de la magnetización inicial
    mag_ini =  MagnetizacionIsing(arregloEspines)

    
    # Creación de las listas de retorno.
    listaMagne = []
    listaMagne.append(mag_ini) # Se agrega la magnetización inicial del sistema.
    listaEnergiasE = []
    listaEnergiasE.append(energia_ini)  # Se agrega la energía inicial del sistema.
  
    # Ciclo principal
    for k in range(nPasos):
        # Calculo la energía del estado i
        iEnergia = EnergiaIsing(arregloEspines, valorJ)

        # Se escoge el espin a 'mover'
        iEspin = np.random.randint(nEspines)

        # Se cambia el estado del espin
        arregloEspines[iEspin] *= -1

        # Calcula la energía del posible estado j
        jEnergia = EnergiaIsing(arregloEspines, valorJ)

        # Se calcula el cambio en la energía del sistema
        deltaE = jEnergia - iEnergia

        # Se calcula la probabilidad de aceptación
        pAceptacion = np.exp(-deltaE / (kBoltzmann * temperatura))


        # Se prueba si se acepta el cambio
        if deltaE > 0:
            if np.random.random() < pAceptacion:
                pass  # Se acepta el cambio

            else:
                arregloEspines[iEspin] *= -1  # Se rechaza el cambio (volvemos al estado original)

        else:
            pass  # Se acepta el cambio pues la energía del estado j es menor a la del esta i
        
        # Se crean nuevas variables para no alterar la ejecusión
        energiaActual = EnergiaIsing(arregloEspines, valorJ)
        magneActual = MagnetizacionIsing(arregloEspines)
        
        # Se agregan a los arreglos de retorno
        listaMagne.append(magneActual)
        listaEnergiasE.append(energiaActual)
    # Fin del ciclo principal
    
    return listaEnergiasE, listaMagne
#--------------------------------------------------------------------------------------------------
# # b) Espere a que las simulaciones entren en equilibrio y calcule los valores de energía y magnetización para un solo valor de temperatura.

# Variable ajustable que tiene como función ejecutar el modelo a diferestes
# temperaturas (baño térmico) ingresadas, e indentificar para que cantidad 
# de pasos el sistema llega al equilibrio.
temperatura_const = float(input('Ingrese la temperatura del baño térmico: '))
#--------------------------------------------------------------------------------------------------
# Cantidad de pasos (microestados) por los que pasará el sistema de espínes
# Otra manera de idenficar esta variable es pensar en la cantidad de pasos
# en los cuales el sistema de espines cambiará su configuración.
nPasos =int(input('Ingresa la cantidad nPasos: '))
#--------------------------------------------------------------------------------------------------
def GraficaEnergia(temperatura, nPasos):
    '''
    -------
    Hace un llamado a la función Modelo_Ising_1d() y extrae el valor
    de la energía para una temperatura específica luego de nPasos.
    temperatura: temperatura del baño térmico a analizar
    nPasos: cantidad de iteraciones a evolucionar el estado del sistema
    -------
    return: un arreglo con los valores de la energía para cada nPaso.
    '''
    
    # Graficación de la Energía
    listaE = ModeloIsing1d(temperatura, nPasos, estado_inicial)[0] # Se extrae la primera salida de la función
    energGrafico = np.asarray(listaE)
    
    return energGrafico
#--------------------------------------------------------------------------------------------------
grafica_Ener = GraficaEnergia(temperatura_const, nPasos)
energia_media = np.mean(grafica_Ener[1000:])
fig, ax = plt.subplots(figsize = (4,4), dpi = 100)
ax.plot(grafica_Ener, color = 'y')
plt.axhline(energia_media, 0, 1, label='Energía promedio: {}'.format(round(energia_media,2)))
ax.set_title('Simulación de modelo de Ising en 1-D a una kT = {} y con todos los espines: {}'.format(temperatura_const , estado_inicial))
ax.set_xlabel('Pasos')
ax.set_ylabel('Energía')
plt.legend(loc = 'lower right')
plt.show()
#--------------------------------------------------------------------------------------------------
paso_Equilibrio_T = int(input('Ingresar el paso a partir del cual la simulación entró en equilibrio: '))
#--------------------------------------------------------------------------------------------------
def GraficaMagnetizacion(temperatura,nPasos):
    '''
    -------
    Hace un llamado a la función Modelo_Ising_1d() y extrae el valor
    de la magnetización para una temperatura específica luego de nPasos
    temperatura: temperatura del baño térmico a analizar
    nPasos: cantidad de iteraciones a evolucionar el estado del sistema
    -------
    return: un arreglo con los valores de la magnetización para cada nPaso.
    '''
    
    # Graficación de la magnetización
    listaMagne = ModeloIsing1d(temperatura, nPasos, estado_inicial)[1] # Se extrae la segunda salida de la función
    magneGrafico = np.asarray(listaMagne)
    
    return magneGrafico
#--------------------------------------------------------------------------------------------------
grafica_Magne = GraficaMagnetizacion(temperatura_const,nPasos)
magnetizacion_media = np.mean(grafica_Magne)
fig, ax = plt.subplots(figsize = (4,4), dpi = 100)
ax.plot(grafica_Magne, color = 'magenta')
plt.axhline(magnetizacion_media, 0, 1, label='Magnetización promedio: {}'.format(round(magnetizacion_media,2)))
ax.set_title('Simulación de modelo de Ising en 1-D a una kT = {} y con todos los espines: {}'.format(temperatura_const, estado_inicial))
ax.set_xlabel('Pasos')
ax.set_ylabel('Magnetización')
plt.legend(loc = 'lower right')
plt.show()
#--------------------------------------------------------------------------------------------------
paso_Equilibrio_M = int(input('Ingresar el paso a partir del cual la simulación entró en equilibrio: '))
#--------------------------------------------------------------------------------------------------
# # c) Reduzca las fluctuaciones haciendo varias ejecuciones de la simulación para el mismo valor de temperatura y haciendo un promedio entre ellas para determinar el valor de energía y magnetización.
#--------------------------------------------------------------------------------------------------
# Se inicializa la variable que rige la cantidad de veces que se llamará a la 
# función ModeloIsing1d con el fin de suavizar las energías y las magnetizaciones
ejecuciones = 10
#--------------------------------------------------------------------------------------------------
def SuavizaEnergias(ejecuciones, temperatura, nPasos):
    '''
    -------
    Calcula el promedio de energía para cada nPaso a lo largo de 
    las ejecuciones que se indiquen.
    ejecuciones: cantidad de veces que se ejecutará un llamado a la función: ModeloIsing1d esto con el fin de suavizar.
    temperatura: temperatura fija del baño térmico con la que se trabajará la ejecución
    nPasos: cantidad de iteraciones a evolucionar el estado del sistema
    -------
    return: devuelve un arreglo con las energías promediadas (suavizadas) para cada nPaso
    '''
    # Esta matriz contendrá todos arreglos de energía dependiendo del paso y la ejecución.
    matriz_Estados_Energeticos = []
    # Este ciclo, construye la matriz a promediar
    for i in range(ejecuciones):
        energias_i = ModeloIsing1d(temperatura, nPasos, estado_inicial)[0]
        matriz_Estados_Energeticos.append(energias_i)
    # Se aplica la transpuesta para iterar más facil el promedio
    matriz_Estados_Energeticos_Transpuesta = np.array(matriz_Estados_Energeticos).T 
    
    # Este ciclo promedia entre los valores de energía en 
    # cada nPaso (filas) y cada ejecución (columnas) de: matriz_Estados_Energeticos
    promedios_energias = []
    for i in range(nPasos):
        energia_i_prom = np.mean(matriz_Estados_Energeticos_Transpuesta[i])
        promedios_energias.append(energia_i_prom)
        
    return promedios_energias
grafica_Energia_Suavizada = SuavizaEnergias(ejecuciones, temperatura_const, nPasos)
energia_media = np.mean(grafica_Energia_Suavizada[paso_Equilibrio_T:])
#--------------------------------------------------------------------------------------------------
# Gráfico
fig, ax = plt.subplots(figsize = (4,4), dpi = 100)
ax.plot(grafica_Energia_Suavizada, color = 'gold')
plt.axhline(energia_media, 0, 1, label='Energía promedio: {}'.format(round(energia_media,2)))
ax.set_title('Simulación modelo Ising en 1-D a una kBT = {}; {} ejecuciones y los espines: {}'.format(temperatura_const, ejecuciones, estado_inicial))
ax.set_xlabel('Pasos')
ax.set_ylabel('Promedio energías')
plt.legend(loc = 'lower right')
plt.show()
#--------------------------------------------------------------------------------------------------
def SuavizaMagnetizacion(ejecuciones, temperatura, nPasos):
    '''
    -------
    Calcula el promedio de la magnetización para cada nPaso a lo largo de 
    las ejecuciones que se indiquen.
    ejecuciones: cantidad de veces que se ejecutará un llamado a la función: Modelo_Ising_1d
    temperatura: temperatura fija del baño térmico con la que se trabajará la ejecución
    nPasos: cantidad de iteraciones a evolucionar el estado del sistema
    -------
    return: devuelve un arreglo con las magnetizaciones promediadas para cada nPaso
    '''
    # Esta matriz contendrá todos arreglos de magnetización dependiendo del nPaso y de la ejecución.
    matriz_Estados_Magnetizados = []
    # Este ciclo, construye la matriz a promediar
    for i in range(ejecuciones):
        magnetizaciones_i = ModeloIsing1d(temperatura, nPasos, estado_inicial)[1]
        matriz_Estados_Magnetizados.append(magnetizaciones_i)
    # Se aplica la transpuesta para iterar más facil el promedio
    matriz_Estados_Magnetizados_Transpuesta = np.array(matriz_Estados_Magnetizados).T

    # Este ciclo promedia entre los valores de magnetización en 
    # cada nPaso (filas) y cada ejecución (columnas) de: matriz_Estados_Magnetizados
    promedios_magnetizaciones = []
    for i in range(nPasos):
        magnetizaciones_i_prom = np.mean(matriz_Estados_Magnetizados_Transpuesta[i])
        promedios_magnetizaciones.append(magnetizaciones_i_prom)
    return promedios_magnetizaciones
grafica_Magne_Suavizada = SuavizaMagnetizacion(ejecuciones, temperatura_const, nPasos)
magnetizacion_media = np.mean(grafica_Magne_Suavizada[paso_Equilibrio_M:])
#--------------------------------------------------------------------------------------------------
# Gráfico
fig, ax = plt.subplots(figsize = (4,4), dpi = 100)
ax.plot(grafica_Magne_Suavizada, color = 'magenta')
plt.axhline(magnetizacion_media, 0, 1, label='Magnetización promedio: {}'.format(round(magnetizacion_media,2)))
ax.set_title('Simulación modelo Ising en 1-D a una kBT = {}, {} ejecuciones y los espines: {}'.format(temperatura_const, ejecuciones, estado_inicial))
ax.set_xlabel('Pasos')
ax.set_ylabel('Promedio magnetizaciones')
plt.legend(loc = 'lower right')
plt.show()
#--------------------------------------------------------------------------------------------------
# # e) Grafique la energía interna U para 0 < kBT < 5. Obtenga el gráfico U en función de kBT correspondiente. Compare con las soluciones analíticas presentadas en  15.3.1. del [Landau, 2011].
def CalculoUEnergiaInterna(arreglo_energias_suavizadas):
    '''
    --------
    Calcula el valor de la energía interna U = <E>
    arreglo_energias_suavizadas: es el arreglo de energías suavizado (promediadas)
    --------
    return: devuelve valor flotante: U = <E>
    '''
    # Se tomarán solo los valores a partir de donde se piensa que se entra en equilibrio
    energia_interna = np.mean(arreglo_energias_suavizadas[paso_Equilibrio_T:])
    return energia_interna
#--------------------------------------------------------------------------------------------------
# Se inicializa la variable que contiene el valor de los puntos a graficar
# las energías, magnetizaciones y calores específicos.
puntos_T_graficar = 20
#--------------------------------------------------------------------------------------------------
# Se crea al dominio de las temperaturas a utilizar [0.1, 5]
valoresT = np.linspace(0.1, 5, puntos_T_graficar)
#--------------------------------------------------------------------------------------------------
# Generación del arreglo que contendrá a la energía interna a graficar.
grafica_U = []
for temperatura in valoresT:
    # energia_U = CalculoUenergiainterna(SuavizaEnergias(ejecuciones, temperatura, nPasos))
    energia_U = CalculoUEnergiaInterna(SuavizaEnergias(ejecuciones, temperatura, nPasos))
    grafica_U.append(energia_U)
#--------------------------------------------------------------------------------------------------
# Gráfico de la energía interna en función de kT
fig, ax = plt.subplots(figsize = (4,4), dpi = 100)
ax.plot(valoresT, grafica_U,marker= '+', color = 'r', label = 'U(T) = <E(T)>')
ax.set_title('Energía interna de modelo de Ising en 1-D')
ax.set_xlabel(r'$k_{B}T$')
ax.set_ylabel(r'$U(k_{B}T)$')
ax.legend(loc = 'upper left')
ax.grid(True)
plt.show()
#--------------------------------------------------------------------------------------------------
# Se inicializan las constantes que son importantes para la graficación de las propiedades termodinámicas.
J = 1 # constante de cambio
nEspines = 100
kBoltzmann = 1
#--------------------------------------------------------------------------------------------------
# Gráfica analítica y simulada.
# Se define la energía interna analitica.
U_analítica = - nEspines * J * np.tanh(J/(kBoltzmann*valoresT))
# Gráfico
fig, ax = plt.subplots(figsize = (4,4), dpi = 100)
ax.plot(valoresT, U_analítica,marker ='o', color = 'g', label = 'Analítica')
ax.plot(valoresT, grafica_U,marker = '+', color = 'r', label = 'Simulación Ising 1-D')
ax.set_title('Energía interna analítica y simulada del modelo de Ising en 1-D')
ax.set_xlabel(r'$k_{B}T$')
ax.set_ylabel(r'$U(k_{B}T)$')
ax.legend(loc = 'lower right')
ax.grid(True)
plt.show()
#--------------------------------------------------------------------------------------------------
# # f) Grafique la magnetización M para 0 < kBT < 5. Obtenga el gráfico M en función de kBT correspondiente. Compare con los resultados analíticos.
def CalculoMagnetizacionPromedio(arreglo_magne_suavizadas):
    '''
    --------
    Calcula el valor de la magnetización M = <M_arreglo> 
    arreglo_magne_suavizadas: es el arreglo de magnetizaciones suavizadas (promediadas)
    --------
    return: devuelve el valor flotante: M_promedio, que representa la magnetización promedio en el equilibrio.
    '''
    # Se tomarán solo los valores a partir de donde se piensa que se entra en equilibrio
    # En este paso es donde se toma en cuenta el valor absoluto de la magnetización.
    magne_suavizadas_absolutas = np.abs(arreglo_magne_suavizadas[paso_Equilibrio_M:])
    magne_promedio = np.mean(magne_suavizadas_absolutas)
    return magne_promedio
#--------------------------------------------------------------------------------------------------
# Generación del arreglo que contendrá a la magnetización a graficar.
grafica_M = []
for temperatura in valoresT:
    magnetizacion_M = CalculoMagnetizacionPromedio(SuavizaMagnetizacion(ejecuciones, temperatura, nPasos))
    grafica_M.append(magnetizacion_M)
#--------------------------------------------------------------------------------------------------
# Gráfica de la magnetización en función de kBT
fig, ax = plt.subplots(figsize = (4,4), dpi = 100)
ax.plot(valoresT, grafica_M, marker = '+', color = 'magenta', label = 'Magnetización')
ax.set_title('Magnetización de modelo de Ising en 1-D')
ax.set_xlabel(r'$k_{B}T$')
ax.set_ylabel('M(T)')
ax.legend(loc = 'upper right')
ax.grid(True)
plt.show()
#--------------------------------------------------------------------------------------------------
# Gráfica analítica
# Se define el valor del campo magnético.
B = 0.03
# Se define la magnetización analítica 
M_analítica = (nEspines*np.exp(J/(kBoltzmann*valoresT))*np.sinh(B/(kBoltzmann*valoresT))) / np.sqrt(np.exp((2*J)/(kBoltzmann*valoresT)) * (np.sinh(B/(kBoltzmann*valoresT)))**2 + np.exp((-2*J)/(kBoltzmann*valoresT)))
# Gráfico
fig, ax = plt.subplots(figsize = (4,4), dpi = 100)
ax.plot(valoresT, M_analítica, marker = 'o', color = 'darkviolet', label = 'Analítica')
ax.plot(valoresT, grafica_M, marker = '+', color = 'magenta', label = 'Simulación Ising 1-D')
ax.set_title('Magnetización analítica del modelo de Ising en 1-D')
ax.set_xlabel(r'$k_{B}T$')
ax.set_ylabel('M(T)')
ax.legend(loc = 'upper right')
ax.grid(True)
plt.show()
#--------------------------------------------------------------------------------------------------
# # g) Compute las fluctuaciones de la energía U_2 y el calor específico C para 0 < kBT < 5. Obtenga el gráfico C en función de kBT correspondiente. Compare los resultados de su simulación con los resultados analíticos.
def CalculoUEnergiaInternaSinSuavizar(temperatura, nPasos):
    '''
    --------
    Calcula el valor de la energía interna U = <E>
    temperatura: temperatura fija del baño térmico con la que se trabajará la ejecución
    nPasos: cantidad de iteraciones a evolucionar el estado del sistema
    --------
    return: devuelve el valor flotante U = <E>
    '''
    # Se tomarán solo los valores a partir de donde se piensa que se entra en equilibrio
    energias = ModeloIsing1d(temperatura, nPasos, estado_inicial)[0]
    # Se calcula el promedio de energias al cuadrado para cada configuración de espines a cada temperatura
    energia_interna_sin_suavizar = np.mean(energias[paso_Equilibrio_T:])
    return energia_interna_sin_suavizar
#--------------------------------------------------------------------------------------------------
# Primero se debe computar el valor de U (sin suavizar) vs kT
grafica_U_sin_suavi = []
for temperatura in valoresT:
    energia_U_sin_suavi = CalculoUEnergiaInternaSinSuavizar(temperatura, nPasos)
    grafica_U_sin_suavi.append(energia_U_sin_suavi)
#--------------------------------------------------------------------------------------------------
def CalculoUEnergiaInterna2(temperatura, nPasos):
    '''
    --------
    Calcula el valor de la energía interna U_2 = <E^2>
    temperatura: temperatura fija del baño térmico con la que se trabajará la ejecución
    nPasos: cantidad de iteraciones a evolucionar el estado del sistema
    --------
    return: devuelve el valor flotante U_2 = <E^2>
    '''
    # Se tomarán solo los valores a partir de donde se piensa que se entra en equilibrio
    energias = ModeloIsing1d(temperatura, nPasos, estado_inicial)[0]
    # Se elevan al cuadrado cada uno de los elementos de la lista.
    energias_cuad = np.power(energias,2)
    # Se calcula el promedio de energias al cuadrado para cada configuración de espines a cada temperatura
    # energia_interna_2 = np.median(energias_cuad[2000:])
    energia_interna_2 = np.mean(energias_cuad[paso_Equilibrio_T:])
    return energia_interna_2
#--------------------------------------------------------------------------------------------------
# Segundo se debe computar el valor de U_2 vs kT
grafica_U_2 = []
for temperatura in valoresT:
    energia_U_2 = CalculoUEnergiaInterna2(temperatura, nPasos)
    grafica_U_2.append(energia_U_2)
#--------------------------------------------------------------------------------------------------
# Gráfico
fig, ax = plt.subplots(figsize = (4,4), dpi = 100)
ax.plot(valoresT, grafica_U_2, color = 'olivedrab', label = r'$U_{2}(T) = <E^{2}(T)>$')
ax.set_title('Promedios de los cuadrados de la energía en el Modelo de Ising en 1-D')
ax.set_xlabel(r'$k_{B}T$')
ax.set_ylabel(r'$U_{2}(k_{B}T)$')
ax.legend(loc = 'upper right')
plt.show()
#--------------------------------------------------------------------------------------------------
# Grafica de la comparación entre U_2 y (U)^2
# Se extraen los valores de las gráficas
energia_int = grafica_U_sin_suavi
energia_int_2 = grafica_U_2

fig, ax = plt.subplots(figsize = (4,4), dpi = 100)
ax.plot(valoresT, np.power(energia_int, 2), color = 'g', label = r'$<E>^2$')
ax.plot(valoresT, energia_int_2, color = 'crimson', label = r'$<E^2>$')
ax.set_title(r'$Comparación\:de\:(U)^2\:y\:U_{2}\:en\:Ising\:1-D$')
ax.set_xlabel(r'$k_{B}T$')
ax.set_ylabel(r'$U$')
ax.legend(loc = 'upper right')
plt.show()
#--------------------------------------------------------------------------------------------------
# Computo y graficación del valor del calor específico
grafica_C_especifico = []

# Ahora se construye el arreglo que contiene a los calores específicos
for i in range(len(valoresT)):
    calor_esp_i = np.abs((1/(nEspines**2)) * ((energia_int_2[i] - energia_int[i]**2)/(kBoltzmann*valoresT[i]**2)))
    grafica_C_especifico.append(calor_esp_i)
#--------------------------------------------------------------------------------------------------
# Graficación del calor específico simulado

fig, ax = plt.subplots(figsize = (4,4), dpi = 100)
ax.plot(valoresT, grafica_C_especifico, color = 'crimson', label = r'$C(T) = \frac{1}{N^2}\frac{U_{2}-U^2}{k_{B}T^2}$')
ax.set_title('Calor específico del modelo de Ising en 1-D')
ax.set_xlabel(r'$k_{B}T$')
ax.set_ylabel(r'$C(k_{B}T)$')
ax.legend(loc = 'upper right')
plt.show()
#--------------------------------------------------------------------------------------------------
# Gráfica analítica
C_analitica = (J/(kBoltzmann*valoresT))**2 /(np.cosh(J/(kBoltzmann*valoresT)))**2

# Gráfico
fig, ax = plt.subplots(figsize = (4,4), dpi = 100)
ax.plot(valoresT, C_analitica, color = 'darkorange', label = 'Analítica')
ax.plot(valoresT, grafica_C_especifico, color = 'crimson', label = 'Simulación')
ax.set_title('Calor específico analítico y simulado del modelo de Ising en 1-D')
ax.set_xlabel(r'$k_{B}T$')
ax.set_ylabel(r'$C(k_{B}T)$')
ax.legend(loc = 'upper right')
plt.show()
#--------------------------------------------------------------------------------------------------
# Fin Tarea.