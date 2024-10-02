import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from funciones import *
from dibujarCohete import dibujar_cohete

# Leer los datos de la simulación desde el archivo CSV
datos_simulacion = pd.read_csv('datos_simulacion.csv')

# Extraer los datos del CSV
(tiempos, posiciones, velocidades, thetas, omegas, CPs, CGs, masavuelo, estabilidad,
 viento_vuelo_mags, viento_vuelo_dirs, viento_vuelo_vecs, wind_xs, wind_ys, wind_zs,
 Dmags, Nmags, Tmags, Dxs, Dys, Dzs, Nxs, Nys, Nzs, Txs, Tys, Tzs, Tvecs, Dvecs, Nvecs,
 accels, palancas, accangs, Gammas, Alphas, torcas, Cds, Machs) = extraer_datoscsv(datos_simulacion)

# Leer los datos de la simulación desde el archivo JSON
with open('datos_simulacion.json', 'r') as f:
    datos = json.load(f)

# Extraer los datos del JSON
(d_ext, t_MECO, tiempo_salida_riel, tiempo_apogeo, tiempo_impacto,
    max_altitude, max_speed, max_acceleration_linear, max_acceleration_angular) = extraer_datosjson(datos)

# Configuración inicial
t = tiempos[:]
t_fin = tiempos[-1]
tamaño = 10

# Crear figura y ejes
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(121)
ax2d = fig.add_subplot(122)

# Configurar el gráfico del cohete
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect("equal")
ax.set_title('Dibujo del Cohete')

# Eje 2D para la visualización
ax2d.set_xlim([0, t_fin + 10])
ax2d.set_ylim([-15, 15])
ax2d.set_title('Ángulos del Cohete')
ax2d.set_xlabel("Tiempo (s)")
ax2d.set_ylabel("Grados")
ax2d.grid()

# Cada cuántos frames graficar
every = 100

# Función de actualización para la animación
def update(frame):
    
    dibujar_cohete(0, 0, thetas[frame], tamaño)  # Dibujar el cohete inclinado
    #ax.set_xlim(-10, 10)
    #ax.set_ylim(-10, 10)
    ax.set_aspect("equal")
    ax.set_title('Dibujo del Cohete')

    
    ax2d.set_xlim([0, t_fin + 1])
    ax2d.set_ylim([-1.8,1.8])
    ax2d.plot(t[:frame + 1], thetas[:frame + 1], 'b-')  # Graficar hasta el frame actual
    ax2d.scatter(t[frame], thetas[frame], color='red')  # Puntos en el gráfico

    return ax, ax2d

# Crear la animación
frames = np.arange(0, len(t), every)
animation = FuncAnimation(fig, update, frames=frames, interval=50, repeat=False)

plt.show()

# Guardar la animación como GIF
animation.save("AngulosAnimados.gif")
print("GIF Guardado")
