#Clase con las variables que requiere el bot para su funcionamiento

class BotVariables():

    def __init__(self) -> None:
        #Token del bot
        self.__token = "5701940559:AAEbpgA7Ns8ig0siGAET6iW8k-QlXZPspKg"
    
    #Funcion que devuelve el token de la clase
    @property
    def TOKEN(self):
        return self.__token