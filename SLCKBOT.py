
from telegram.ext import Updater
from bot_functions import *
from bot_handlers import handling

#! Запуск бота
if __name__ == '__main__':
    try:
        handling().start_polling()
    except:
        print('Something went wrong...')
    else:
        print('Success!')
    