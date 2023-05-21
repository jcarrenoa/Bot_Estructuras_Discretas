import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import re
import requests
from io import BytesIO
from PIL import Image


class Constelaciones():

    #Constructor de la clase Constelaciones

    #ATRIBUTOS:

    #__nombre_constelaciones = Atributo privado que contiene todalas las constelaciones que se encuentran en los archivos (lista)
    #__estrellas = Atributo privado con las coordenadas de todas las estrellas (lista)
    #__dic_estrellas = Atributo privado con las coordenadas de las estrellas con nombre (diccionario)
    #__coordemadas = Atributo privado con lsolo las coordenadas he intensidad de todas las estrellas (lista)
    def __init__(self, nombre_archivo) -> None:
        self.__nombre_constelaciones = ["Boyero", "Casiopea", "Cazo", "Cygnet", "Geminis", "Hydra", 
                             "OsaMayor", "OsaMenor"]
        self.__estrellas, self.__dic_estrellas = self.estrellas(nombre_archivo)
        self.__coordenadas = np.array([[float(x[0]), float(x[1]), float(x[3])/30] for x in self.__estrellas])
    
    #Funcion que sirve para retornar las coordenadas de todas las estrellas y un diccionario con solo las estrellas con nombres
    #PARAMETROS:
    #nombre_archivo = Parametro que contiene el nombre del archivo de todas las estrellas (str)
    def estrellas(self, nombre_archivo):
        stars = []
        dic = {}
        #Abre el archivo segun el nombre que se mando por parametro
        with open(f"Archivos/{nombre_archivo}", "r") as archivo:
            #For each que lee linea por linea del archivo
            for linea in archivo:
                #split de la linea segun los espacios
                vec = linea.split(" ")
                #Almacena en un vector temporal solo las coordenadas, la intensidad y codigo de la estrella
                temp = [vec[0], vec[1], vec[3], vec[4]]
                text = ""
                #Ciclo encargado de almacenar en una variable temporal de texto los nombres de las estrellas si es que tienen
                for i in range(6, len(vec)):
                    text += f"{vec[i]} "
                #Condicional para saber si tiene nombre o no una estrella
                if text != "":
                    #split del texto segun un punto y coma. Si tiene un punto y como es que la estrella tiene dos nombres
                    nombres = text.split(";")
                    #Ciclo para agregar todos los nombres que contenga una estrella
                    for estrella in nombres:
                        dic[estrella.strip()] = (float(temp[0]), float(temp[1]))
                stars.append(temp)
        return stars, dic

    #Funcion que da como resultado un diccionarios con conecciones de las estrellas dependiendo de la constelacion que se quiera hallar
    #PARAMETRO:
    #txt = Nombre de la constelacion de las que se hallaran las relaciones (str)
    def dic_constelaciones(self, txt):
        vec = []
        aux = []
        #Abre el archivo segun el nombre que se mande como parametro
        with open(f"Archivos/{txt}", "r") as archivo:
            #For each que lee linea por linea del archivo
            for linea in archivo:
                #split de una linea segun las comas
                splt = linea.split(",")
                splt[-1] = splt[-1].strip()
                vec.append(splt)
                #For each que cumple la funcion de agregar las relaciones que se encuentren en un vector auxiliar
                for x in splt:
                    aux.append(x.strip())
            #agrega todas las estrellas encontradas en un diccionario
            dic = {start:[] for start in aux}
            #For each que agrega en el diccionario todas las relaciones de todas las estrellas
            for union in vec:
                dic[union[0]] += [union[1]]
                dic[union[1]] += [union[0]]
        return dic

    #Funcion que se encarga de graficar todas las estrellas
    def generar_estrellas(self):
        fig, ax = plt.subplots()
        #Se configura el estilo de la grafica (Fondo negro y sin ejes)
        plt.style.use('dark_background')
        #Se generan todas las estrellas
        plt.scatter(self.__coordenadas[:,0], self.__coordenadas[:,1], c="white", s = self.__coordenadas[:,2])
        ax.axis('off')
        #Se guarda la imagen de las estrellas
        plt.savefig("Cielo_Estrellado.png")

    def generar_estrellas_y_constelacion(self, constelacion, dic_estrellas):
        fig, ax = plt.subplots()
        #Se configura el estilo de la grafica (Fondo negro y sin ejes)
        plt.style.use('dark_background')
        ax.axis('off')
        #Se generan todas las estrellas
        ax.scatter(self.__coordenadas[:,0], self.__coordenadas[:,1], c="white", s = self.__coordenadas[:,2])
        dic_c = self.dic_constelaciones(f"{constelacion}.txt")
        #Genera las figuras de la constelacion pasada como parametro
        for key, values in dic_c.items():
            for value in values:
                print([dic_estrellas[key][0], dic_estrellas[value][0]], [dic_estrellas[key][1], dic_estrellas[value][1]])
                plt.plot([dic_estrellas[key][0], dic_estrellas[value][0]], [dic_estrellas[key][1], dic_estrellas[value][1]], c = "olive", linewidth = 1.8)
        #Se guarda la imagen de las estrellas con la constelacion
        plt.savefig("Cielo_Estrellado_{constelacion}.png")

    def generar_estrellas_y_constelaciones(self, nombre_constelaciones):
        fig, ax = plt.subplots()
        #Se configura el estilo de la grafica (Fondo negro y sin ejes)
        plt.style.use('dark_background')
        ax.axis('off')
        #Se generan todas las estrellas
        plt.scatter(self.__coordenadas[:,0], self.__coordenadas[:,1], c="white", s = self.__coordenadas[:,2])
        #Genera las figuras de todas las constelaciones
        for nc in nombre_constelaciones:
            constelacion = self.dic_constelaciones(f"{nc}.txt")
            for key, values in constelacion.items():
                for value in values:
                    plt.plot([self.__dic_estrellas[key][0], self.__dic_estrellas[value][0]], [self.__dic_estrellas[key][1], self.__dic_estrellas[value][1]], c = "olive", linewidth = 1.05)
        #Se guarda la imagen de las estrellas con todas las constelaciones
        if len(nombre_constelaciones) == 1:
            plt.savefig(f"Cielo_Estrellado_{nombre_constelaciones[0]}.png")
        else:
            plt.savefig("Cielo_Estrellado_Constelaciones.png")

    #Funcion para obtener el atributo privado __nombre_constelaciones
    def get_nombre_constelaciones(self):
        return self.__nombre_constelaciones

class RRLHCCC():

    #Constructor de la clase RRLHCCC
    
    #ATRIBUTOS:

    #__relacion = Atributo privado que se le pasara la relacion de recurrencia
    #a evaluar como un str
    #__n = Atributo privado que se le pasara el valor por el que empiezan las condiciones iniciales
    #__condiciones = Atributo privado que se le pasara una lista con las condiciones iniciales en orden ascendente

    def __init__(self) -> None:
       self.__relacion = None
       self.__n = None
       self.__condiciones = None

    #getters y setters de los atributos de la clase

    @property
    def relacion(self):
       return self.__relacion
    
    @relacion.setter
    def relacion(self, set):
       self.__relacion = set
    
    @property
    def condiciones(self):
       return self.__condiciones

    @condiciones.setter
    def condiciones(self, condiciones):
       self.__condiciones = condiciones

    @property
    def n(self):
       return self.__n

    @n.setter
    def n(self, n):
       self.__n = n

    #Se sacan los grados de cada f y se pasa retorna como una dupla "(f(n-x), x)""
    #PARAMETROS:
    #cadena = Relacion de recurrencia a evaluar los grados
    def sacar_grado(self, cadena):
        #Expresion regural para identificar los f(n-k)
        regex = fr'f\(n\s*-\s*[0-9]+\)'
        #Nos devuelve cada f(n-k)
        resultado = re.findall(regex, cadena.replace(" ", ""))
        vec = []
        for i in resultado:
          #Agrega en un vector el f(n-k) y k como una dupla
          vec.append([i, i[4:-1]])
        return (vec)
    
    #Funcino que resuelve una relacion de recurrencia segun sus terminos y condiciones iniciales
    #PARAMETROS:
    #terminos = Terminos de la relacion de recurrencia (lista)
    #condiciones = Condiciones iniciales de la relacion de recurrencia (diccionario) 
    def resolver_homogenia(self, terminos, condiciones):
      #Define la variable f como funcion si encuentra una "f" en la ecuacion
      f = sp.Function('f')
      #Define la variable n como una variable simbolica si encuentra "n" en la ecuacion
      n = sp.symbols('n')
      #Define una funcion como f(n) siendo f una funcion y n una variable simbolica
      fun = f(n)
      for termino in terminos:
          #Cumple la funcion de restarle los terminos que se encuentran al lado derecho de f(n) en la relacion de recurrencia
          fun = fun - termino
      #Soluciona la relacion de recurrencia segun los parametros ingresados
      solucion = sp.rsolve(fun, f(n), condiciones)
      return solucion
    
    #Funcion que da el resultado de la ecuacion no recurrente como str
    #PARAMETROS:
    #recurrencia = Relacion de recurrencia a evaluar (str)
    #val_inical = Condiciones iniciales de la recurrencia (lista)
    #n = Valor por el cual empiezan las condiciones iniciales (int)
    def recurrencias_homogeneas(self, recurrencia, val_iniciales, n):
      #Convierte la cadena de la relacion de recurrencia a una expresion de sympy
      parse_rr = sp.parse_expr(recurrencia)
      #Diccionario con los valores iniciales de la relacion
      dic_f = {}
      i = 0
      #For each que recorre todos los valores iniciales
      for valor_f in val_iniciales:
        #Guarda en una variabel temporal el f(k) (condicion), y la pasa a una expresion de sympy
        temp_f = sp.parse_expr(f"f({n + i})")
        #Guarda en un diccionario el valor inicial de la condicion inicial
        #temp_f = Llave
        #valor_f = Valor
        dic_f[temp_f] = int(valor_f)
        i += 1
      #guarda los terminos por separados de la variable parse_rr
      terminos_rr = parse_rr.args
      #Llama la funcion resolver_homogenia
      fn_homogen = self.resolver_homogenia(terminos_rr, dic_f)
      #devuelve el resulado de lo anterior como un str
      return str(fn_homogen)

    #Funcion que sirve para guardar la funcion no recurrente encontrada como imagen
    #PARAMETROS:
    #equation = Ecuacion que se pasara a tipo imagen (str)
    def latex_img(self, ecuacion_rr):
        #Se convierte la ecuacion a una expresion de sympy
        latex_rr = sp.latex(sp.parse_expr(ecuacion_rr))
        #Variable que guarda la respuesta de la pagina que covierte la funcion a formato latex en imagen
        response = requests.get(f'http://latex.codecogs.com/png.latex?\dpi{{500}} {latex_rr}')
        #Si la respuesta de la pagina es satisfactoria nos convierte la respuesta de la pagina en una imagen
        #y devuelve True. Sino devuelve False y no hace ninguna operacion
        if response.status_code == 200:
            imagen_bytes = BytesIO(response.content)
            image = Image.open(imagen_bytes)
            image = image.convert('RGB')
            image_bytes_jpg = BytesIO()
            image.save(image_bytes_jpg, format='JPEG')
            image_bytes_jpg.seek(0)
            with open('latex_image.jpg', 'wb') as file:
                file.write(image_bytes_jpg.getvalue())
            return True
        else:
            return False