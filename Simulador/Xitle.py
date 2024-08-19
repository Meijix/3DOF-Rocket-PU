
from condiciones_init import *
from Componentes import *
from cohete import *
from math import *

#Dimensiones principales del cohete
diam_ext = 0.152
espesor = 0.003

#Creación de los componentes individuales

#Componentes externos
nariz = Cono("Nariz", 0.8 , np.array([0.0, 0.0, 0.0]), 0.81, diam_ext, "ogiva")
coples = Cilindro("Coples",1.5, np.array([0.0,0.0, nariz.bottom[2]]),0.176, diam_ext, diam_ext-espesor)
tubo_recup = Cilindro("Tubo recuperación", 2.3, np.array([0.0, 0.0, coples.bottom[2]]), 0.92, diam_ext, diam_ext-espesor)
transfer = Cilindro("Transferidor", 1, np.array([0.0, 0.0, tubo_recup.bottom[2]]), 0.25, diam_ext, diam_ext-espesor)
#tanquelleno = Cilindro("Tanquelleno", 22.0, np.array([0.0, 0.0, fuselaje.bottom[2]]), 1.33, diam_ext, 0)
tanquevacio = Cilindro("Tanquevacio", 8.7, np.array([0.0, 0.0, transfer.bottom[2]]), 1.25, diam_ext, diam_ext-espesor)
#NOX
valvulas = Cilindro("Valvulas", 2.4 , np.array([0.0, 0.0, tanquevacio.bottom[2]]), 0.167, diam_ext, diam_ext-espesor)
#Grano
CC = Cilindro("Camara de Combustión", 4.3, np.array([0.0, 0.0,valvulas.bottom[2]]),0.573,diam_ext, 0.102)

boattail = Boattail("Boattail", 0.251, np.array([0.0, 0.0, CC.bottom[2]]), 0.12, diam_ext, 0.132, espesor)

#Componentes internos
avionica = Cilindro("Aviónica", 1.8, np.array([0.0, 0.0, 0.20]), 0.21, 0.14, 0)
CU = Cilindro("CU", 4.3, np.array([0.0, 0.0, 0.50]), 0.3, 0.14, 0)
drogue = Cilindro("Drogue", 0.6, np.array([0.0, 0.0, 1.0]), 0.17, 0.14, 0)
main = Cilindro("Main", 1.7, np.array([0.0, 0.0, 1.4]), 0.30, 0.14, 0)
aletas= Aletas("Aletas", 1.1, np.array([0.0, 0.0, CC.bottom[2]]), diam_ext, 4, 0.11, 0.3, 0.1, 0.2, 25)

#Combustibles del cohete
oxidante = Cilindro("Oxidante", 12.0, np.array([0.0, 0.0, transfer.bottom[2]]), 1.33, 0.1461, 0)
grano = Cilindro("Grano", 4.0 , np.array([0.0, 0.0, valvulas.bottom[2]]), 0.505 , 0.158, 0.334)

#Lista de componentes y creación del vehículo completo
#Debe ser un diccionario con un nombre corto para cada componente
componentes = {'Nariz': nariz ,'coples': coples,'Tubo recuperación': tubo_recup, 'Transferidor de carga': transfer, 'Aviónica': avionica, 'Carga Útil': CU, 'drogue': drogue,
               'main': main, 'tanquevacio': tanquevacio,
               'oxidante': oxidante, 'valvulas': valvulas, 'grano': grano, 'Cámara Combustión': CC, 'Aletas': aletas, 'Boattail': boattail}

componentes_externos = {'Nariz': nariz ,'coples': coples,'Tubo recuperación': tubo_recup, 'Transferidor de carga': transfer, 'tanquevacio': tanquevacio,
               'oxidante': oxidante, 'valvulas': valvulas, 'grano': grano, 'Cámara Combustión': CC, 'Boattail': boattail}
Xitle = Cohete("Xitle", "hibrido", componentes, componentes_externos)

#print(Xitle)

if __name__ == "__main__":
    #NOTA: en los bottom de todos los componentes tambien se esta sumando la longitud a los ejes x y
    #print(boattail.bottom)
    print("El centro de gravedad es:",Xitle.CG[2], "metros")
    print("El centro de presión es:", Xitle.CP[2], "metros")
    #print(Xitle.CN)
    print("La masa inicial total es:",Xitle.masa, "kg")
    print("El impulso total es:", Xitle.I_total, "N s")