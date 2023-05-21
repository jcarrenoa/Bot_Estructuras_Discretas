from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class InlineKeyboard():

    #Metodo que genera el menu de las opciones del bot
    @staticmethod
    def markup_inline_menu():
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Estrellas", callback_data = "Si"),
                   InlineKeyboardButton("Relaciones de recurrencias", callback_data = "No"),
                   InlineKeyboardButton("Cerrar", callback_data = "cerrar"))
        return markup

    #Metodo que genera el menu de las opciones de las constelaciones
    @staticmethod
    def markup_inline_cielo():
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton("Cielo estrellado", callback_data = "cielo"),
                   InlineKeyboardButton("Cielo con una constelacion", callback_data = "cielo_c_uc"),
                   InlineKeyboardButton("Cielo con todas las constelaciones", callback_data = "cielo_c_tc"))
        return markup