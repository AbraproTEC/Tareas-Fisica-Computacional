import numpy as np
import random as ran
import matplotlib.pylab as plt

# Inicializando Variables

numero_pasos = 20000
numero_particulas = 100
x_coor = []
y_coor = []
raiz_cua_particulas = int(numero_particulas ** 0.5)
div_eje = 10
x_bordes = np.linspace(0, 100, div_eje + 1)
y_bordes = np.linspace(0, 100, div_eje + 1)
s_mat = []


# Definiendo Funciones

def vecino():
    selector = ran.randint(0, 100)
    x_paso = 0
    y_paso = 0
    if selector < 25:
        x_paso = 1
    elif selector < 50:
        x_paso = -1
    elif selector < 75:
        y_paso = 1
    elif selector < 100:
        y_paso = -1
    return ([x_paso, y_paso])


def paso(particulas):
    x_pasos = []
    y_pasos = []
    for a in range(particulas):
        x, y = vecino()
        x_pasos.append(x)
        y_pasos.append(y)
    return ([x_pasos, y_pasos])


# PRINCIPAL

for a in range(raiz_cua_particulas):
    x = 45 + a
    y = 45
    for b in range(raiz_cua_particulas):
        y = y + 1
        y_coor.append(y)
        x_coor.append(x)

x_matcoor = [x_coor]
y_matcoor = [y_coor]

if numero_pasos == 0:
    plt.plot(x_coor, y_coor, '.')
    plt.title(str(numero_particulas) + ' partículas de crema en el café' + ' en ' + str(numero_pasos) + ' pasos')
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.show()
else:

    for a in range(numero_pasos):

        x_pasos, y_pasos = paso(numero_particulas)
        x_serv = []
        y_serv = []

        for b in range(numero_particulas):
            x_serv.append(x_pasos[b] + x_coor[b])
            y_serv.append(y_pasos[b] + y_coor[b])
        x_coor = x_serv
        y_coor = y_serv
        x_matcoor = x_matcoor + [x_serv]
        y_matcoor = y_matcoor + [y_serv]

        for c in range(numero_particulas):
            if x_serv[c] > 100:
                x_serv[c] = 100
            elif x_serv[c] < 0:
                x_serv[c] = 0
            elif y_serv[c] > 100:
                y_serv[c] = 100
            elif y_serv[c] < 0:
                y_serv[c] = 0
        s_paso = 0

        h = np.histogram2d(x_serv, y_serv, bins=(x_bordes, y_bordes))
        p = h[0] / numero_particulas
        for d in range(div_eje):
            for e in range(div_eje):
                if p[d][e] > 0:
                    s_paso = s_paso - p[d][e] * np.log(p[d][e])
        s_mat.append(s_paso)


plt.subplot(1, 2, 1)
plt.plot(x_serv, y_serv, '.')
plt.title(str(numero_particulas) + ' partículas de crema en el café' + ' en ' + str(numero_pasos) + ' pasos')
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.gca().axes.get_yaxis().set_visible(False)
plt.gca().axes.get_xaxis().set_visible(False)

plt.subplot(1, 2, 2)
plt.plot(s_mat, '.')
plt.ylim(0, 5)
plt.xlim(0, 20000)
plt.title('Evolución de la entropía del sistema')
plt.ylabel('Entropía')
plt.xlabel('Tiempo(pasos)')
plt.show()