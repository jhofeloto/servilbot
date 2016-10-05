# -*- coding: utf-8 -*-
"""
Este ejemplo muestra como capturar datos de un usuario realizando un registro paso a paso
"""
import time #Es un modulo de python
"""
El módulo time difiere de date o datetime porque representa el tiempo en segundos desde el epoch (comenzando desde 1970)

"""
import telebot #Se llama la libreria de telegram para python pyTelegramBotAPI
"""
Para instalar realizar este procedimeinto en la terminal
git clone https://github.com/eternnoir/pyTelegramBotAPI.git
cd pyTelegramBotAPI
python setup.py install
mas info: https://wp.me/p4lhgi-42j
"""
from telebot import types

API_TOKEN = '262667998:AAHEfNe9BArbkAdMr3LAmWHEsARv8H1fRaM' # Esta es el token que BotFather le asigna para el BOT ver: http://botsfortelegram.com/?p=1529 

bot = telebot.TeleBot(API_TOKEN) # se nombra la variable bot para ser llamada posteriormente y se realiza la llave entre el modulo telebot y el TOKEN del BOT para este caso servilBOT

user_dict = {} # 
""" 
dict
Un dict (diccionario) de Python es una tabla hash que asocia (map) un objeto-clave a un objeto-valor. 
Por ejemplo:
>>> a = {'k':'v', 'k2':3}
>>> a['k']
v
>>> a['k2']
3
>>> a.has_key('k')
True
>>> a.has_key('v')
False
Ver mas en: https://goo.gl/ZUN7xA
"""

class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None

""" Class
Como Python es un lenguaje de tipado dinámico, las clases y objetos pueden resultar extrañas. 
De hecho no necesitas definir las variables incluidas (atributos) al declarar una clase, y distintas instancias de la misma clase pueden tener distintos atributos. 
Los atributos (attribute) se asocian generalmente con la instancia, no la clase (excepto cuando se declaran como atributos de clase o "class attributes", que vienen a ser las "static member variables" de C++/Java).

Aquí se muestra un ejemplo:

>>> class MiClase(object): pass
>>> miinstancia = MiClase()
>>> miinstancia.mivariable = 3
>>> print miinstancia.mivariable
3
"""

# Handle (o encargarse de:) '/start' y '/help'

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hola, Soy Servil.
Cual es tu nombre?
""")
    bot.register_next_step_handler(msg, process_name_step)

"""
Handle o encargarse de, es un comando de la API para arancar el bot, se estan definiendo los 
comando basicos para arrancar el BOT, en este caso se colocó start para arracar y help, aunque este no esta definido, asu vez se asigna
la primera cción que es reply_to como función de responder ante la solicitud de /start ,indicando un mensaje de presentación y una primera pregunta, 
se deja preparado el sigueinte paso con la función "register_next_step_handler" registro, definiendo el siguiente paso "process_name_step" paso proceso nombre, junto con la función 
msg la cual se nombro como bot.reply_to(message..
"""

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Cuantos años tienes?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

"""
Esta función define el proceso 1: denominado process_name_step, donde se indica el mensaje siguiente: Cuantos años tienes? llamando el sigueinte paso "process_age_step"
generando una excepción por si no coloca un numero, esta excepción se describe en el sigueinte paso  

"""

def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'La edad debe ser un numero. Cuantos años tienes?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Masculino', 'Femenino')
        msg = bot.reply_to(message, 'Cual es tu genero', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

"""
Este proceso indicar  "" process_age_step", donde se coloca la excepción si no escribe un numero con la función isdigit
para hcer bucle hasta que se coloque la respuesta correcta, luego se lanza el sigueinte proceso haciendo la pregunta "Cual es tu género, llamado un keyboard 
"ReplyKeyboardMarkup" y através de markup añade las opciones de una línea, si quisiera colocar mas de una linea debería colocar algo así:
markup.row('a', 'v')
markup.row('c', 'd', 'e')
Y lanza la ejecución del sigueinte paso
"""

def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Masculino') or (sex == u'Femenino'):
            user.sex = sex
        else:
            raise Exception()
        bot.send_message(chat_id, 'Gracias por tu informacion ' + user.name + '\n Edad:' + str(user.age) + '\n Sexo:' + user.sex)
    except Exception as e:
        bot.reply_to(message, 'oooops')

"""
En este último proceso se imprime el resumen de la información cargada en los pasos anteriores, cerrando con una especie de combinación de resultados
donde une los valores guardados : user.name , user.age, user.sex, 
"""

bot.polling()