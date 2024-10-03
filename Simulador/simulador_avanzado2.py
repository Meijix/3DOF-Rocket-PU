import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import json
from math import pi
import time
from datetime import datetime

# Import necessary modules
from condiciones_init import *
from Xitle import *
from Vuelo import *
from Viento import Viento
from riel import Torrelanzamiento
from Atmosfera1 import atmosfera
from Componentes import Componente, Cono, Cilindro, Aletas, Boattail

class SimuladorCohetesAvanzado:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulador de Cohetes Suborbitales Avanzado")
        self.master.geometry("1200x800")

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both")

        self.create_rocket_tab()
        self.create_input_tab()
        self.create_trajectory_tab()
        self.create_position_tab()
        self.create_forces_tab()
        self.create_angles_tab()
        self.create_stability_tab()
        self.create_wind_tab()
        self.create_summary_tab()
        self.create_csv_import_tab()

        self.rocket = None

    def create_rocket_tab(self):
        rocket_frame = ttk.Frame(self.notebook)
        self.notebook.add(rocket_frame, text="Cohete")

        # Nose Cone
        ttk.Label(rocket_frame, text="Nariz (Cono):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.nose_length = self.create_entry(rocket_frame, 1, "Longitud (m):")
        self.nose_diameter = self.create_entry(rocket_frame, 2, "Diámetro (m):")
        self.nose_geometry = ttk.Combobox(rocket_frame, values=["conica", "ogiva", "parabolica", "eliptica"])
        self.nose_geometry.grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(rocket_frame, text="Geometría:").grid(row=3, column=0, sticky="w", padx=5, pady=5)

        # Body Tube
        ttk.Label(rocket_frame, text="Tubo del cuerpo:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.body_length = self.create_entry(rocket_frame, 5, "Longitud (m):")
        self.body_diameter = self.create_entry(rocket_frame, 6, "Diámetro exterior (m):")
        self.body_thickness = self.create_entry(rocket_frame, 7, "Espesor (m):")

        # Fins
        ttk.Label(rocket_frame, text="Aletas:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.fin_count = self.create_entry(rocket_frame, 9, "Número de aletas:")
        self.fin_span = self.create_entry(rocket_frame, 10, "Envergadura (m):")
        self.fin_root_chord = self.create_entry(rocket_frame, 11, "Cuerda raíz (m):")
        self.fin_tip_chord = self.create_entry(rocket_frame, 12, "Cuerda punta (m):")
        self.fin_sweep = self.create_entry(rocket_frame, 13, "Ángulo de barrido (grados):")

        # Boattail
        ttk.Label(rocket_frame, text="Boattail:").grid(row=14, column=0, sticky="w", padx=5, pady=5)
        self.boattail_length = self.create_entry(rocket_frame, 15, "Longitud (m):")
        self.boattail_front_diameter = self.create_entry(rocket_frame, 16, "Diámetro frontal (m):")
        self.boattail_rear_diameter = self.create_entry(rocket_frame, 17, "Diámetro trasero (m):")

        # Create Rocket button
        self.btn_create_rocket = ttk.Button(rocket_frame, text="Crear Cohete", command=self.create_rocket)
        self.btn_create_rocket.grid(row=18, column=0, columnspan=2, pady=20)

    def create_entry(self, parent, row, label):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=5)
        entry = ttk.Entry(parent)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def create_rocket(self):
        try:
            # Create components
            nose = Cono("Nariz", 1.0, 0.0, float(self.nose_length.get()), float(self.nose_diameter.get()), self.nose_geometry.get())
            body = Cilindro("Tubo", 5.0, float(self.nose_length.get()), float(self.body_length.get()), float(self.body_diameter.get()), float(self.body_diameter.get()) - 2*float(self.body_thickness.get()))
            fins = Aletas("Aletas", 2.0, float(self.nose_length.get()) + float(self.body_length.get()) - float(self.fin_root_chord.get()),
                          float(self.body_diameter.get()), int(self.fin_count.get()), float(self.fin_span.get()),
                          float(self.fin_root_chord.get()), float(self.fin_tip_chord.get()), 0.0, np.deg2rad(float(self.fin_sweep.get())))
            boattail = Boattail("Boattail", 1.0, float(self.nose_length.get()) + float(self.body_length.get()),
                                float(self.boattail_length.get()), float(self.boattail_front_diameter.get()),
                                float(self.boattail_rear_diameter.get()), float(self.body_thickness.get()))

            # Create rocket
            self.rocket = Cohete()
            self.rocket.componentes = {
                "Nariz": nose,
                "Tubo": body,
                "Aletas": fins,
                "Boattail": boattail
            }
            self.rocket.calcular_propiedades()

            messagebox.showinfo("Éxito", "Cohete creado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el cohete: {str(e)}")

    def create_input_tab(self):
        input_frame = ttk.Frame(self.notebook)
        self.notebook.add(input_frame, text="Parámetros de Simulación")

        # Launch site parameters
        ttk.Label(input_frame, text="Parámetros del sitio de lanzamiento").grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(input_frame, text="Latitud:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.latitud = ttk.Entry(input_frame)
        self.latitud.grid(row=1, column=1, padx=5, pady=5)
        self.latitud.insert(0, str(latitud_cord))

        ttk.Label(input_frame, text="Longitud:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.longitud = ttk.Entry(input_frame)
        self.longitud.grid(row=2, column=1, padx=5, pady=5)
        self.longitud.insert(0, str(longitud_cord))

        ttk.Label(input_frame, text="Altitud (m):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.altitud = ttk.Entry(input_frame)
        self.altitud.grid(row=3, column=1, padx=5, pady=5)
        self.altitud.insert(0, str(altitud_cord))

        ttk.Label(input_frame, text="Fecha (YYYY-MM-DD):").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.fecha = ttk.Entry(input_frame)
        self.fecha.grid(row=4, column=1, padx=5, pady=5)
        self.fecha.insert(0, fecha)

        # Launch rail parameters
        ttk.Label(input_frame, text="Parámetros del riel de lanzamiento").grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Label(input_frame, text="Longitud del riel (m):").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.longitud_riel = ttk.Entry(input_frame)
        self.longitud_riel.grid(row=6, column=1, padx=5, pady=5)
        self.longitud_riel.insert(0, str(riel.longitud))

        ttk.Label(input_frame, text="Ángulo del riel (grados):").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.angulo_riel = ttk.Entry(input_frame)
        self.angulo_riel.grid(row=7, column=1, padx=5, pady=5)
        self.angulo_riel.insert(0, str(np.rad2deg(riel.angulo)))

        # Wind parameters
        ttk.Label(input_frame, text="Parámetros del viento").grid(row=8, column=0, columnspan=2, pady=10)

        ttk.Label(input_frame, text="Velocidad base (m/s):").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        self.vel_base_viento = ttk.Entry(input_frame)
        self.vel_base_viento.grid(row=9, column=1, padx=5, pady=5)
        self.vel_base_viento.insert(0, str(viento_actual.vel_base))

        ttk.Label(input_frame, text="Velocidad media (m/s):").grid(row=10, column=0, sticky="w", padx=5, pady=5)
        self.vel_mean_viento = ttk.Entry(input_frame)
        self.vel_mean_viento.grid(row=10, column=1, padx=5, pady=5)
        self.vel_mean_viento.insert(0, str(viento_actual.vel_mean))

        ttk.Label(input_frame, text="Variación de velocidad:").grid(row=11, column=0, sticky="w", padx=5, pady=5)
        self.vel_var_viento = ttk.Entry(input_frame)
        self.vel_var_viento.grid(row=11, column=1, padx=5, pady=5)
        self.vel_var_viento.insert(0, str(viento_actual.vel_var))

        ttk.Label(input_frame, text="Variación de ángulo (grados):").grid(row=12, column=0, sticky="w", padx=5, pady=5)
        self.var_ang_viento = ttk.Entry(input_frame)
        self.var_ang_viento.grid(row=12, column=1, padx=5, pady=5)
        self.var_ang_viento.insert(0, str(viento_actual.var_ang))

        # Simulation parameters
        ttk.Label(input_frame, text="Parámetros de simulación").grid(row=13, column=0, columnspan=2, pady=10)

        ttk.Label(input_frame, text="Tiempo máximo (s):").grid(row=14, column=0, sticky="w", padx=5, pady=5)
        self.t_max = ttk.Entry(input_frame)
        self.t_max.grid(row=14, column=1, padx=5, pady=5)
        self.t_max.insert(0, "800")

        ttk.Label(input_frame, text="Paso de tiempo (s):").grid(row=15, column=0, sticky="w", padx=5, pady=5)
        self.dt = ttk.Entry(input_frame)
        self.dt.grid(row=15, column=1, padx=5, pady=5)
        self.dt.insert(0, "0.01")

        self.btn_simular = ttk.Button(input_frame, text="Simular", command=self.simular)
        self.btn_simular.grid(row=16, column=0, columnspan=2, pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(input_frame, orient="horizontal", length=200, mode="indeterminate")
        self.progress.grid(row=17, column=0, columnspan=2, pady=10)

        self.progress_label = ttk.Label(input_frame, text="")
        self.progress_label.grid(row=18, column=0, columnspan=2)

    def create_trajectory_tab(self):
        self.trajectory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.trajectory_frame, text="Trayectoria 3D")

    def create_position_tab(self):
        self.position_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.position_frame, text="Posición y Velocidad")

    def create_forces_tab(self):
        self.forces_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.forces_frame, text="Fuerzas")

    def create_angles_tab(self):
        self.angles_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.angles_frame, text="Ángulos")

    def create_stability_tab(self):
        self.stability_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stability_frame, text="Estabilidad")

    def create_wind_tab(self):
        self.wind_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.wind_frame, text="Viento")

    def create_summary_tab(self):
        self.summary_frame = tt

k.Frame(self.notebook)
        self.notebook.add(self.summary_frame, text="Resumen")

    def create_csv_import_tab(self):
        self.csv_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.csv_frame, text="Importar CSV")

        ttk.Button(self.csv_frame, text="Importar Curva de Empuje", command=self.import_thrust_curve).pack(pady=10)
        ttk.Button(self.csv_frame, text="Importar Cd vs Mach", command=self.import_cd_vs_mach).pack(pady=10)

        self.thrust_plot_frame = ttk.Frame(self.csv_frame)
        self.thrust_plot_frame.pack(fill=tk.BOTH, expand=True)

        self.cd_plot_frame = ttk.Frame(self.csv_frame)
        self.cd_plot_frame.pack(fill=tk.BOTH, expand=True)

    def import_thrust_curve(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            df = pd.read_csv(file_path)
            self.plot_csv_data(df, self.thrust_plot_frame, "Curva de Empuje", "Tiempo (s)", "Empuje (N)")

    def import_cd_vs_mach(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            df = pd.read_csv(file_path)
            self.plot_csv_data(df, self.cd_plot_frame, "Cd vs Mach", "Mach", "Cd")

    def plot_csv_data(self, df, frame, title, xlabel, ylabel):
        for widget in frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(df.iloc[:, 0], df.iloc[:, 1])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def simular(self):
        if self.rocket is None:
            messagebox.showerror("Error", "Por favor, cree un cohete antes de simular.")
            return

        try:
            # Start progress bar
            self.progress.start()
            self.progress_label.config(text="Simulando...")
            self.master.update()

            # Update launch site parameters
            latitud_cord = float(self.latitud.get())
            longitud_cord = float(self.longitud.get())
            altitud_cord = float(self.altitud.get())
            fecha = self.fecha.get()

            # Update launch rail parameters
            riel.longitud = float(self.longitud_riel.get())
            riel.angulo = np.deg2rad(float(self.angulo_riel.get()))

            # Update wind parameters
            viento_actual.vel_base = float(self.vel_base_viento.get())
            viento_actual.vel_mean = float(self.vel_mean_viento.get())
            viento_actual.vel_var = float(self.vel_var_viento.get())
            viento_actual.var_ang = float(self.var_ang_viento.get())

            # Update simulation parameters
            t_max = float(self.t_max.get())
            dt = float(self.dt.get())

            # Simulation
            inicio = time.time()
            print("Simulando...")

            viento_actual.actualizar_viento3D()
            print("Viento actual", viento_actual.vector)

            vuelo1 = Vuelo(self.rocket, atmosfera_actual, viento_actual)
            tiempos, sim, CPs, CGs, masavuelo, viento_vuelo_mags, viento_vuelo_dirs, viento_vuelo_vecs, Tvecs, Dvecs, Nvecs, accels, palancas, accangs, Gammas, Alphas, torcas, Cds, Machs = vuelo1.simular_vuelo(np.array([0, 0, 0, 0, 0, 0, riel.angulo, 0]), t_max, dt, dt)

            fin = time.time()
            print(f"Tiempo de ejecución: {fin-inicio:.1f}s")

            # Process data
            posiciones = np.array([state[0:3] for state in sim])
            velocidades = np.array([state[3:6] for state in sim])
            thetas = np.array([state[6] for state in sim])
            omegas = np.array([state[7] for state in sim])

            Tmags = np.array([np.linalg.norm(Tvec) for Tvec in Tvecs])
            Dmags = np.array([np.linalg.norm(Dvec) for Dvec in Dvecs])
            Nmags = np.array([np.linalg.norm(Nvec) for Nvec in Nvecs])

            Txs, Tys, Tzs = zip(*Tvecs)
            Dxs, Dys, Dzs = zip(*Dvecs)
            Nxs, Nys, Nzs = zip(*Nvecs)

            wind_xs = [vec[0] for vec in viento_vuelo_vecs]
            wind_ys = [vec[1] for vec in viento_vuelo_vecs]
            wind_zs = [vec[2] for vec in viento_vuelo_vecs]

            stability = [(CP - CG) / self.rocket.d_ext for CP, CG in zip(CPs, CGs)]

            max_altitude = max(posiciones[:, 2])
            max_speed = max(np.linalg.norm(velocidades, axis=1))

            # Update graphs
            self.plot_trajectory(tiempos, posiciones)
            self.plot_position_velocity(tiempos, posiciones, velocidades)
            self.plot_forces(tiempos, Tmags, Dmags, Nmags)
            self.plot_angles(tiempos, thetas, Gammas, Alphas)
            self.plot_stability(tiempos, CPs, CGs, stability)
            self.plot_wind(tiempos, viento_vuelo_mags, viento_vuelo_dirs)
            self.update_summary(vuelo1, max_altitude, max_speed, np.max(accels), np.max(accangs))

            # Save data
            self.save_data(tiempos, posiciones, velocidades, thetas, omegas, CPs, CGs, masavuelo,
                           viento_vuelo_mags, viento_vuelo_dirs, viento_vuelo_vecs, Tmags, Dmags, Nmags,
                           Txs, Tys, Tzs, Dxs, Dys, Dzs, Nxs, Nys, Nzs, accels, palancas, accangs,
                           Gammas, Alphas, torcas, Cds, Machs, stability)

            # Stop progress bar
            self.progress.stop()
            self.progress_label.config(text="Simulación completada")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during simulation: {str(e)}")
            self.progress.stop()
            self.progress_label.config(text="Error en la simulación")

    def plot_trajectory(self, tiempos, posiciones):
        for widget in self.trajectory_frame.winfo_children():
            widget.destroy()

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2])
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Altitud (m)')
        ax.set_title('Trayectoria 3D del Cohete')

        canvas = FigureCanvasTkAgg(fig, master=self.trajectory_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_position_velocity(self, tiempos, posiciones, velocidades):
        for widget in self.position_frame.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

        ax1.plot(tiempos, posiciones[:, 2])
        ax1.set_xlabel('Tiempo (s)')
        ax1.set_ylabel('Altitud (m)')
        ax1.set_title('Altitud vs Tiempo')

        velocidades_mag = np.linalg.norm(velocidades, axis=1)
        ax2.plot(tiempos, velocidades_mag)
        ax2.set_xlabel('Tiempo (s)')
        ax2.set_ylabel('Velocidad (m/s)')
        ax2.set_title('Velocidad vs Tiempo')

        canvas = FigureCanvasTkAgg(fig, master=self.position_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_forces(self, tiempos, Tmags, Dmags, Nmags):
        for widget in self.forces_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(tiempos, Tmags, label='Empuje')
        ax.plot(tiempos, Dmags, label='Arrastre')
        ax.plot(tiempos, Nmags, label='Normal')
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Fuerza (N)')
        ax.set_title('Fuerzas vs Tiempo')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.forces_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_angles(self, tiempos, thetas, Gammas, Alphas):
        for widget in self.angles_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(tiempos, np.rad2deg(thetas), label='Theta')
        ax.plot(tiempos, np.rad2deg(Gammas), label='Gamma')
        ax.plot(tiempos, np.rad2deg(Alphas), label='Alpha')
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Ángulo (grados)')
        ax.set_title('Ángulos vs Tiempo')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.angles_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_stability(self, tiempos, CPs, CGs, stability):
        for widget in self.stability_frame.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

        ax1.plot(tiempos, CPs, label='CP')
        ax1.plot(tiempos, CGs, label='CG')
        ax1.set_xlabel('Tiempo (s)')
        ax1.set_ylabel('Posición (m)')
        ax1.set_title('Centro de Presión y Centro de Gravedad vs Tiempo')
        ax1.legend()

        ax2.plot(tiempos, stability)
        ax2.set_xlabel('Tiempo (s)')
        ax2.set_ylabel('Estabilidad (calibres)')
        ax2.set_title('Estabilidad vs Tiempo')

        canvas = FigureCanvasTkAgg(fig, master=self.stability_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_wind(self, tiempos, viento_vuelo_mags, viento_vuelo_dirs):
        for widget in self.wind_frame.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

        ax1.plot(tiempos, viento_vuelo_mags)
        ax1.set_xlabel('Tiempo (s)')
        ax1.set_ylabel('Velocidad del viento (m/s)')
        ax1.set_title('Magnitud del viento vs Tiempo')

        ax2.plot(tiempos, np.rad2deg(viento_vuelo_dirs))
        ax2.set_xlabel('Tiempo (s)')
        ax2.set_ylabel('Dirección del viento (grados)')
        ax2.set_title('Dirección del viento vs Tiempo')

        canvas = FigureCanvasTkAgg(fig, master=self.wind_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_summary(self, vuelo, max_altitude, max_speed, max_accel_linear, max_accel_angular):
        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        summary_text = f"""
        Resumen de la simulación:

        Diámetro externo del cohete: {self.rocket.d_ext:.2f} m
        Tiempo de MECO: {self.rocket.t_MECO:.2f} s
        Tiempo de salida del riel: {vuelo.tiempo_salida_riel:.2f} s
        Tiempo de apogeo: {vuelo.tiempo_apogeo:.2f} s
        Tiempo de impacto: {vuelo.tiempo_impacto:.2f} s
        Altitud máxima: {max_altitude:.2f} m
        Velocidad máxima: {max_speed:.2f} m/s ({max_speed/340:.2f} Mach)
        Aceleración lineal máxima: {max_accel_linear:.2f} m/s²
        Aceleración angular máxima: {max_accel_angular:.2f} rad/s²
        """

        summary_label = ttk.Label(self.summary_frame, text=summary_text, justify=tk.LEFT)
        summary_label.pack(padx=10, pady=10)

    def save_data(self, tiempos, posiciones, velocidades, thetas, omegas, CPs, CGs, masavuelo,
                  viento_vuelo_mags, viento_vuelo_dirs, viento_vuelo_vecs, Tmags, Dmags, Nmags,
                  Txs, Tys, Tzs, Dxs, Dys, Dzs, Nxs, Nys, Nzs, accels, palancas, accangs,
                  Gammas, Alphas, torcas, Cds, Machs, stability):
        
        # Save data to CSV
        datos_simulados = pd.DataFrame({
            'tiempos': tiempos,
            'posiciones_x': posiciones[:, 0],
            '

posiciones_y': posiciones[:, 1],
            'posiciones_z': posiciones[:, 2],
            'velocidades_x': velocidades[:, 0],
            'velocidades_y': velocidades[:, 1],
            'velocidades_z': velocidades[:, 2],
            'thetas': thetas,
            'omegas': omegas,
            'CPs': CPs,
            'CGs': CGs,
            'masavuelo': masavuelo,
            'viento_vuelo_mags': viento_vuelo_mags,
            'viento_vuelo_dirs': viento_vuelo_dirs,
            'wind_xs': [vec[0] for vec in viento_vuelo_vecs],
            'wind_ys': [vec[1] for vec in viento_vuelo_vecs],
            'wind_zs': [vec[2] for vec in viento_vuelo_vecs],
            'Tmags': Tmags,
            'Dmags': Dmags,
            'Nmags': Nmags,
            'Txs': Txs,
            'Tys': Tys,
            'Tzs': Tzs,
            'Dxs': Dxs,
            'Dys': Dys,
            'Dzs': Dzs,
            'Nxs': Nxs,
            'Nys': Nys,
            'Nzs': Nzs,
            'accels': accels,
            'palancas': palancas,
            'accangs': accangs,
            'Gammas': Gammas,
            'Alphas': Alphas,
            'torcas': torcas,
            'Cds': Cds,
            'Machs': Machs,
            'estabilidad': stability
        })

        datos_simulados.to_csv('datos_simulacion.csv', index=False)

        # Save important data to JSON
        datos_a_guardar = {
            'd_ext': self.rocket.d_ext,
            't_MECO': self.rocket.t_MECO,
            'tiempo_salida_riel': vuelo1.tiempo_salida_riel,
            'tiempo_apogeo': vuelo1.tiempo_apogeo,
            'tiempo_impacto': vuelo1.tiempo_impacto,
            'max_altitude': max(posiciones[:, 2]),
            'max_speed': max(np.linalg.norm(velocidades, axis=1)),
            'max_acceleration_linear': max(accels),
            'max_acceleration_angular': max(accangs)
        }

        with open('datos_simulacion.json', 'w') as f:
            json.dump(datos_a_guardar, f, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorCohetesAvanzado(root)
    root.mainloop()