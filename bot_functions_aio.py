import os

from bs4 import BeautifulSoup
from requests import Session
from random import choice
from datetime import datetime
from subprocess import check_output, STDOUT
from mss import mss
from aiogram import Bot, Dispatcher, executor, types

# 
def handler():
    
    bot = Bot(token='токен')
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['ls'])
    async def ls(message: types.Message): # Получить список файлов/папок в директории
        await message.answer('\n- '.join([f'{i}' for i in (os.listdir(f'{os.getcwd()}'))]))
    
    @dp.message_handler(regexp=r'привет|hi|сап')
    async def message_handler(message: types.Message): # А это поздороваться
        phrase = (set(message.text.lower().split()))
        try:
            greet_phrase = \
            choice(['Доброе утро', 'Привет!']) if 5 <= int(str(datetime.now().time())[:2]) <= 11 \
            else choice(['Добрый день', 'Привет!']) if 12 <= int(str(datetime.now().time())[:2]) <= 17 \
            else choice(['Добрый вечер', 'Привет!']) if 18 <= int(str(datetime.now().time())[:2]) <= 22 \
            else choice(['Доброй ночи', 'Привет!'])
            await message.reply(greet_phrase)    
        except:
            pass

    @dp.message_handler(regexp='пароль|password|pass|пасс')   
    async def message_handler(message: types.Message): 
        phrase = (set(message.text.lower().split()))
        try:
            pass_len = 10
            z = message.text.lower().split()
            for i in z:
                try: pass_len = int(i)
                except: pass
            await message.reply(''.join(choice('QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm234567890') 
                            for i in range(1 if pass_len <= 0 \
                            else 300 if pass_len > 300 \
                            else pass_len)) )
        except:
            pass

    @dp.message_handler(commands=['start'])
    async def start(message: types.Message): # Старт бота
        await message.answer("Roger-roger!")

    @dp.message_handler(commands=['getcwd'])
    async def gcwd(message: types.Message): # Получить current dir
        await message.answer(f"{os.getcwd()}")
    
    @dp.message_handler(commands=['cmd'])
    async def cmd(message: types.Message): # Выолнить команду в терминале
        x = message.text.lower()[5:]
        try:
            y = check_output(x, shell=True,stderr=STDOUT)
            await message.answer(f"{y.decode('ISO-8859-1')}")
        except:
            await message.answer(text="sorry, can't do this")

    @dp.message_handler(commands=['screen'])
    async def screenshot(message: types.Message): # Сделать и отослать скрин
        with mss() as sct:
            sct.shot()
        with open('monitor-1.png', 'rb') as photo:
            await message.reply_photo(photo)
        os.remove('monitor-1.png')

    @dp.message_handler(commands=['cd'])
    async def cd(message: types.Message): # Сменить директорию
        try:
            x = message.text.lower()[4:]
            os.chdir(x)
        except:
            await message.reply("соре хуйня")
        else:
            await message.answer(f"{os.getcwd()}")
    
    @dp.message_handler(regexp='табель|оценки|зачеты|экз|экзамен')
    async def get_marks(message: types.Message):

        class Iterpals(object):

            url = 'https://student.rea.ru/'

            def auth(self):
                '''authorization on the site'''
                session = Session()
                url = self.url + 'progress/'
                params = {'AUTH_FORM': 'Y',
                        'TYPE': u'AUTH',
                        'backurl': u'/index.php',
                        'USER_LOGIN': u'Логин',
                        'USER_PASSWORD': u'Пароль',
                        'Login': u'Войти'}
                r = session.post(url, params)
                return r

            def get_data(self, auth, data):
                '''getting needed data'''
                soup = BeautifulSoup(auth.text, 'lxml')
                text = soup.find_all("div", {'class':data})
                return text

            def convert_to_normal(self, text_list, excluding=''):
                '''Convert dumbass html to normal text'''
                for t in range(len(text_list)):
                    text_list[t] = text_list[t].text.strip()
                text_list = list(filter(lambda word: word != excluding, text_list))
                return text_list
            
            def zip_items(self, iter1, iter2, iter3):
                zipped_items = zip(iter1, iter2, iter3)
                zipped_items = list(zipped_items)
                map(list(),list(zipped_items))
                return zipped_items

            # setup work   
        def main(Iterpals): 
            Iterpals = Iterpals()
            auth = Iterpals.auth()
            get_data_item = Iterpals.get_data(auth, data="es-progress__line-item es-discipline")
            convert_data_item = map(lambda x: f'>> {x[:]}', Iterpals.convert_to_normal(get_data_item, excluding ='Дисциплина'))
            get_data_form= Iterpals.get_data(auth, data="es-progress__line-item es-form")
            convert_data_form = Iterpals.convert_to_normal(get_data_form, excluding ='Форма отчетности')
            get_data_val = Iterpals.get_data(auth, data="es-progress__line-item es-valuation")
            convert_data_val = Iterpals.convert_to_normal(get_data_val, excluding ='Оценка')
            zipped_items = Iterpals.zip_items(convert_data_item, convert_data_form, convert_data_val)
            ZI_list = []
            for items in zipped_items:
                ZI_list.insert(0,'--'.join(map(str, items)))
            return '\n'.join(ZI_list)

        cooked_vals = main(Iterpals)
        await message.answer(text=cooked_vals)

    @dp.message_handler(commands=['help'])
    async def help_command(message: types.Message): # Получить помощь по командам #! Обновлять по мере появления новых команд/функций
        await message.answer(text='Вот какие команды я знаю')
        await message.answer(text='''1. /start - Начало работы со мной
2. /getcwd - Вывод адреса текущей рабочей директории
3. /cd - Смена рабочей директории
4. /ls - Вывод содержимого текущей рабочей директории
5. /cmd _____ - Исполнение команды терминала
6. /screen - Вывод скриншота
7. сделай пароль/пароль - Генерирует пароль, если есть число - принимает как длину пароля
8. оценки/табель/экзы - Выводит табеля''')

    return dp
