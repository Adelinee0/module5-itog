import telebot
from config import exchanges, TOKEN
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types = ['voice'])
def repeat(message: telebot.types.Message):
    bot.send_message(message.chat.id, "У тебя красивый голос!")


@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):
    text = f"Привет, {message.chat.username}. Чтобы начать работу ввeдите команду боту с следующем формате:\n<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>." \
           f"\n Увидеть список всех доступных валют:/values"
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    #a = []
    for key in exchanges.keys():
        #a.append(key)
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Некорректное количество указанных параметров')

        quote, base, amount = values
        conv = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e} Ошибка сервера')
    else:
        text = f'Цена {amount} {quote} в {base} - {conv}'
        bot.send_message(message.chat.id, text)



bot.infinity_polling()