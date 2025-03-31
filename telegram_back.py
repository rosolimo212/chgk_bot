# coding: utf-8
# ELO-bot main file
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os
current_dir = os.path.abspath(os.getcwd())
parent_dir = os.path.dirname(current_dir)

import data_load as dl

import sys
sys.path.append(current_dir)

settings = dl.read_yaml_config('config.yaml', section='telgram_test_bot')

# telegram bot logic
def make_answer_buttons(buttons_lst):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in buttons_lst:
        item = types.KeyboardButton(button)
        markup.add(item)
    
    return markup 
    
async def start(bot, message):
    markup = make_answer_buttons([
         'Главное меню',
                                ])

    await bot.send_message(
            message.chat.id, 
            """
Введите ID свой команды
Его можно узнать вот здесь: https://rating.chgk.info/teams
            """,
            reply_markup=markup
                    )

    
async def launch_404(bot, message):
    markup = make_answer_buttons([
         'Главное меню',
                                ])

    await bot.send_message(
            message.chat.id, 
            """
К сожалению, что-то пошло не так: такой команды нет.
Возможно, произошла ошибка в самой игре. 
Возможно, вы использовали неожиданную текстовую команду.
Возвращайтесь в главное меню и попробуйте снова.
Если проблема повторяется, нажмите /start
            """,
            reply_markup=markup
                    )
    
bot = Bot(token=settings['token'])
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'старт'])
async def launch_main_menu(message):
    markup = make_answer_buttons([
         'Первая кнопка',
                                ])

    await bot.send_message(
        message.chat.id, 
        """
Привет!
Сейчас узнаем, как нам турниры заходят
        """,
        reply_markup=markup
                )


@dp.message_handler(content_types=["text"])
async def handle_text(message):
    if message.text.strip() in 'Первая кнопка':
        try:
            await start(bot, message) 
        except:
            await launch_404(bot, message)
    elif message.text.strip() in 'Главное меню':
        try:
            await launch_main_menu(message) 
        except:
            await launch_404(bot, message)
    else:
        try:
            await launch_404(bot, message)
        except:
            await bot.send_message(chat_id=249792088, text="Опять какая-то хрень")

print('Ready for launch')
executor.start_polling(dp)