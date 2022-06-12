from telebot.async_telebot import AsyncTeleBot
from stdnum.util import isdigits
import asyncio
import json


def chech_valid(number):
    """Проверяет контрольную цифру для 10-значных ИНН юридических лиц"""
    if not isdigits(number):
        return 'Формат'

    if len(number) == 10:
        weights = (2, 4, 10, 3, 5, 9, 4, 6, 8)
        return int(number[9]) == sum(w * int(n) for w, n in zip(weights, number)) % 11 % 10
    else:
        return 'Число'
           

def telegram_bot(token):
    bot = AsyncTeleBot(token)
    print('Бот запущен')


    # Обработчик сообщения '/start'
    @bot.message_handler(commands=['start'])
    async def start_message(message):
        await bot.send_message(message.chat.id,
        "Привет, хочешь проверить ИНН юридического лица на валидность? Тогда просто отправь ИНН и я помогу тебе с этим")

    
    # Обработчик сообщений для проверки ИНН
    @bot.message_handler()
    async def get_user_text(message):
        if chech_valid(message.text) == 'Формат':
            msg = f'Проверь формат ИНН'
        elif chech_valid(message.text) == 'Число':
            msg = f'Проверь длину ИНН'
        elif chech_valid(message.text) == True:
            msg = f'ИНН {message.text} валидно'
        elif chech_valid(message.text) == False:
            msg = f'ИНН {message.text} не валидно'
        else:
            msg = f'Unknown reason'

        await bot.send_message(message.chat.id, msg)

    
    asyncio.run(bot.polling())


if __name__ == '__main__':
    with open('const.json', 'r') as const_file:
        data = json.load(const_file)

    telegram_bot(data['token'])