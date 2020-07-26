
#* Воскрес
#*
#*
#*
#*

import logging

from bot_functions_aio import handler
from aiogram import executor

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    executor.start_polling(handler(), skip_updates=True)