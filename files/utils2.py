# -*- coding: utf-8 -*-
import telebot, json
from enum import Enum
from telebot import types
from models2 import *


HELLO_MESSAGE = "\t{}, привет. Меня зовут Шпулечка! Я буду помогать Вам проходить онлайн-марафон по текстильным куколкам.\n\n\t\
Если вы здесь впервые, то перейдите по ссылке:\n👉🏼 {}\n\n\tОбязательно прочитайте эту статью! Там я рассказала важные аспекты, благодаря которым Вы сможете получить от меня мега-ценные подарки на марафоне.\n\n\t\
🌺Поэтому, не ругайтесь потом на меня, если вдруг пропустили эту информацию!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot"
TASK_WORDS = {
    1 : ['#привет', 'zgEnCQ7~LG'], 
    2 : ['#цель', 'Jp~Bt}xPFP'], 
    3 : ['#миф', 'y~rNV3Vn~1'], 
    4 : ['#инсайт', 'hb5DrmF{5E'],
    5 : ['6C5pTjzegZ'], 
    6 : ['hs76sPA%ZV']
}

TASK_6_COLORS = [
    'Оттенок №1',
    'Оттенок №2',
    'Оттенок №3',
    'Оттенок №4', 
    'Оттенок №5',
    'Оттенок №6'
]

T5_TEXT = """Сегодня будет домашнее задание с проверкой Вашей внимательности.

1. Как вы считаете, нужны ли специальные виды игл, чтобы правильно шить трикотаж? Если да, то какие? (на фирму не обращаем внимания, это просто мои любимые).

Выберите верный вариант из представленных в опросе ниже.

2. После того, как выберете вариант, напишите, почему выбрали именно его.

Выполните задание прямо сейчас, чтобы заработать +10 пуговок (ниточек) и в конце марафона получить от меня ценные подарки.


"""

T6_TEXT = """
Девочки, перед Вами палитра из 6-ти оттенков.

1. Выберите в опросе два оттенка, которые на Ваш взгляд сочетаются друг с другом больше всего.

2. После того, как проголосуете в опросе, придумайте и напишите необычное название минимум для одного оттенка.

Например: Оттенок № 4 - имбирный каппучино😄


"""

task_title = [
    'Задание 1',
    'Задание 2',
    'Задание 3',
    'Задание 4',
    'Задание 5',
    'Задание 6'
]
    
TASK_TEXT = {
    1: 'Предварительное задание "Знакомство".\n',
    2: 'Предварительное задание "Цели".\n',
    3: "Предварительное задание \"Миф\".\n",
    4: "Основное задание \"ДЗ1\".\n",
    5: T5_TEXT,
    6: T6_TEXT
}

TASK_5_ITEMS = [
    'Иглы №1', 
    'Иглы №2', 
    'Иглы №3', 
    'Любые'
]

TASK_FINISH_MESSAGES = [
    '\tОтправила Вам в корзинку +5 пуговок 🔵 за выполнение задания со знакомством.\n\n\tКстати, Вы можете нажать кнопку "Баланс" и узнать, сколько у Вас пуговок и какие задания ещё необходимо выполнить.\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot',
    '\tЕсть цель - летим к ней 🕶️🚀\nОтправила Вам в корзинку +5 пуговок 🔵\n\n\tКстати, Вы можете нажать кнопку "Баланс" и узнать, сколько у Вас пуговок и какие задания ещё необходимо выполнить.\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot',
    '\t+1 пуговка за Ваш миф 🔵 Может у Вас есть ещё мифы в запасе?\n\n\tКстати, Вы можете нажать кнопку "Баланс" и узнать, сколько у Вас пуговок и какие задания ещё необходимо выполнить.\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot',
    '\t😘 {name}, задание выполнено. Отправила 10 пуговок 🔵 Вам на счёт!\n\n\tКстати, Вы можете нажать кнопку "Баланс" и узнать, сколько у Вас пуговок и какие задания ещё необходимо выполнить.\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot',
    '\t{name}, задание выполнено. Отправила 10 пуговок 🔵 Вам на счёт!\n\n\tКстати, Вы можете нажать кнопку "Баланс" и узнать, сколько у Вас пуговок и какие задания ещё необходимо выполнить.\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot',
    '\t😘 {name}, задание выполнено. Отправила 10 пуговок 🔵 Вам на счёт!\n\n\tКстати, Вы можете нажать кнопку "Баланс" и узнать, сколько у Вас пуговок и какие задания ещё необходимо выполнить.\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot',
]

INSTRUCTION_TEXT = """ 1. Перейдите на сайт: https://guryleva.ru/school-marafon3 и выберите подходящий пакет

2. Нажмите кнопку "Купить"

3. Заполните форму и нажмите кнопку "Оплатить"

4. Нажмите на кнопку "Знаете промо-код?" и введите в поле промокод "{}" (без кавычек), нажмите "Применить"

5. Оплатите со скидкой удобным для Вас способом

Ниже добавила инструкцию со скриншотами 👇"""


MES_START_MARATHON = '#старт'
MES_FINISH_MARATHON = '#стоп'
MES_OPEN_TASK = '#задание'
MES_OPEN_REWARD= '#пуговка'

class MessageType(Enum):
    open_task = 1
    start_marathon = 2
    finish_marathon = 3
    show_reward = 4


class MessageData (object):
    def __init__(self, type_, task=None,link=None):
        self.type = type_
        self.task = task
        self.link = link
        
    @classmethod
    def construct(cls, type_, task=None, link=None):
        return cls(type_, task, link)

def get_user_mes_type(text):
    """
    :param text: - сообщение
    :return int: - [1; 6] - номер задания (5-6 - секретные слова)
    :return None:- не команда
    """
    text = text.lower()
    for task, val in TASK_WORDS.items():
        for kw in val:
            if kw.lower() in text:
                return task
    return None

def get_adm_mes_type(text):
    """
    :param text: - сообщение
    :return MessageData: - тип команды
    :return None: в случае, если не команда
    """

    if is_start_marathon(text.lower()):
        return MessageData(type_ = MessageType.start_marathon, link = text[7:])
    elif is_finish_marathon(text.lower()):
        return MessageData(type_ = MessageType.finish_marathon)
    elif is_open_reward(text.lower()):
        Marathon.open_reward()
        return None
    elif is_open_task(text.lower()):
        if ord(text[8]) >= 48 and ord(text[8]) <= 57:
            return MessageData(type_ = MessageType.open_task, task = int(text[8]), link = text[10:])
        else:
            return None
    else:
        return None

def is_open_reward(text):
    """
    :param text: - текст сообщения в нижнем регистре
    :return True:- это сообщение пуговки
    :return False: - это сообщение пуговки
    """ 
    return MES_OPEN_REWARD in text


def is_start_marathon(text):
    """
    :param text: - текст сообщения в нижнем регистре
    :return True:- это сообщение старта марафона
    :return False: - это не старт марафона
    """ 
    return MES_START_MARATHON in text

def is_finish_marathon(text):
    """
    :param text: - текст сообщения в нижнем регистре
    :return True:- это сообщение конца марафона
    :return False: - это не конец марафона
    """ 
    return MES_FINISH_MARATHON in text 

def is_open_task(text):
    """
    :param text: - текст сообщения в нижнем регистре
    :return True:- это сообщение задания
    :return False: - это не задание
    """ 
    return MES_OPEN_TASK in text
    
def get_buttons(tg_id):
    """
    :param tg_id: - айди пользователя
    :return InlineKeyboardMarkup: - клавиатура
    """
    but = types.InlineKeyboardMarkup(row_width=3)
    av_tasks = int(Marathon.get_t_available())
    buttons = []
    for i in range(av_tasks):
        task = i + 1
        if User.is_task_finished(tg_id, task) or (task == 3 and User.t3_is_finished(tg_id)):
            t = types.InlineKeyboardButton(text="✅ {}".format(task_title[i]), callback_data="t{}".format(task))
            buttons.append(t)
        else:
            t = types.InlineKeyboardButton(text="❌ {}".format(task_title[i]), callback_data="t{}".format(task))
            buttons.append(t)

    if len(buttons) == 1:
        but.add(buttons[0])
    elif len(buttons) == 2:
        but.row(buttons[0], buttons[1])
    elif len(buttons) == 3:
        but.row(buttons[0], buttons[1], buttons[2])
    elif len(buttons) == 4:
        but.row(buttons[0], buttons[1])
        but.row(buttons[2], buttons[3])
    elif len(buttons) == 5:
        but.row(buttons[0], buttons[1], buttons[2])
        but.row(buttons[3], buttons[4])
    elif len(buttons) == 6:
        but.row(buttons[0], buttons[1], buttons[2])
        but.row(buttons[3], buttons[4], buttons[5])

    points = types.InlineKeyboardButton(text='Баланс', callback_data='points')
    if Marathon.is_open_reward():
        but2 = types.InlineKeyboardButton(text='Пуговка', callback_data='get_reward')
        but.row(points, but2)
    else:
        but.row(points)
    return but

def get_button_balance():
    but = types.InlineKeyboardMarkup(row_width=3)
    points = types.InlineKeyboardButton(text='Баланс', callback_data='points')
    but.add(points)
    return but

def get_t6_buttons(tg_id, ans1 = None, ans2 = None):
    """
    :param tg_id: - айди пользователя
    :return InlineKeyboardMarkup: - клавиатура
    """
    but = types.InlineKeyboardMarkup()
    for ind, color in enumerate(TASK_6_COLORS):
        if ans1 == ind or ans2 == ind:
            b = types.InlineKeyboardButton(text="{} ✅".format(color), callback_data="color{}".format(ind))
        else:
            b = types.InlineKeyboardButton(text="{}".format(color), callback_data="color{}".format(ind))
        but.add(b)
    return but

def get_t5_buttons(tg_id, ans = None):
    """
    :param tg_id: - айди пользователя
    :return InlineKeyboardMarkup: - клавиатура
    """
    but = types.InlineKeyboardMarkup()
    for ind, item in enumerate(TASK_5_ITEMS):
        if ans == ind:
            b = types.InlineKeyboardButton(text="{} ✅".format(item), callback_data="item{}".format(ind))
        else:
            b = types.InlineKeyboardButton(text="{}".format(item), callback_data="item{}".format(ind))
        but.add(b)
    return but


def get_instruction(bot,user_id,reward):

    reward = reward*2

    bot.send_message(user_id,text=INSTRUCTION_TEXT.format(reward))
    
    img = '/home/app2/instructions/new_instruction.jpg'
    with open(img, "rb") as file:
        data = file.read()
    bot.send_photo(user_id, photo=data,caption='Ваш промокод: {}'.format(reward),reply_markup=get_buttons(user_id))

