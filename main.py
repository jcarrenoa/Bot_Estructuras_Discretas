#%%
from private import BotVariables
import telebot
from telebot.types import ReplyKeyboardMarkup
from funciones import Constelaciones, RRLHCCC
from bot_funcion import InlineKeyboard

#Se inicializa el bot y objetos de las clases Constelaciones y RRLHCCC que son 
#las que hacen las operaciones para dichas funcionalidades
Variables = BotVariables()
bot = telebot.TeleBot(Variables.TOKEN)
constelaciones_object = Constelaciones("stars.txt")
rr_object = RRLHCCC()

def main():

    #Llamada del menu de las funcionalidades si se ingresa el comando /menu 
    @bot.message_handler(commands=["menu"])
    def cmd_menu(message):
        bot.send_message(message.chat.id, "Selecciona una opcion del menu", reply_markup = InlineKeyboard.markup_inline_menu())

    #Llamada del menu de ayuda si se ingresa el comando /ayuda
    @bot.message_handler(commands=["ayuda"])
    def cmd_ayuda(message):
        #Mensaje con todos los comandos disponible
        bot.send_message(message.chat.id, "--------- COMANDOS GENERALES ---------\n\n"
                         "/ayuda = Muestra todos los comandos\n"
                         "/menu = Muestra todas las opciones en un menu\n\n"
                         "--------- COMANDOS ESPECIFICOS ---------\n\n"
                         "Comandos para las constelaciones:\n\n"
                         "/estrellas = Muestra todas las estrellas sin constelaciones\n"
                         "/constelacion = Muestra las estrellas pero con una sola constelacion que elija el usuario\n"
                         "/constelaciones = Muestra las estrellas con todas las constelaciones existentes en el programa\n\n"
                         "Comandos para las relaciones de recurrencias:\n\n"
                         "/RR = resuelve relaciones de recurrencias lineales homogeneas con coeficientes constantes")

    #Llamada del mensaje de bienvenida si se ingresa el comando /start
    @bot.message_handler(commands=["start"])
    def cmd_start(message):
        bot.send_message(message.chat.id, "Bienvenido a tu bot de confianza %s" % u'\U0001F913' + ". Ingrese el comando /ayuda para mas informacion %s" % u'\U0001F9D0')

    #Llama del metodo seleccionado segun lo que el usuario haya seleccionado en los diferentes menus
    @bot.callback_query_handler(func=lambda message: True)
    def callback_query(call):

        #Llama la funcion que devuelve el cielo estrellado
        if call.data == "cielo":
            bot.delete_message(call.from_user.id, call.message.id)
            cmd_estrellas_menu(call)

        #Llama la funcion que devuelve el cielo estrellado con una constelacion
        if call.data == "cielo_c_uc":
            bot.delete_message(call.from_user.id, call.message.id)
            cmd_constelacion_menu(call)

        #Llama la funcion que devuelve el cielo estrellado
        if call.data == "cielo_c_tc":
            bot.delete_message(call.from_user.id, call.message.id)
            cmd_constelaciones_menu(call)

        #Llama al metodo que devuelve el menu de las constelaciones
        if call.data == "Si":
            bot.delete_message(call.from_user.id, call.message.id)
            bot.send_message(call.from_user.id, "Selecciona una opcion del menu de estrellas", reply_markup = InlineKeyboard.markup_inline_cielo())
        
        #Llama la funcion que desencadena los textos de requerimientos para resolver una relacion de recurrencia
        if call.data == "No":
            bot.delete_message(call.from_user.id, call.message.id)
            cmd_RR_menu(call)

        #Llama al cierre del menu
        if call.data == "cerrar":
            bot.delete_message(call.from_user.id, call.message.id)

    #Funciones por menu:

    #Genera el cielo estrellado y la manda al usuario
    def cmd_estrellas_menu(call):
        constelaciones_object.generar_estrellas()
        foto = open("Cielo_Estrellado.png", "rb")
        bot.send_photo(call.from_user.id, foto, "Cielo Estrellado %s" % u'\U0001F4AB')

    #Le pregunta al usuario cual constelacion quiere ver
    def cmd_constelacion_menu(call):
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Escoje una constelacion", resize_keyboard=True)
        markup.add("Boyero", "Casiopea", "Cazo", "Cygnet", "Geminis", "Hydra", "OsaMayor", "OsaMenor")
        msg = bot.send_message(call.from_user.id, "¿Cual es la constelacion que quieres visualizar %s?" % u'\U0001F914 \U0001F4AB', reply_markup=markup)
        bot.register_next_step_handler(msg, mostrar_constelacion)

    #Genera el cielo estrellado con todas las constelaciones y la manda al usuario
    def cmd_constelaciones_menu(call):
        constelaciones_object.generar_estrellas_y_constelaciones(constelaciones_object.get_nombre_constelaciones())
        foto = open("Cielo_Estrellado_Constelaciones.png", "rb")
        bot.send_photo(call.from_user.id, foto, "Cielo Estrellado con Constelaciones %s" % u'\U0001F30C')

    #Le pregunta al usuario por la relacion de recurrencia que quiere resolver
    def cmd_RR_menu(call):
        msg = bot.send_message(call.from_user.id, "Ingrese su relacion de relacion de recurrencia de la fomra "
                               "f(n) = C1*f(n - 1) + ... + g(n)")
        bot.register_next_step_handler(msg, valores_de_n)

    #Funciones por comandos:

    #Genera el cielo estrellado y la manda al usuario
    @bot.message_handler(commands=["estrellas"])
    def cmd_estrellas(message):
        constelaciones_object.generar_estrellas()
        foto = open("Cielo_Estrellado.png", "rb")
        bot.send_photo(message.chat.id, foto, "Cielo Estrellado %s" % u'\U0001F4AB')

    #Le pregunta al usuario cual constelacion quiere ver
    @bot.message_handler(commands=["constelacion"])
    def cmd_constelacion(message):
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Escoje una constelacion", resize_keyboard=True)
        markup.add("Boyero", "Casiopea", "Cazo", "Cygnet", "Geminis", "Hydra", "OsaMayor", "OsaMenor")
        msg = bot.send_message(message.chat.id, "¿Cual es la constelacion que quieres visualizar %s?" % u'\U0001F914 \U0001F4AB', reply_markup=markup)
        bot.register_next_step_handler(msg, mostrar_constelacion)

    #Genera el cielo estrellado con todas las constelaciones y la manda al usuario
    @bot.message_handler(commands=["constelaciones"])
    def cmd_constelaciones(message):
        constelaciones_object.generar_estrellas_y_constelaciones(constelaciones_object.get_nombre_constelaciones())
        foto = open("Cielo_Estrellado_Constelaciones.png", "rb")
        bot.send_photo(message.chat.id, foto, "Cielo Estrellado con Constelaciones %s" % u'\U0001F30C')

    #Le pregunta al usuario por la relacion de recurrencia que quiere resolver
    @bot.message_handler(commands=["RR"])
    def cmd_RR(message):
        #Genera un mensaje de como debe ingresar los datos el usuario
        msg = bot.send_message(message.chat.id, "Ingrese su relacion de relacion de recurrencia de la fomra "
                               "f(n) = C1*f(n - 1) + ... + g(n)")
        bot.register_next_step_handler(msg, valores_de_n)

    #Genera un mensaje al usuario por si se ha equivocado de comando o a escrito algo que no puede interpretar el bot
    @bot.message_handler(content_types=["text"])
    def bot_message_text(message):
        if message.text.startswith("/"):
            bot.send_message(message.chat.id, "Comando no disponible. Para mas informacion ingrese el comando de /ayuda")
        else:
            bot.send_message(message.chat.id, "Lo siento, no puedo interpretar tu mensaje. Para mas informacion ingrese el comando de /ayuda")

    #Pregunta por el valor en el que empezaran las condiciones iniciales
    def valores_de_n(msg):
        rr_object.relacion = msg.text
        #Genera un mensaje de como debe ingresar los datos el usuario
        msg = bot.send_message(msg.chat.id, "¿Desde que valor de \"n\" empiezan las condiciones iniciales %s?" % u'\U0001F914')
        bot.register_next_step_handler(msg, condiciones_iniciales)

    #Pregunta por las condiciones iniciales de la relacion de recurrencia
    def condiciones_iniciales(msg):
        #Bloque try except que permite saber si se pudo hacer o no la operacion pedida al usuario
        #Sino se pudo es porque se ingresaron valores erroneos
        try:
            text = ""
            rr_object.n = int(msg.text)
            #Saca el mayor grado de la relacion de recurrencia
            aux = [i[1] for i in rr_object.sacar_grado(rr_object.relacion)]
            max_grado = int(max(aux))
            #Genera un mensaje de como debe ingresar los datos el usuario
            for i in range(max_grado):
                text += f"f({i + int(rr_object.n)}) "
            msg = bot.send_message(msg.chat.id, f"Digite las condiciones {text.strip()}, seguida(s) de comas en orden acendente\n"
                                   "Por ejemplo: 1, 3 siendo 1 = f(0) y 3 = f(1)" )
            bot.register_next_step_handler(msg, mostrar_formula)
        except:
            bot.send_message(msg.chat.id, "No se puede realizar la operacion con los datos suministrados. Por favor, intente ingresarlos correctamente", )
            bot.send_message(msg.chat.id, "Selecciona una opcion del menu", reply_markup = InlineKeyboard.markup_inline_menu())

    def mostrar_formula(msg):
        #Bloque try except que permite saber si se pudo hacer o no la operacion pedida al usuario
        #Sino se pudo es porque se ingresaron valores erroneos
        try:
            text = msg.text.replace(" ", "")
            vec = text.split(",")
            rr_object.condiciones = [int(x) for x in vec]
            res = rr_object.latex_img(rr_object.recurrencias_homogeneas(rr_object.relacion, rr_object.condiciones, rr_object.n))
            if res:
                foto = open('latex_image.jpg', "rb")
                bot.send_photo(msg.chat.id, foto, "Formula no recurrente encontrada")
            else:
                bot.send_message(msg.chat.id, "Formula no recurrente encontrada\n\n"
                f"f(n) = {rr_object.recurrencias_homogeneas(rr_object.relacion, rr_object.condiciones, rr_object.n)}")
        except:
            bot.send_message(msg.chat.id, "No se puede realizar la operacion con los datos suministrados. Por favor, intente ingresarlos correctamente.\n\n"
                             "Ten en cuenta que si ingresastes datos que supuestamente son correctos y sigue dando error, puede ser debido a raices imaginarias")
            bot.send_message(msg.chat.id, "Selecciona una opcion del menu", reply_markup = InlineKeyboard.markup_inline_menu())

    def mostrar_constelacion(msg):
        #Bloque try except que permite saber si se pudo hacer o no la operacion pedida al usuario
        #Sino se pudo es porque se ingresaron valores erroneos
        try:
            constelaciones_object.generar_estrellas_y_constelaciones([msg.text])
            foto = open(f"Cielo_Estrellado_{msg.text}.png", "rb")
            bot.send_photo(msg.chat.id, foto, f"Cielo Estrellado con la Constelacion de nombre {msg.text} " + "%s" % u'\U0001F30C')
        except:
            bot.send_message(msg.chat.id, "Constelacion no encontrada. Intente seleccionar alguna constelacion disponible en el menu desplegable ubicado en la parte inferior derecha")
    
    bot.infinity_polling()

if __name__ == "__main__":
    print("Bot iniciado")
    main()
# %%
