# Curso: Física Aplicada a Biología y Medicina
# Proyecto: Simulación computacional del movimiento deproyectil no ideal de un balón de futbol
# Profesores: Esteban Pérez Hidalgo / Álvaro Amador Jara
# Estudiantes:
#   - Abraham Alfaro Alvarado
#   - Andrés Camacho Alvarado
#   - Kevin Monge Calvo

# Se importan las bibliotecas
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D
from vpython import *


# Parámetros iniciales
# Condiones geométricas y físicas
g = 9.81 # m/s^2
rapidezInicial = 30.0 # m/s
theta = 45 # grados
phi = 45 # grados
conversion = np.pi/180

# Condiciones del balón
masa = 0.450 # kg
radio = 0.1114 # m
volumenBalon = (4*np.pi/3)*radio**3 # m^3
areaTransversal = np.pi*(radio)**2
densidadAire = 1.225 # kg/m^3
k = 0.5*densidadAire*areaTransversal/masa
coeficienteArrastre = 0.13075 # sin unidades
coeficienteSustentacion = 0.25 # sin unidades

# Condiciones Iniciales
# Movimiento x (Condiciones iniciales)
veloInicialX = rapidezInicial * np.cos(theta * conversion) * np.cos(phi * conversion)
posiInicialX = 0

# Movimiento y (Condiciones iniciales)
veloInicialY = rapidezInicial * np.cos(theta * conversion) * np.sin(phi * conversion)
posiInicialY = 0

# Movimiento z (Condiciones iniciales)
veloInicialZ = rapidezInicial * np.sin(theta * conversion)
posiInicialZ = 0


# Condiciones del viento
# Tomando en cuenta el viento (Varian dependiendo de lo buscado)
veloVientoX = 2 # m/s
veloVientoY = -2 # m/s
veloVientoZ = 1 # m/s

# Velocidades iniciales angulares (Varian dependiendo de lo buscado)
omegax = -1 # rad/s
omegay = 1 # rad/s
omegaz = 0 # rad/s

def SolucionaSistemaEcuaciones(t, M):
    '''
    Retorna los valores de las derivadas de los valores contenidos en el vector M,
    la salida de esta función será utilizada por la función solve_ivp()
    :param t: el arreglo que contiene los valores del tiempo
    :param M: un vector que contiene los valores de las velocidades y posiciones
    para el balón en cada eje coordenado.
    :return: retorna las derivadas de cada uno de los valores (retorna las ecuaciones
    diferenciales que resolverá la función solve_ivp())
    '''
    veloX = M[0]
    posiX = M[1]
    veloY = M[2]
    posiY = M[3]
    veloZ = M[4]
    posiZ = M[5]
    
    # Ecuaciones de movimiento
    velocidad = np.sqrt((veloX - veloVientoX) ** 2 + (veloY - veloVientoY) ** 2 + (veloZ - veloVientoZ) ** 2)
    omega = np.sqrt((omegax)**2 + (omegay)**2 + (omegaz)**2)

    if omega == 0:
        dvx_dt = -k * velocidad * (coeficienteArrastre * (veloX - veloVientoX))
        dx_dt = veloX

        dvy_dt = -k * velocidad * (coeficienteArrastre * (veloY - veloVientoY))
        dy_dt = veloY

        dvz_dt = -g - k * velocidad * (coeficienteArrastre * (veloZ - veloVientoZ)) + densidadAire * volumenBalon * g / masa
        dz_dt = veloZ
    else:
        dvx_dt = -k * velocidad * (coeficienteArrastre * (veloX - veloVientoX) - coeficienteSustentacion * ((omegay * (veloZ - veloVientoZ) - omegaz * (veloY - veloVientoY)) / omega))
        dx_dt = veloX

        dvy_dt = -k * velocidad * (coeficienteArrastre * (veloY - veloVientoY) - coeficienteSustentacion * ((omegaz * (veloX - veloVientoX) - omegax * (veloZ - veloVientoZ)) / omega))
        dy_dt = veloY

        dvz_dt = -g - k * velocidad * (coeficienteArrastre * (veloZ - veloVientoZ) - coeficienteSustentacion * ((omegax * (veloY - veloVientoY) - omegay * (veloX - veloVientoX)) / omega)) + densidadAire * volumenBalon * g / masa
        dz_dt = veloZ

    sistemaEcuaciones = np.array([dvx_dt, dx_dt, dvy_dt, dy_dt, dvz_dt, dz_dt])

    return sistemaEcuaciones


# Inicializando el arreglo que contendrá los tiempos
t_span = np.array([0, 10])
tiempos = np.linspace(t_span[0], t_span[1], 100)

# Creando el arreglo de condiciones iniciales
# Condiciones Iniciales
condicionesIniciales = np.array([veloInicialX, posiInicialX, veloInicialY, posiInicialY, veloInicialZ, posiInicialZ])

# Ejecusión de la función solve_ivp de la biblioteca scipy.integrate
solucion = solve_ivp(SolucionaSistemaEcuaciones , t_span, condicionesIniciales, t_eval=tiempos)

# Extracción de los datos
# Se extraen los datos, se usan solo los valores positivos
t = solucion.t; t_nuevo=[]
vx = solucion.y[0]; vx_nuevo=[]
x = solucion.y[1]; x_nuevo=[]
vy = solucion.y[2]; vy_nuevo=[]
y = solucion.y[3]; y_nuevo=[]
vz = solucion.y[4]; vz_nuevo=[]
z = solucion.y[5]; z_nuevo=[]

for i in range(len(z)):
    if z[i] >= 0:
        y_nuevo.append(y[i])
        t_nuevo.append(t[i])
        vx_nuevo.append(vx[i])
        vy_nuevo.append(vy[i])
        x_nuevo.append(x[i])
        vz_nuevo.append(vz[i])
        z_nuevo.append(z[i])
    else:
        break

t = t_nuevo
vx = vx_nuevo
x = x_nuevo
vy = vy_nuevo
y = y_nuevo
vz = vz_nuevo
z = z_nuevo

# Sección de graficación en 3D
fig = plt.figure(figsize=(6,6))
ax = fig.gca(projection='3d')
lado = 60
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
ax.set_xlim3d(0,lado)
ax.set_ylim3d(0,lado)
ax.set_zlim3d(0,lado)
ax.invert_xaxis()
ax.plot(x, y, z, color = 'g', label = 'Con fricción')
X = np.random.randint(0, lado, (5,5))
Y = np.random.randint(0, lado, (5,5))
Z = np.random.randint(0, lado, (5,5))
ax.quiver(X, Y, Z, veloVientoX, veloVientoY, veloVientoZ, length = 1, arrow_length_ratio = 0.2)
ax.legend(loc='upper left')
ax.invert_xaxis()
plt.show()
#----------------------------Termina el análisis general y empieza la graficación con VPython----------------------------------#
#Sección de graficación con VPython
def GraficoVPython(theta, phi, veloVientoX, veloVientoY, veloVientoZ, omegax, omegay, omegaz):
    '''Función que permite cambiar los parámetros necesarios para la simulación iterativa de varios valores de
    los parámetros ángulo theta, ángulo phi, componentes de la velocidad del viento y componentes del spin.
    Incorpora dentro de sí la función SolucionaSistemaEcuaciones, que es igual a la utilizada en el código original.
    Entradas:
        theta: valor deseado del ángulo theta.
        phi: valor deseado del ángulo phi.
        veloVientoX: valor deseado de la componente en x de la velocidad del viento.
        veloVientoY: valor deseado de la componente en y de la velocidad del viento.
        veloVientoZ: valor deseado de la componente en z de la velocidad del viento.
        omegax: valor deseado de la componente en x del spin.
        omegay: valor deseado de la componente en y del spin.
        omega: valor deseado de la componente en z del spin.
    Salidas:
        x,y,z: arreglos de posición necesarios para la simulación en VPython.'''

    def SolucionaSistemaEcuaciones(t, M):
        '''
        Retorna los valores de las derivadas de los valores contenidos en el vector M,
        la salida de esta función será utilizada por la función solve_ivp()
        :param t: el arreglo que contiene los valores del tiempo
        :param M: un vector que contiene los valores de las velocidades y posiciones
        para el balón en cada eje coordenado.
        :return: retorna las derivadas de cada uno de los valores (retorna las ecuaciones
        diferenciales que resolverá la función solve_ivp())
        '''
        veloX = M[0]
        posiX = M[1]
        veloY = M[2]
        posiY = M[3]
        veloZ = M[4]
        posiZ = M[5]

        # Ecuaciones de movimiento
        velocidad = np.sqrt((veloX - veloVientoX) ** 2 + (veloY - veloVientoY) ** 2 + (veloZ - veloVientoZ) ** 2)
        omega = np.sqrt((omegax) ** 2 + (omegay) ** 2 + (omegaz) ** 2)

        if omega == 0:
            dvx_dt = -k * velocidad * (coeficienteArrastre * (veloX - veloVientoX))
            dx_dt = veloX

            dvy_dt = -k * velocidad * (coeficienteArrastre * (veloY - veloVientoY))
            dy_dt = veloY

            dvz_dt = -g - k * velocidad * (coeficienteArrastre * (veloZ - veloVientoZ)) + densidadAire * volumenBalon * g / masa
            dz_dt = veloZ
        else:
            dvx_dt = -k * velocidad * (coeficienteArrastre * (veloX - veloVientoX) - coeficienteSustentacion * ((omegay * (veloZ - veloVientoZ) - omegaz * (veloY - veloVientoY)) / omega))
            dx_dt = veloX

            dvy_dt = -k * velocidad * (coeficienteArrastre * (veloY - veloVientoY) - coeficienteSustentacion * ((omegaz * (veloX - veloVientoX) - omegax * (veloZ - veloVientoZ)) / omega))
            dy_dt = veloY

            dvz_dt = -g - k * velocidad * (coeficienteArrastre * (veloZ - veloVientoZ) - coeficienteSustentacion * ((omegax * (veloY - veloVientoY) - omegay * (veloX - veloVientoX)) / omega)) + densidadAire * volumenBalon * g / masa
            dz_dt = veloZ

        sistemaEcuaciones = np.array([dvx_dt, dx_dt, dvy_dt, dy_dt, dvz_dt, dz_dt])

        return sistemaEcuaciones

    # Inicializando el arreglo que contendrá los tiempos
    t_span = np.array([0, 10])
    tiempos = np.linspace(t_span[0], t_span[1], 100)

    # Creando el arreglo de condiciones iniciales
    # Condiciones Iniciales
    condicionesIniciales = np.array([veloInicialX, posiInicialX, veloInicialY, posiInicialY, veloInicialZ, posiInicialZ])

    # Ejecusión de la función solve_ivp de la biblioteca scipy.integrate
    solucion = solve_ivp(SolucionaSistemaEcuaciones, t_span, condicionesIniciales, t_eval=tiempos)

    # Extracción de los datos
    # Se extraen los datos, se usan solo los valores positivos
    t = solucion.t;
    t_nuevo = []
    vx = solucion.y[0];
    vx_nuevo = []
    x = solucion.y[1];
    x_nuevo = []
    vy = solucion.y[2];
    vy_nuevo = []
    y = solucion.y[3];
    y_nuevo = []
    vz = solucion.y[4];
    vz_nuevo = []
    z = solucion.y[5];
    z_nuevo = []

    for i in range(len(z)):
        if z[i] >= 0:
            y_nuevo.append(y[i])
            t_nuevo.append(t[i])
            vx_nuevo.append(vx[i])
            vy_nuevo.append(vy[i])
            x_nuevo.append(x[i])
            vz_nuevo.append(vz[i])
            z_nuevo.append(z[i])
        else:
            break

    t = t_nuevo
    vx = vx_nuevo
    x = x_nuevo
    vy = vy_nuevo
    y = y_nuevo
    vz = vz_nuevo
    z = z_nuevo

    return x, y, z

#Graficación en VPython
#Se establece la portería
poste_derecho= box(pos = vector(11,1.22,3.72), lenght = 0.12, height = 2.44, width = 0.12)
poste_izquierdo = box(pos = vector(11,1.22,-3.72), lenght = 0.12, height = 2.44, width = 0.12)
poste_superior = box(pos = vector(11,2.5,0), lenght = 0.12, height = 0.12, width = 7.56)

#Se acomoda la cámara según lo que se desea ver
scene.camera.pos = vector(11,0,0)

#Se itera sobre theta y phi para generar la simulación buscada
for theta in range (0,20,1):
    for phi in range (-20, 20, 1):
        bola = sphere(pos = vector(0,0,0), radius = 0.11, color = color.red, make_trail = True)
        x,y,z = GraficoVPython(theta,phi,0,0,0,0,0,0)
        for i in range(len(z)):
            if bola.pos.x > 11:
                pass
            else:
                sleep(0.01) #Permite que se observe la trayectoria de la pelota.
                bola.pos = vector(x[i],z[i],y[i])
        #scene.waitfor("click")
#-----------------------------------Fin del análisis-------------------------------------------#