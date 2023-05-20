import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import sympy as sp
from fractions import Fraction
import re
import math
from IPython.display import display, Math
from sympy.parsing.sympy_parser import parse_expr
from sympy.logic import false
from sympy.plotting import plot
import requests
from io import BytesIO
from PIL import Image


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

class RRLHCCC():

    def __init__(self) -> None:
       self.__relacion = None
       self.__n = None
       self.__condiciones = None

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

    #Se sacan los frados de cada f y se pasa retorna como una dupla "(f(n-x), x)""
    def sacar_grado(self, cadena):
        regex = fr'f\(n\s*-\s*[0-9]+\)'
        resultado = re.findall(regex, cadena.replace(" ", ""))
        vec = []
        for i in resultado:
          vec.append([i, i[4:-1]])
        return (vec)   
     
    #Reescribe lo que se tiene de una funcion en su forma polinomica
    def polinomio(self, fn):
      x = self.sacar_grado(fn)
      vec = [i[1] for i in x]
      grado_max = int(max(vec))
      fn = f"x**{grado_max} + " + fn
      for i in x:
        fn = fn.replace(i[0], f"(-1)*x**{grado_max - int(i[1])}")
      return fn

    #Halla las raices de un polinomio
    def roots(self, poli):
      x = sp.symbols('x')
      p = poli
      return sp.roots(p)    
    
    #Obtiene la rrlhccc con valores expresados de b segun la multiplicidad de las raices
    def rrlccc(self, rootss):
      c = 0
      z = 0
      text = ""
      for key, value in rootss.items():
        text = text + "("
        count = 0
        for i in range(c, c + value):
          text = text + f"b_{i} * n**({count}) + "
          count = count + 1
          z += 1
        text = text[0:len(text) - 2] + ")*" + f"({key})**n + "
        c = c + value
      return text[0:len(text) - 3], z

    #Resuelve una funcion en terminos de alguna variable y un valor de esa variable
    def resolver_funcion(self, expr, valor_de_n, n):
      expr = sp.sympify(expr)
      valor_de_la_variable = {n: valor_de_n}
      valor_de_la_funcion = expr.subs(valor_de_la_variable)
      return valor_de_la_funcion

    #Resuelve un sistema de ecuaciones segun los valores iniciales y las ecuaciones 
    #Para Buscar su solicion
    def sistema(self, dic_c, vec):
      aux = []
      for value in dic_c.values():
        expresion = re.sub(r"sqrt\(([^)]+)\)", r"math.sqrt(\1)",value[0])
        resultado = eval(expresion)
        aux.append(resultado)
      vec.append(aux)   

    #Funcion con la se deja expresada la solucion homogenea con los b que hallan
    def coef_b(self, cad, n):
      coeficientes = {i:[] for i in range(n)}
      for i in range(n):
        aux = str(self.resolver_funcion(cad, 1, sp.symbols(f'b_{i}')))
        for j in range(n):
          if (i != j):
            aux = str(self.resolver_funcion(aux, 0, sp.symbols(f'b_{j}')))
        coeficientes[i] = [aux]
      return coeficientes   
    
    def resolver_sistema(self, eq, sol):
        # Obtener el número de variables
        num_variables = len(eq[-1])

        # Definir las variables simbólicas
        variables = sp.symbols(' '.join(['b_{}'.format(i) for i in range(num_variables)]))

        # Definir las ecuaciones utilizando los coeficientes
        ecuaciones = [sp.Eq(sum(coef * var for coef, var in zip(eq[i][:num_variables], variables)), sol[i])
                      for i in range(len(eq))]
        # Resolver el sistema de ecuaciones
        sol = sp.solve(ecuaciones, variables)
        return sol

  #Llama a cada una de las funciones en un orden especifico para obtener la respuesta
    def res(self, fn, ini, ini_n):
      poli = self.polinomio(fn)
      root = self.roots(poli)
      fh = self.rrlccc(root)
      vec = []
      for i in range(ini_n, len(ini) + ini_n):
        r, m = self.resolver_funcion(fh, i, n = sp.symbols('n'))
        self.sistema(self.coef_b(str(r), m), vec)
      coef = self.resolver_sistema(vec, ini)
      f = fh[0]
      for i in range(fh[1]):
        f = f.replace(f"b_{i}", str(coef[sp.symbols(f"b_{i}")]))
      return f
    
    def resolver_rrlhccc(self):
        return self.res(self.__relacion, self.__condiciones, self.__n)

    def latex_img(self, equation):
        equation_latex = sp.latex(parse_expr(equation))
        response = requests.get('http://latex.codecogs.com/png.latex?\dpi{{500}} {formula}'.format(formula=equation_latex))
        imagen_bytes = BytesIO(response.content)
        image = Image.open(imagen_bytes)
        image = image.convert('RGB')  # Convertir a formato RGB para guardar como JPG
        image_bytes_jpg = BytesIO()
        image.save(image_bytes_jpg, format='JPEG')
        image_bytes_jpg.seek(0)
        with open('latex_image.jpg', 'wb') as file:
            file.write(image_bytes_jpg.getvalue())