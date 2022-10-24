import telebot
from config import TOKEN
from keys import exchanges
from extensions import APIException, Convert

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = f"Приветствую Вас! \nЧтобы просмотреть инструкцию используйте команду: /help\nДля просмотра доступных валют:\n/values"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате через пробел: \nИмя валюты;\nВ какую валюту перевести;\nКоличество переводимой валюты'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('Слишком много параметров.')
        if len(values) < 3:
            raise APIException('Недостаточно данных')
        quote, base, amount = values
        total_base = float(Convert.get_price(quote, base, amount))*int(amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()