# Curso: Física Aplicada a Biología y Medicina
# Proyecto modelo Hodgkin Huxley
# Profesora: SOFIA COTO GUZMAN
# Estudiantes:
#   - Abraham Alfaro Alvarado
#   - Alonso Jiménez Moya
#   - Kevin Monge Calvo

# Importación de paquetes
import numpy as np
import xlsxwriter
import matplotlib.pyplot as plt
#-----------------------------------------------------------------------------
# Se inicializan las constantes del problema.
gbar_K = 36.0    # (1/mΩ*cm^2)
gbar_Na = 120.0  # (1/mΩ*cm^2)
g_L = 0.3      # (1/mΩ*cm^2)
E_K = -12.0      # (mV)
E_Na = 115.0     # (mV)
E_L = 10.6     # (mV)
C = 1.0          # (μF/cm^2)
#-----------------------------------------------------------------------------
# Se crea una función que inicializa el arreglo que contendrá los tiempos.
def Genera_Tiempo(inicio, fin, cambio):
    '''
    Esta función crea el dominio del tiempo
    return: un arreglo t que contiene los tiempos a evaluar las ecuaciones.
    '''
    contador = inicio
    tiempo = []
    while (contador <= fin):
        tiempo += [contador]
        contador += cambio
    return tiempo
#------------------------------------------------------------------------------
# Se crea una función que genera el estímulo para el modelo
def J_estimulo(dens_corriente):
    '''
    Esta función crea la corriente de estímulo
    return: un arreglo corriente que coniene los estímulos
    '''
    lapso1 = 1000    # (ms)
    lapso2 = 5000   # (ms)
    magnitud_j = dens_corriente # (mA/cm^2) del estímulo
    corriente = np.zeros(10000)
    for i in range(len(corriente)):
        if i <= lapso1:
            corriente[i] = magnitud_j
        elif lapso1 < i <= lapso2:
            corriente[i] = magnitud_j
        else:
            corriente[i] = magnitud_j
    return corriente
#-------------------------------------------------------------
# Gráfica de la corriente de estímulo
t = Genera_Tiempo(0, 100, 0.01)
j = J_estimulo(50)
plt.plot(t, j, color = "g", label='magnitud de la densidad de corriente')
plt.xlabel("tiempo (ms)")
plt.ylabel(r"J $(mA/cm^{2})$")
plt.grid(True)
plt.title("Estímulo para la activación del potencial de membrana")
plt.legend(loc='upper right')
plt.show()
#------------------------------------------------------------
# Se definen las funciones de los coeficientes de las ecuaciones del modelo
def alfa_n(V):
    return 0.01 * ((10 - V) / (np.exp((10 - V) / 10) - 1))
def beta_n(V):
    return 0.125 * np.exp(-V / 80)
def alfa_m(V):
    return 0.1 * ((25 - V) / (np.exp((25 - V) / 10) - 1))
def beta_m(V):
    return 4 * np.exp(-V / 18)
def alfa_h(V):
    return 0.07 * np.exp(-V / 20)
def beta_h(V):
    return 1 / (np.exp((30 - V) / 10) + 1)
#----------------------------------------------------------------
# Se crea una función que ejecuta el modelo Hodgkin Huxley
def Ejecuta_Modelo_Hodkin_Huxley(dens_corriente):
    '''
    Esta función utiliza las ecuaciones del modelo y teoría de Hodgkin Huxley
    y para ejecutar la resolución de ecuaciones diferenciales ordinarias me-
    diante el método de diferencias hacia adelante de Euler.
    param dens_corriente: entra el valor del arreglo de la densidad de corriente
    return: retorna el valor del potencial de acción en función del tiempo.
    '''
    # Se inicializan los valores de las constantes
    an = 0
    bn = 0
    am = 0
    bm = 0
    ah = 0
    bh = 0

    # Se inicia el arreglo que contendrá los valores para el potencial de acción en la membrana.
    potencial_accion = [] # (mV)

    # Se llama a la densidad de corriente de estímulo.
    j_estim = J_estimulo(dens_corriente) # Recordar que es una variable tipo arreglo.

    # Se llama al los valores del timepo
    t_inicio = 0  # (ms)
    t_final = 100 # (ms)
    deltaT = 0.01 # (ms)
    tiempo = Genera_Tiempo(t_inicio, t_final, deltaT) # Recordar que es una variable tipo arrglo

    # Se inicializa una variable que construirá el potencial de acción
    voltajes = [0] # (mV)

    # Se definen las constantes con sus respectivas funciones dependientes de voltaje.
    contador = 0
    # Se definen las constantes con sus respectivas funciones dependientes de voltaje.
    an = alfa_n(voltajes[contador])
    bn = beta_n(voltajes[contador])
    am = alfa_m(voltajes[contador])
    bm = beta_m(voltajes[contador])
    ah = alfa_h(voltajes[contador])
    bh = beta_h(voltajes[contador])
    n = an/(an+bn)
    m = am/(am+bm)
    h = ah/(ah+bh)
    for t in range(len(tiempo)-1):
        an = alfa_n(voltajes[contador])
        bn = beta_n(voltajes[contador])
        am = alfa_m(voltajes[contador])
        bm = beta_m(voltajes[contador])
        ah = alfa_h(voltajes[contador])
        bh = beta_h(voltajes[contador])

        jNa = (m**3) * gbar_Na * h * (voltajes[contador]-E_Na)
        jK = (n**4) * gbar_K * (voltajes[contador]-E_K)
        jF = g_L *(voltajes[contador]-E_L)
        jIon = j_estim[contador] - jNa - jK -jF

    # Para resolver las ecuaciones diferenciales se utiliza el método
    # de diferencias hacia adelante, como se muestra a continuación.
        voltajes += [voltajes[contador] + deltaT*jIon/C]
        n = n + deltaT*(an *(1-n) - bn * n)
        m = m + deltaT*(am *(1-m) - bm * m)
        h = h + deltaT*(ah *(1-h) - bh * h)
        contador += 1

    # Finalmente se construye el potencial de acción
    for voltaje in voltajes:
        potencial_accion += [voltaje-0]   # El - 70 (mV) inidica el potencial de reposo o inicial.
    
    return potencial_accion, tiempo
# Graficación del potencial de acción en funcion del tiempo
Magnitud_densidad_corriente = 50 # (mA/cm^2)
potencial, tiempo = Ejecuta_Modelo_Hodkin_Huxley(Magnitud_densidad_corriente)

for i in range(len(potencial)):
    potencial[i] = potencial[i]-70
plt.plot(tiempo, potencial, color = "r", label=r'Potencial de acción para un estímulo de: '+str(Magnitud_densidad_corriente)+ ' $mA/cm^{2}$')
plt.xlabel("tiempo (ms)")
plt.ylabel("Potencial de membrana (mV)")
plt.grid(True)
plt.ylim(-90,50)
plt.title("Voltaje sobre tiempo en la membrana de una neurona simulada")
plt.axhline(-70, 0, 1, label='Potencial de reposo')
plt.legend(loc='best')
plt.show()
#---------------------------------------------------------------------------------------------------
# Se crea una función que busca la cantidad de puntos máximos relativos de la funcion del potencial
# de acción respecto a un porcentaje del pico máximo
def busqueda_maximos(voltajes, maximo):
    '''
    Calcula la cantidad de picos o potenciales de acción en el
    intervalo de tiempo escogido y en función de las magnitudes
    de los estímulos.
    :param voltajes: arreglo que contiene los valores del potencial de acción en función del tiempo
    :param maximo: el valor en voltaje del pico máximo de la gráfica de potencial de acción.
    :return: devuelve la cantidad de picos máximos en la gráfica de potencial de acción.
    '''

    menor = voltajes[0]
    menor_siguiente = voltajes[0]
    presente = voltajes[0]
    resultado = 0
    for voltaje in voltajes:
        if(menor_siguiente > menor and menor_siguiente > presente):
            if(menor_siguiente >= maximo*0):
                resultado += 1
        menor = menor_siguiente
        menor_siguiente = presente
        presente = voltaje
    return resultado
#-----------------------------------------------------------------------------------------------------
# Se crea una función que crea una hoja de Excel que permite escribir valores de la frecuencia de
# aparición de los potenciales de acción en función de la magnitud del estímulo.
def genera_excel(estimulo, frecuencia):
    '''
    Crea un archivo de Excel con valores de magnitud de estímulo y frecuencia de respuestas de potencial.
    :param estimulo: magnitud del estímulo a análizar (densidad de corriente)
    :param frecuencia: arreglo que contiene a las frecuencias en función del magnitud del estímulo
    :return: Escribe un archivo Excel y verifica la realización con un mensaje en pantella.
    '''

    workbook = xlsxwriter.Workbook('Modelo_Respuesta_de_frecuencias ABRAHAM.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:B', 20)
    worksheet.write('A1', 'Estimulo')
    worksheet.write('B1', 'Frecuencia')
    contador = 1
    while(contador <= len(frecuencia)):
        worksheet.write(contador, 0, estimulo[contador-1])
        worksheet.write(contador, 1, frecuencia[contador-1])
        contador+=1
    workbook.close()
    return print('Creación del Excel completada')
#------------------------------------------------------------------------------------------------
# Se crea una función que genera un bucle de iteración para extraer el valor de frecuencia
# en función de la magnitud del estímulo.
def calculo_de_frecuencias():
    '''
    Hace un llamado a las funciones busqueda_maximos y genera _excel
    :return: Restorna un mensaje en pantalla sobre la realización del excel
    '''

    estimulo = [10]
    frecuencias = []
    contador = 0
    while(contador < 170):
        respuestas_modelo = Ejecuta_Modelo_Hodkin_Huxley(estimulo[contador])
        volt_max = max(respuestas_modelo[0])
        frecuencias += [busqueda_maximos(respuestas_modelo[0], volt_max)]
        estimulo += [estimulo[contador]+1]
        contador += 1
    estimulo = estimulo[:-1]
    plt.plot(estimulo, frecuencias, color = 'g', label='Respuesta de frecuencias')
    plt.xlabel(r"Densidad corriente $(mA/cm^{2})$")
    plt.ylabel("Frecuencia (Pot. Acción/100 ms)")
    plt.grid(True)
    plt.title("Frecuencia de aparición de los potenciales de acción")
    plt.legend(loc='best')
    plt.show()
    #genera_excel(estimulo, frecuencias)
    print('Generación de la gráfica de frecuencia vs magnitud del estímulo completada')

# Ejecusión de la función calculo_de_frecuencias.
calculo_de_frecuencias()








