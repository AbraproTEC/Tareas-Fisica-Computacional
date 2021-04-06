#CURSO FÍSICA COMPUTACIONAL
#PROFESORES: ESTEBAN PÉREZ / ÁLVARO AMADOR
#ESTUDIANTES: ABRAHAM ALFARO / ANDRÉS CAMACHO
#SEMANA 5: ANÁLISIS DE FOURIER / FFT Y IFFT

#IMPORTACIÓN DE PAQUETES
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fftfreq

#I)------GENERACIÓN DE LA SEÑAL RUIDOSA------#

#a) Parámetros
#a.1) Puntos que deseamos del muestreo
tasa_muestreo = 1024
#a.2) Paso temporal
deltaT = 1
#a.3) Puntos a analizar
nPuntos = deltaT*tasa_muestreo

#b) Universo de puntos para la coordenada temporal
puntos_tiempo = np.linspace(0, deltaT, nPuntos)

#c) Generación de señales individuales con la forma Y(t) = A*sen(2*pi*f*t)
frec_1 = 5 # Hz
Ampli_1 = 10.0
frec_2 = 30 # Hz
Ampli_2 = 20.0
señal_1 = Ampli_1*np.sin(2.0*np.pi*frec_1*puntos_tiempo)
señal_2 = Ampli_2*np.sin(2.0*np.pi*frec_2*puntos_tiempo)

#d) Ruido para la señal
ruido = np.random.normal(0, 20, nPuntos)
señal_pura = señal_1 + señal_2
señal_ruidosa = señal_pura + ruido

#e) Graficación de la señal ruidosa y la pura

fig = plt.figure(figsize =  (12, 5), frameon = False, facecolor = 'yellow')
fig.canvas.set_window_title('Ventana de salida de señales')
fig.suptitle('Señal', fontsize = 15, color = 'red')
plt.plot(puntos_tiempo, señal_ruidosa, label = 'Señal ruidosa')
plt.xlabel('Tiempo (s)', color = 'b')
plt.ylabel('Amplitud', color = 'b')
plt.legend(loc = 'upper right')

plt.show()

# II)------CÁLCULO DE LA TRANSFORMADA DE FOURIER------#

#a) Creación del dominio de la frecuencia
frecuencias = fftfreq(nPuntos, d = 1/tasa_muestreo)

#b) Ignoramos la mitad de los valores, puesto que son los conjugados complejos de los otros
# indices_numeros_positivos = frecuencias > 0

#c) Cálculo de la transformada mediante la FFT
señal_ruidosa_dom_frec = fft(señal_ruidosa)
amplitudes_señal_ruidosa_dom_frec = (2.0/nPuntos) * np.abs(señal_ruidosa_dom_frec)

#d) Graficación de la señal (dominio de la frecuencia)

fig = plt.figure(figsize =  (12, 5), frameon = False, facecolor = 'yellow')
fig.canvas.set_window_title('Ventana de salida de la señal en el dominio de la frecuencia')
fig.suptitle('Señal ruidosa en el dominio de la frecuencia', fontsize = 15, color = 'red')

plt.plot(frecuencias[0:100], amplitudes_señal_ruidosa_dom_frec[0:100], label = 'Valores de la transformada')
plt.xlabel('Frecuencia (Hz)', color = 'magenta')
plt.ylabel('Amplitud', color = 'magenta')
plt.legend(loc = 'upper right')

plt.show()


# III)------Filtración de la señal mediante la función Filtrar_Señal()------#

def FiltrarSeñal(señal_ruidosa, umbral):
    '''
    Esta función toma como parámetros a la señal ruidosa que se quiere filtrar,
    y devuelve dicha señal filtrada dependiendo el umbral de filtración escogido.
    señal_ruidosa: Señal ruidosa que será filtrada
    umbral: Parámetro que indica la amplitud máxima de refencia para el filtrado de la señal
    return: Devuelve la señal filtrada y una gráfica de la misma.
    '''
    # Montaje del arreglo que contendrá a la señal sin ruido (tipo complejo)
    señal_filtrada_dom_frec = np.zeros(len(señal_ruidosa), dtype='complex')
    amplitudes_señal_ruidosa_dom_frec = 2.0 * np.abs(señal_ruidosa / nPuntos)

    # Ciclo que filtra las frecuencias no deseadas
    for i in range(0, len(señal_ruidosa)):
        if amplitudes_señal_ruidosa_dom_frec[i] > umbral:
            señal_filtrada_dom_frec[i] = señal_ruidosa[i]
        else:
            señal_filtrada_dom_frec[i] = señal_filtrada_dom_frec[i]

    # Amplitudes de la señal filtrada en el dominio de la frecuencia
    amplitudes_señal_filtrada_dom_frec = (2.0/ nPuntos) * np.abs(señal_filtrada_dom_frec)

    # Graficación de la señal filtrada en el dominio de la frecuencia

    fig = plt.figure(figsize=(12, 5), frameon=False, facecolor='yellow')
    fig.canvas.set_window_title('Ventana de salida de la señal filtrada en el dominio de la frecuencia')
    fig.suptitle('Señal filtrada en el dominio de la frecuencia', fontsize=15, color='red')
    plt.plot(frecuencias[0:100], amplitudes_señal_filtrada_dom_frec[0:100], label='Valores de la transformada filtrados')
    plt.xlabel('Frecuencia (Hz)', color='magenta')
    plt.ylabel('Amplitud', color='magenta')
    plt.legend(loc='upper right')
    plt.show()

    return (señal_filtrada_dom_frec)

# IV)------CÁLCULO DE LA TRANSFORMADA RÁPIDA INVERSA PARA OBTENER LA
# SEÑAL FILTRADA EN EL DOMINIO DEL TIEMPO------#

#a) Calculo de la transformada inversa a la señal filtrada
umbral = 4.0
señal_filtrada = ifft(FiltrarSeñal(señal_ruidosa_dom_frec, umbral))

#b) Se aplica .real puesto que la ifft devuelve un arreglo de numeros complejos
#donde la parte real es la señal filtrada en el tiempo
señal_filtrada_real = señal_filtrada.real

#c) Graficación de la señal filtrada en el dominio del tiempo

fig = plt.figure(figsize=(12, 5), frameon=False, facecolor='yellow')
fig.canvas.set_window_title('Ventana de salida de la señal filtrada en el dominio del tiempo')
fig.suptitle('Comparacion de señal filtrada y pura en el dominio del tiempo', fontsize=15, color='red')
plt.plot(puntos_tiempo,señal_filtrada_real, label='Valores de la señal filtrada')
plt.plot(puntos_tiempo,señal_pura, label='Valores de la señal pura')
plt.xlabel('Tiempo (s)', color='green')
plt.ylabel('Amplitud', color='green')
plt.legend(loc='upper right')
plt.show()




plt.show()