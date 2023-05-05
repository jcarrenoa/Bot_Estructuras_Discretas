#%%
import numpy as np
import matplotlib.pyplot as plt

class Constelaciones():

    def __init__(self, nombre_archivo) -> None:
        self.__nombre_constelaciones = ["Boyero", "Casiopea", "Cazo", "Cygnet", "Geminis", "Hydra", 
                             "OsaMayor", "OsaMenor"]
        self.__estrellas, self.__dic_estrellas = self.estrellas(nombre_archivo)
        self.__coordenadas = np.array([[float(x[0]), float(x[1]), float(x[3])/30] for x in self.__estrellas])
        
    def estrellas(self, nombre_archivo):
        stars = []
        dic = {}
        with open(f"Archivos/{nombre_archivo}", "r") as archivo:
            for linea in archivo:
                vec = linea.split(" ")
                temp = [vec[0], vec[1], vec[3], vec[4]]
                text = ""
                for i in range(6, len(vec)):
                    text += f"{vec[i]} "
                if text != "":
                    nombres = text.split(";")
                    for estrella in nombres:
                        dic[estrella.strip()] = (float(temp[0]), float(temp[1]))
                stars.append(temp)
        return stars, dic

    def dic_constelaciones(self, txt):
        vec = []
        aux = []
        with open(f"Archivos/{txt}", "r") as archivo:
            for linea in archivo:
                splt = linea.split(",")
                splt[-1] = splt[-1].strip()
                vec.append(splt)
                for x in splt:
                    aux.append(x.strip())
            dic = {start:[] for start in aux}
            for union in vec:
                dic[union[0]] += [union[1]]
                dic[union[1]] += [union[0]]
        return dic

    def generar_estrellas(self):
        fig, ax = plt.subplots()
        plt.style.use('dark_background')
        plt.scatter(self.__coordenadas[:,0], self.__coordenadas[:,1], c="white", s = self.__coordenadas[:,2])
        ax.axis('off')
        plt.savefig("Cielo_Estrellado.png")

    def generar_estrellas_y_constelacion(self, constelacion, dic_estrellas):
        fig, ax = plt.subplots()
        plt.style.use('dark_background')
        ax.axis('off')
        ax.scatter(self.__coordenadas[:,0], self.__coordenadas[:,1], c="white", s = self.__coordenadas[:,2])
        dic_c = self.dic_constelaciones(f"{constelacion}.txt")
        for key, values in dic_c.items():
            for value in values:
                print([dic_estrellas[key][0], dic_estrellas[value][0]], [dic_estrellas[key][1], dic_estrellas[value][1]])
                plt.plot([dic_estrellas[key][0], dic_estrellas[value][0]], [dic_estrellas[key][1], dic_estrellas[value][1]], c = "olive", linewidth = 0.99)
        plt.savefig("Cielo_Estrellado_{constelacion}.png")

    def generar_estrellas_y_constelaciones(self, nombre_constelaciones):
        fig, ax = plt.subplots()
        plt.style.use('dark_background')
        ax.axis('off')
        ax.scatter(self.__coordenadas[:,0], self.__coordenadas[:,1], c="white", s = self.__coordenadas[:,2])
        for nc in nombre_constelaciones:
            constelacion = self.dic_constelaciones(f"{nc}.txt")
            for key, values in constelacion.items():
                for value in values:
                    plt.plot([self.__dic_estrellas[key][0], self.__dic_estrellas[value][0]], [self.__dic_estrellas[key][1], self.__dic_estrellas[value][1]], c = "olive", linewidth = 0.99)
        if len(nombre_constelaciones) == 1:
            plt.savefig(f"Cielo_Estrellado_{nombre_constelaciones[0]}.png")
        else:
            plt.savefig("Cielo_Estrellado_Constelaciones.png")

    def get_nombre_constelaciones(self):
        return self.__nombre_constelaciones

# %%
