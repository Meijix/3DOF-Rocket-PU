#Caso 2: Gravedad + Arrastre cuadratico y masa cte

import numpy as np
import matplotlib.pyplot as plt
#from scipy.integrate import odeint
from IntegradoresCasos import *
from FunSimularDinamica import *

def der_gravedad_arrastre(t, state):
    v = state[1]
    if v == 0:
        Drag = 0
    else:
        Drag = (D_mag/m) * (v**2) * np.sign(v)
    
    derivs = np.array((v, -g - Drag))
    #print(derivs)
    return derivs
import numpy as np

def sol_analitica_gravedad_arrastre(state, t, m, g, D_mag):
    z0= state[0]
    v0= state[1]
    k = np.sqrt(g * D_mag / m)
    
    v = (v0 + (g / k)) * np.exp(-k * t) - (g / k)
    z = z0 + (v0 + (g / k)) * (1 - np.exp(-k * t)) / k - g * t / k
    
    return z, v

'''

#Calcular y graficar el error numerico
#error en metros
error_pos = [pos_simul[i] - pos_analitica[i] for i in range(len(tiempos))]
error_vel = [vel_simul[i] - vel_analitica[i] for i in range(len(tiempos))]

#error relativo
error_pos_rel = [abs(error_pos[i]/pos_analitica[i]) for i in range(len(tiempos))]
error_vel_rel = [abs(error_vel[i]/vel_analitica[i]) for i in range(len(tiempos))]

plt.figure(figsize=(8, 6))
plt.plot(tiempos, error_pos, label='Error z(t)')
plt.plot(tiempos, error_vel, label='Error v(t)')
plt.title("Error absoluto")
plt.xlabel('Tiempo [s]')
plt.ylabel('Errorres absolutos [m],[m/s]')
plt.legend()

plt.figure(figsize=(8, 6))
plt.plot(tiempos, error_pos_rel, label='Error z(t)')
plt.plot(tiempos, error_vel_rel, label='Error v(t)')
plt.title("Error relativo")
plt.xlabel('Tiempo [s]')
plt.ylabel('Errores relativos')
plt.legend()

plt.show()


##############################
# Simulación con scipy
##############################
from scipy.integrate import odeint

def simular_dinamica_scipy(estado, t_max, dt):
    t = np.arange(0, t_max, dt)
    sol = odeint(der_gravedad_arrastre, estado, t)
    return t, sol

# ...

# Simulación con scipy
t_scipy, sol_scipy = simular_dinamica_scipy(estado, t_max, dt)

pos_scipy = sol_scipy[:, 0]
vel_scipy = sol_scipy[:, 1]

# Graficar resultados
plt.figure(figsize=(8, 6))
plt.plot(t_scipy, pos_scipy, label='Scipy')
plt.plot(tiempos, pos_analitica, label='Analítica')
plt.plot(tiempos, pos_simul, label='Simulación')
plt.title('Posición vertical [m/s]')
plt.xlabel('Tiempo [s]')
plt.ylabel('Posición [m]')
plt.legend()

plt.figure(figsize=(8, 6))
plt.plot(t_scipy, vel_scipy, label='Scipy')
plt.plot(tiempos, vel_analitica, label='Analítica')
plt.plot(tiempos, vel_simul, label='Simulación')
plt.title('Velocidad vertical [m/s]')
plt.xlabel('Tiempo [s]')
plt.ylabel('Velocidad [m/s]')
plt.legend()

plt.show()

'''
##############################################################################
#Comparacion integradores
# Listas para guardar los resultados
tiempos_euler = []
pos_euler = []
vel_euler = []

tiempos_rk4 = []
pos_rk4 = []
vel_rk4 = []

tiempos_rkf45 = []
pos_rkf45 = []
vel_rkf45 = []

# Estado inicial
z0 = 0
v0 = 100
estado = np.array([z0, v0])

#no afecta la masa la dinamica
m = 5.0 #masa cte
g = 9.81 #Aceleracion de gravedad cte
rho = 1.225
A = 1
cd = 0.45
D_mag = 0.5 * cd * A * rho

# Parametros de la simulacion
dt = 0.1
t_max = 80

# Simulaciones numericas con diferentes integradores
integradores = [Euler, RungeKutta4, RungeKutta2]#, RKF45]
labels = ['Euler', 'RK4', 'RK2'] #, 'RKF45']

for integrador, label in zip(integradores, labels):
    tiempos, sim = simular_dinamica(estado, t_max, dt, integrador, der_gravedad_arrastre)
    pos = [sim[i][0] for i in range(len(sim))]
    vel = [sim[i][1] for i in range(len(sim))]
    
    if label == 'Euler':
        tiempos_euler = tiempos
        pos_euler = pos
        vel_euler = vel
    elif label == 'RK4':
        tiempos_rk4 = tiempos
        pos_rk4 = pos
        vel_rk4 = vel
    elif label =='RK2':
        tiempos_rk2 = tiempos
        pos_rk2 = pos
        vel_rk2 = vel
    elif label == 'RKF45':
        tiempos_rkf45 = tiempos
        pos_rkf45 = pos
        vel_rkf45 = vel

divisiones = t_max+1


#Solucion analitica
pos_analitica = []
vel_analitica = []

#la solucion analitica se calcula para los tiempos de Euler
for t in tiempos_euler:
    pos, vel = sol_analitica_gravedad_arrastre(estado, t, m, g, D_mag)
    pos_analitica.append(pos)
    vel_analitica.append(vel)

#print(pos_analitica, pos_simul)
#print(vel_analitica, vel_simul)
#print(tiempos)




opacidad=1
# Graficar resultados
plt.figure(figsize=(8, 6))
#Checar el tamano de la solcion analitica?
plt.plot(tiempos_euler, pos_analitica, label='Analitica', ls='-', alpha=opacidad)
plt.plot(tiempos_euler, pos_euler, label='Euler',marker ='o', alpha=opacidad)
plt.plot(tiempos_rk4, pos_rk4, label='RK4', marker='*', alpha= opacidad)
plt.plot(tiempos_rk2, pos_rk2, label='RK2', linestyle='dashed', alpha=opacidad) #marker ='v', alpha= opacidad)
plt.plot(tiempos_rkf45, pos_rkf45, label='RKF45', marker='X',alpha=opacidad)
plt.title('Posición vertical [m]')
plt.xlabel('Tiempo [s]')
plt.ylabel('Posición [m]')
plt.legend()

plt.figure(figsize=(8, 6))
plt.plot(tiempos_euler, vel_analitica, label='Analitica', ls='-', alpha = opacidad)
plt.plot(tiempos_euler, vel_euler, label='Euler', marker='o', alpha= opacidad)
plt.plot(tiempos_rk4, vel_rk4, label='RK4', marker='*', alpha=opacidad)
plt.plot(tiempos_rk2, vel_rk2, label='RK2', linestyle='dashed', alpha=opacidad) 
plt.plot(tiempos_rkf45, vel_rkf45, label='RKF45',marker='X', alpha=opacidad)
plt.title('Velocidad vertical [m/s]')
plt.xlabel('Tiempo [s]')
plt.ylabel('Velocidad [m/s]')
plt.legend()

plt.show()
