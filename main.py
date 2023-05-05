#%%
from private import TOKEN
import telebot
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ForceReply
from funciones import Constelaciones

bot = telebot.TeleBot(TOKEN)

constelaciones_object = Constelaciones("stars.txt")

def main():
    @bot.message_handler(commands=["ayuda"])
    def cmd_ayuda(message):
        bot.send_message(message.chat.id, "/ayuda = Muestra todos los comandos\n"
                         "/estrellas = Muestra todas las estrellas sin constelaciones\n"
                         "/constelacion = Muestra las estrellas pero con una sola constelacion que elija el usuario\n"
                         "/constelaciones = Muestra las estrellas con todas las constelaciones existentes en el programa")

    @bot.message_handler(commands=["start"])
    def cmd_start(message):
        bot.send_message(message.chat.id, "Bienvenido a tu bot de confianza. Ingrese el comando /ayuda para mas informacion")

    @bot.message_handler(commands=["estrellas"])
    def cmd_estrellas(message):
        constelaciones_object.generar_estrellas()
        foto = open("Cielo_Estrellado.png", "rb")
        bot.send_photo(message.chat.id, foto, "Cielo Estrellado")
    
    @bot.message_handler(commands=["constelacion"])
    def cmd_constelacion(message):
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Escoje una constelacion", resize_keyboard=True)
        markup.add("Boyero", "Casiopea", "Cazo", "Cygnet", "Geminis", "Hydra", "OsaMayor", "OsaMenor")
        msg = bot.send_message(message.chat.id, "¿Cual es la constelacion que quieres visualizar?", reply_markup=markup)
        bot.register_next_step_handler(msg, mostrar_constelacion)

    @bot.message_handler(commands=["constelaciones"])
    def cmd_constelaciones(message):
        constelaciones_object.generar_estrellas_y_constelaciones(constelaciones_object.get_nombre_constelaciones())
        foto = open("Cielo_Estrellado_Constelaciones.png", "rb")
        bot.send_photo(message.chat.id, foto, "Cielo Estrellado con Constelaciones")
    
    def mostrar_constelacion(msg):
        try:
            constelaciones_object.generar_estrellas_y_constelaciones([msg.text])
            foto = open(f"Cielo_Estrellado_{msg.text}.png", "rb")
            bot.send_photo(msg.chat.id, foto, f"Cielo Estrellado con la Constelacion de nombre {msg.text}")
        except:
            bot.send_message(msg.chat.id, "Constelacion no encontrada. Intente seleccionar alguna constelacion disponible en el menu desplegable ubicado en la parte inferior derecha")

    bot.infinity_polling()

if __name__ == "__main__":
    print(f"Bot iniciado")
    main()



# %%
