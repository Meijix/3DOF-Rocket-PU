#Simulacion Numerica de los casos simplificados

import numpy as np
import matplotlib.pyplot as plt
#from scipy.integrate import odeint

from Integradores import *

g=9.81 #Aceleracion de gravedad cte

#Caso 1: Gravedad y masa cte
#no aplica parte angular

#no depende de t porque nada es variable
def der_gravedad_masa_cte(t, state):
    z, v = state
    derivs = np.array((v, -g))
    #print(derivs)
    return derivs

def sol_analitica_gravedad_masa_cte(z0, v0, t):
    z = z0 + v0*t -0.5*g*t**2
    v = v0 - g*t
    return z, v

def simular_dinamica(estado, t_max, dt):
    #print(estado)
    t = 0.0
    it = 0
    #########################################
    #CAMBIO DE METODO DE INTEGRACIÓN
    # Integracion = Euler(der_gravedad_masa_cte) #ocupa dt=0.005
    Integracion = RungeKutta4(der_gravedad_masa_cte) #ocupa dt=0.1
    # Integracion = RKF45(der_gravedad_masa_cte)
    #Integracion = RungeKutta2(self.fun_derivs)
    ##########################################
    
    sim=[estado] #lista de estados de vuelo
    tiempos=[0] #lista de tiempos
    while t < t_max:
        #print(t)
        # Integracion numérica del estado actual
        #el dt_new se usa para que el inetgrador actualize el paso de tiempo
        nuevo_estado = Integracion.step(t, estado, dt)
        # nuevo_estado, dt_new = Integracion.step(t, estado, dt, tol=1e-5)
        # print(dt_new)
        # dt = dt_new
        #print(dt_new,dt)
        #print("dt= ", dt)

        # Avanzar estado
        it += 1
        t += dt
        estado = nuevo_estado

        sim.append(estado)
        tiempos.append(t)

        #Indicar el avance en la simulacion
        if it%500==0:
            print(f"Iteracion {it}, t={t:.1f} s, altitud={estado[0]:.1f} m, vel vert={estado[1]:.1f}")
        
        if estado[0] < 0:
            break

    return tiempos, sim



#Solucion de ese caso
# Estado inicial
z0 = 0
v0 = 80

#no afecta la masa la dinamica
#m = 1.0 #masa cte

estado=np.array([z0, v0])
#print(estado)

#Parametros de la simulacion
dt = 0.1 #0.1 #[s]
t_max = 80 #[s]
divisiones = t_max+1

#Simulacion
tiempos, simulacion = simular_dinamica(estado, t_max, dt)

pos_simul = [sim[0] for sim in simulacion]
vel_simul = [sim[1] for sim in simulacion]

#Solucion analitica
pos_analitica = []
vel_analitica = []
for t in tiempos:
    pos, vel = sol_analitica_gravedad_masa_cte(z0, v0, t)
    pos_analitica.append(pos)
    vel_analitica.append(vel)

#Graficar
plt.figure(figsize=(8, 6))
plt.scatter(tiempos, pos_simul, label='Numérica', color="C1")
plt.plot(tiempos, pos_analitica, label='Analitica', ls='-')
plt.title('Posición vertical [m/s]')
plt.xlabel('Tiempo [s]')
plt.ylabel('Posicion [m]')
plt.legend()

plt.figure(figsize=(8, 6))
plt.scatter(tiempos, vel_simul, label="Numérica", color="C1")
plt.plot(tiempos, vel_analitica, label='Analitica', ls='-')
plt.title('Velocidad vertical [m/s]')
plt.xlabel('Tiempo [s]')
plt.ylabel('Velocidad [m/s]')
plt.legend()

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


##############################################################################
#Caso 2: Gravedad y masa variable
