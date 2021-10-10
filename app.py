import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите комманду боту в слудеющем формате:\n" \
"<имя валюты с большой буквы кириллицей и без ошибок>\
<в какую валюту перевести с большой буквы кириллицей и также без ошибок>\
<количество переводимой валюты целой суммой без запятой. Пример: Доллар Рубль 150, " \
"для дробной суммы только через точку и без пробелов. Пример: Доллар Евро 20.5>\n" \
"<увидеть список всех доступных валют:/values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Приветствую! Modul18Bot готов помочь Вам конвертировать валюты EUR USD RUB>, '
                               'используйте команды подсказки /start /help и /values!')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
