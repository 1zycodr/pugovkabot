# -*- coding: utf-8 -*-
import telebot, json
from telebot import types
from models2 import User, Marathon
from utils2 import *
from flask import Flask, request, jsonify
import requests 
TOKEN = '1218173285:AAHDGQPjL3g610h-AxPcwldCuYSFUD3pvQc'

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

@bot.message_handler(commands=['bot_init'])
def init_message(message):
    if message.chat.type == 'group':
        bot.send_message(message.chat.id, 'Чат {} зарегестрирован как чат администраторов.'.format(message.chat.title))

@bot.message_handler(commands=['deleteMe'])
def delete_user(message):
    if User.is_exist(message.from_user.id):
        User.delete_user(message.from_user.id)
        bot.send_message(message.from_user.id,'Вы были удалены с марафона\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot')

@bot.message_handler(commands=['start'])
def start_message(message):
    if not message.chat.type == 'group':
        if Marathon.is_active():
            if User.is_exist(message.from_user.id):
                if User.is_win(message.from_user.id):
                    bot.send_message(message.chat.id, 'Здравствуйте! Вы уже участвовали в марафоне.')
                else:
                    img = '/home/app2/images/ШТУЛУЧКА.jpg'
                    with open(img, "rb") as file:
                        data = file.read()
                    bot.send_message(message.chat.id, HELLO_MESSAGE.format(message.from_user.first_name, Marathon.get_link()))
                    bot.send_photo(message.from_user.id, photo=data, reply_markup=get_buttons(message.from_user.id))
            else:
                User.create(message.from_user.id)
                img = '/home/app2/images/ШТУЛУЧКА.jpg'
                with open(img, "rb") as file:
                    data = file.read()
                bot.send_message(message.chat.id, HELLO_MESSAGE.format(message.from_user.first_name, Marathon.get_link()))
                bot.send_photo(message.from_user.id, photo=data, reply_markup=get_buttons(message.from_user.id))
                if Marathon.is_task_opened(5):
                    bot.send_message(message.from_user.id, 'ВАШЕ ДОМАШНЕЕ ЗАДАНИЕ\n({})\n\n{} Жду Ваши ответы!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(5), TASK_TEXT[5]), reply_markup=get_buttons(message.from_user.id))
                    img = '/home/app2/images/z5.jpg'
                    with open(img, "rb") as file:
                        data = file.read()
                    bot.send_message(message.from_user.id, 'Выбери свой вариант:')
                    bot.send_photo(message.from_user.id, photo=data, reply_markup=get_t5_buttons(message.from_user.id))
                if Marathon.is_task_opened(6):
                    bot.send_message(message.from_user.id, 'ВАШЕ ДОМАШНЕЕ ЗАДАНИЕ\n({})\n\n{}Жду Ваши фантазийные названия!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(6), TASK_TEXT[6]), reply_markup=get_buttons(message.from_user.id))
                    img = '/home/app2/images/z6.jpg'
                    with open(img, "rb") as file:
                        data = file.read()
                    bot.send_message(message.from_user.id, 'Выбери свой вариант:')
                    bot.send_photo(message.from_user.id, photo=data, reply_markup=get_t6_buttons(message.from_user.id))
        else:
            bot.send_message(message.chat.id, 'Здравствуйте! Марафон ещё не начался!')

@bot.message_handler(content_types=['text'])
def text_message(message):
    if message.chat.type == 'group':
        # управление админами
        # #старт <ссылка>
        # #стоп
        # #задание1 <ссылка>
        # #задание2 <ссылка>
        # #задание3 <ссылка>
        # #задание4 <ссылка>
        # #задание5 <ссылка>
        # #задание6 <ссылка>
        user_status = bot.get_chat_member(message.chat.id, message.from_user.id).status
        if  user_status in ['creator', 'administrator']:
            mes = get_adm_mes_type(message.text)
            if mes is not None:
                if mes.type == MessageType.open_task:
                    if Marathon.is_active():
                        cur_task = Marathon.get_t_available()
                        if not (mes.task >= 1 and mes.task <= 6):
                            bot.send_message(message.chat.id, 'Некорректный номер задания! Доступны 1 - 6 задания.')
                        if cur_task == mes.task - 1:
                            Marathon.open_task(mes.task)
                            Marathon.set_task_link(mes.task, mes.link)
                            bot.send_message(message.chat.id, 'Задание {} было открыто с ссылкой {}'.format(mes.task, mes.link))
                            mar_members = User.get_members_id()
                            if mes.task == 5:
                                img = '/home/app2/images/z5.jpg'
                                with open(img, "rb") as file:
                                    data = file.read()
                            elif mes.task == 6:
                                img = '/home/app2/images/z6.jpg'
                                with open(img, "rb") as file:
                                    data = file.read()
                            for member in mar_members:
                                try:
                                    if mes.task <= 4:
                                        bot.send_message(member['tg_id'], 'Вышло {} задание марафона!\n\n{}\nСсылка на пост:\n{}\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(mes.task, TASK_TEXT[mes.task], mes.link), reply_markup=get_buttons(member['tg_id']))
                                    if mes.task == 5:
                                        bot.send_message(member['tg_id'], 'ВАШЕ ДОМАШНЕЕ ЗАДАНИЕ\n({})\n\n{} Жду Ваши ответы!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(mes.link, TASK_TEXT[5]), reply_markup=get_buttons(member['tg_id']))
                                        print('sended to ' + str(member['tg_id']))
                                        bot.send_message(member['tg_id'], 'Выбери свой вариант:')
                                        bot.send_photo(member['tg_id'], photo=data, reply_markup=get_t5_buttons(member['tg_id']))
                                    elif mes.task == 6:
                                        bot.send_message(member['tg_id'], 'ВАШЕ ДОМАШНЕЕ ЗАДАНИЕ\n({})\n\n{}Жду Ваши фантазийные названия!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(mes.link, TASK_TEXT[6]), reply_markup=get_buttons(member['tg_id']))
                                        
                                        bot.send_message(member['tg_id'], 'Выбери свой вариант:')
                                        bot.send_photo(member['tg_id'], photo=data, reply_markup=get_t6_buttons(member['tg_id']))
                                except:
                                    print('Failed to send to ' + str(member['tg_id']))
                        elif cur_task > mes.task - 1:
                            bot.send_message(message.chat.id, 'Задание {} уже было открыто!'.format(mes.task))
                        else:
                            bot.send_message(message.chat.id, 'Сначала откройте задание {}!'.format(cur_task + 1))
                    else:
                        bot.send_message(message.chat.id, 'Сначала запустите марафон командой #старт!')
                elif mes.type == MessageType.start_marathon:
                    if Marathon.is_active():
                        bot.send_message(message.chat.id, 'Сначала закончите предыдущий марафон!')
                    else:
                        Marathon.start(mes.link)
                        bot.send_message(message.chat.id, 'Это старт марафона с ссылкой {}'.format(mes.link))
                elif mes.type == MessageType.finish_marathon:
                    Marathon.finish()
                    bot.send_message(message.chat.id, 'Марафон был закончен!')
                    mar_members = User.get_members_id()
                    User.finish_marathon()
                    for member in mar_members:
                        bot.send_message(member['tg_id'], 'Марафон завершён. Спасибо за участие!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot')
        else:
            bot.send_message(message.chat.id, 'Вам нужно быть администратором, чтобы отправлять мне команды!')
    elif Marathon.is_active():
        # обрабатываем данные от пользователя
        # #привет   
        # #цель
        # #миф
        # #инсайт
        # секретные слова:
            # з1 - zgEnCQ7~LG
            # з2 - Jp~Bt}xPFP
            # з3 - y~rNV3Vn~1
            # з4 - hb5DrmF{5E
            # з5 - 6C5pTjzegZ
            # з6 - hs76sPA%ZV
        if User.is_exist(message.from_user.id):
            if not User.is_win(message.from_user.id):
                task = get_user_mes_type(message.text)
                if task is not None:
                    if Marathon.is_task_opened(task):
                        if not User.is_task_finished(message.from_user.id, task):
                            User.finish_task(message.from_user.id, task)
                            if task >= 1 and task <= 4:
                                if task == 3:
                                    User.add_points(message.from_user.id, 1)
                                elif task ==4:
                                    User.add_points(message.from_user.id,10)
                                else:
                                    User.add_points(message.from_user.id, 5)
                                if task == 1:
                                    img = '/home/app2/images/1.jpg'
                                    with open(img, "rb") as file:
                                        data = file.read()
                                    bot.send_message(message.from_user.id, TASK_FINISH_MESSAGES[0])
                                    bot.send_photo(message.from_user.id, photo=data, reply_markup=get_button_balance())
                                elif task == 2:
                                    img = '/home/app2/images/2.jpg'
                                    with open(img, "rb") as file:
                                        data = file.read()
                                    bot.send_message(message.from_user.id, TASK_FINISH_MESSAGES[1])
                                    bot.send_photo(message.from_user.id, photo=data, reply_markup=get_button_balance())
                                elif task == 3:
                                    img = '/home/app2/images/3.jpg'
                                    with open(img, "rb") as file:
                                        data = file.read()
                                    bot.send_message(message.from_user.id, TASK_FINISH_MESSAGES[2])
                                    bot.send_photo(message.from_user.id, photo=data, reply_markup=get_button_balance())
                                elif task == 4:
                                    img = '/home/app2/images/4.jpg'
                                    with open(img, "rb") as file:
                                        data = file.read()
                                    bot.send_message(message.from_user.id, TASK_FINISH_MESSAGES[3].format(name=message.from_user.first_name))
                                    bot.send_photo(message.from_user.id, photo=data, reply_markup=get_button_balance())
                elif message.text.lower() in ['пуговка', 'пугавка', 'пуговица', 'пугавица', 'пуговки']:
                    bal = User.get_balance(message.from_user.id)
                    if bal <= 5:
                        bot.send_message(message.from_user.id, 'К сожалению, у Вас пока мало пуговок для получения скидки.\n Нажмите на кнопку "Баланс" и узнайте, какие задания Вам надо выполнить, чтобы набрать больше пуговок!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot', reply_markup=get_buttons(message.from_user.id))
                    elif bal <= 6 and bal >= 15:
                        bot.send_message(message.from_user.id, "У вас {} пуговок! Вы можете воспользоваться скидкой в 150 рублей на обучение в моей онлайн-школе. Для этого:".format(bal))
                        get_instruction(bot,message.from_user.id,'150')
                    elif bal >= 16 and bal <= 39:
                        bot.send_message(message.from_user.id, 'У Вас {} пуговок! Вы можете воспользоваться скидкой в 200 рублей на обучение в моей онлайн-школе. Для этого:'.format(bal))
                        get_instruction(bot,message.from_user.id,'200')
                    elif bal >= 40:
                        bot.send_message(message.from_user.id, 'У Вас {} пуговок! Вы можете воспользоваться скидкой в 300 рублей на обучение в моей онлайн-школе. Для этого:'.format(bal))
                        get_instruction(bot,message.from_user.id ,'300')
    else:
        bot.send_message(message.chat.id, 'Здравствуйте! Марафон ещё не начался!')



@bot.callback_query_handler(func=lambda call: True)
def user_chat(call):
    if User.is_exist(call.from_user.id):
        if not User.is_win(call.from_user.id):
            if call.data == 't1':
                if User.is_task_finished(call.from_user.id, 1):
                    bot.send_message(call.message.chat.id, 'Предварительное задание "Знакомство".\n\n✅ ВЫПОЛНЕНО.\n\n👉🏼 {}\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(1)), reply_markup=get_buttons(call.from_user.id))
                else:
                    bot.send_message(call.message.chat.id, 'Это задание ещё не выполнено. Перейдите по ссылке {}, прочитайте задание и выполните его, чтобы заработать пуговки!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(1)), reply_markup=get_buttons(call.from_user.id))
            elif call.data == 't2':
                if User.is_task_finished(call.from_user.id, 2):
                    bot.send_message(call.message.chat.id, 'Предварительное задание "Цели".\n\n✅ ВЫПОЛНЕНО.\n\n👉🏼 {}\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(2)), reply_markup=get_buttons(call.from_user.id))
                else:
                    bot.send_message(call.message.chat.id, 'Это задание ещё не выполнено. Перейдите по ссылке {}, прочитайте задание и выполните его, чтобы заработать пуговки!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(2)), reply_markup=get_buttons(call.from_user.id))
            elif call.data == 't3':
                if User.is_task_finished(call.from_user.id, 3):
                    bot.send_message(call.message.chat.id, 'Предварительное задание "Миф".\n\n✅ ВЫПОЛНЕНО.\n\n👉🏼 {}\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(3)), reply_markup=get_buttons(call.from_user.id))
                else:
                    bot.send_message(call.message.chat.id, 'Это задание ещё не выполнено. Перейдите по ссылке {}, прочитайте задание и выполните его, чтобы заработать пуговки!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(3)), reply_markup=get_buttons(call.from_user.id))
            elif call.data == 't4':
                if User.is_task_finished(call.from_user.id, 4):
                    bot.send_message(call.message.chat.id, 'Основное задание "ДЗ1".\n\n✅ ВЫПОЛНЕНО.\n\n👉🏼 {}\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(4)), reply_markup=get_buttons(call.from_user.id))
                else:
                    bot.send_message(call.message.chat.id, 'Это задание ещё не выполнено. Перейдите по ссылке {}, прочитайте задание и выполните его, чтобы заработать пуговки!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(4)), reply_markup=get_buttons(call.from_user.id))
            elif call.data == 't5':
                if User.is_task_finished(call.from_user.id, 5):
                    bot.send_message(call.message.chat.id, 'Основное задание "ДЗ2".\n\n✅ ВЫПОЛНЕНО.\n\n👉🏼 {}\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(5)), reply_markup=get_buttons(call.from_user.id))
                else:
                    bot.send_message(call.message.chat.id, 'Это задание ещё не выполнено. Перейдите по ссылке {}, прочитайте задание и выполните его, чтобы заработать пуговки!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(5)), reply_markup=get_buttons(call.from_user.id))
            elif call.data == 't6':
                if User.is_task_finished(call.from_user.id, 6):
                    bot.send_message(call.message.chat.id, 'Основное задание "ДЗ3".\n\n✅ ВЫПОЛНЕНО.\n\n👉🏼 {}\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(6)), reply_markup=get_buttons(call.from_user.id))
                else:
                    bot.send_message(call.message.chat.id, 'Это задание ещё не выполнено. Перейдите по ссылке {}, прочитайте задание и выполните его, чтобы заработать пуговки!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(Marathon.get_task_link(6)), reply_markup=get_buttons(call.from_user.id))
            elif call.data == 'points':
                bal = User.get_balance(call.from_user.id)
                if bal < 41:
                    bot.send_message(call.message.chat.id, 'У Вас на счету: {} пуговок\n\nПродолжайте собирать пуговки для получения скидки и бонусного курса по кедам. Для этого, нужно выполнять все задания, которые показаны внизу.\n\n✅ Зеленая кнопка - задание выполнено. \n❌ Красная кнопка - задание не выполнено.\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(User.get_balance(call.from_user.id)), reply_markup=get_buttons(call.from_user.id))
                else:
                    bot.send_message(call.message.chat.id, 'У Вас на счету: {} пуговок\n\nВаш бонусный курс по кедам »\nhttps://yadi.sk/d/GCgydsVp3QxH2e. Вас ждёт ещё хорошая скидка на основное обучение в моей школе. Проверьте, выполнили ли Вы все задания.\n\n✅ Зеленая кнопка - задание выполнено. \n❌ Красная кнопка - задание не выполнено.\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot'.format(User.get_balance(call.from_user.id)), reply_markup=get_buttons(call.from_user.id))

            elif call.data == 'get_reward':
                bal = User.get_balance(call.from_user.id)
                if bal <= 5:
                    bot.send_message(call.message.chat.id, 'К сожалению, у Вас пока мало пуговок для получения скидки.\n Нажмите на кнопку "Баланс" и узнайте, какие задания Вам надо выполнить, чтобы набрать больше пуговок!\n————\nЕсли возникнут вопросы, можете задавать сюда: @mdolls1bot', reply_markup=get_buttons(call.from_user.id))
                elif bal <= 6 and bal >= 15:
                    bot.send_message(call.from_user.id, "У вас {} пуговок! Вы можете воспользоваться скидкой в 150 рублей на обучение в моей онлайн-школе. Для этого:".format(bal))
                    get_instruction(bot,call.from_user.id,'150')
                elif bal >= 16 and bal <= 39:
                    bot.send_message(call.message.chat.id, 'У Вас {} пуговок! Вы можете воспользоваться скидкой в 200 рублей на обучение в моей онлайн-школе. Для этого:'.format(bal))
                    get_instruction(bot,call.from_user.id,'200')
                elif bal >= 40:
                    bot.send_message(call.message.chat.id, 'У Вас {} пуговок! Вы можете воспользоваться скидкой в 300 рублей на обучение в моей онлайн-школе. Для этого:'.format(bal))
                    get_instruction(bot,call.from_user.id ,'300')
                # elif bal >= 40:
                #     bot.send_message(call.message.chat.id, 'У тебя {} пуговок! Тут получаем награду в зависимости от кол-ва пуговок. (ссылка4)'.format(bal), reply_markup=get_buttons(call.from_user.id))
                #     get_instruction(message.from_user.id,'150')

            elif 'item' in call.data:
                ind = int(call.data[4])
                if not User.is_task_finished(call.from_user.id, 5):
                    User.finish_task(call.from_user.id, 5)
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=get_t5_buttons(call.from_user.id, ind))
                    bot.send_message(call.message.chat.id, TASK_FINISH_MESSAGES[4].format(name=call.from_user.first_name))
                    img = '/home/app2/images/5.jpg'
                    with open(img, "rb") as file:
                        data = file.read()
                    bot.send_photo(call.message.chat.id, photo=data, reply_markup=get_buttons(call.from_user.id))
                    User.add_points(call.from_user.id, 10)
                else:
                    c = False
                    for j, i in enumerate(dict(call.message.json)['reply_markup']['inline_keyboard']):
                        if i[0]['text'][-1] == '✅':
                            if j != ind:
                                c = True
                                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=get_t5_buttons(call.from_user.id, ind))
                    if not c:
                        User.finish_task(call.from_user.id, 5)
            elif 'color' in call.data:
                ind = int(call.data[5])
                if not User.is_task_finished(call.from_user.id, 6):
                    prev_goloc = User.get_t6_status(call.from_user.id)
                    if prev_goloc == -1:
                        User.set_t6_status(call.from_user.id, ind)
                        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=get_t6_buttons(call.from_user.id, ind))
                    elif prev_goloc != ind:
                        User.finish_task(call.from_user.id, 6)
                        User.add_points(call.from_user.id, 10)
                        img = '/home/app2/images/6.jpg'
                        with open(img, "rb") as file:
                            data = file.read()
                        bot.send_message(call.message.chat.id, TASK_FINISH_MESSAGES[5].format(name=call.from_user.first_name))
                        bot.send_photo(call.message.chat.id, photo=data, reply_markup=get_buttons(call.from_user.id))
                        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=get_t6_buttons(call.from_user.id, ind, prev_goloc))
                else:
                    b1 = b2 = None
                    for j, i in enumerate(dict(call.message.json)['reply_markup']['inline_keyboard']):
                        if i[0]['text'][-1] == '✅':
                            if b1 is None:
                                b1 = j
                            else:
                                b2 = j
                                break
                    if b1 != ind and b2 != ind:
                        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=get_t6_buttons(call.from_user.id, b1, ind))

        else:
            bot.send_message(call.message.chat.id, 'Марафон ещё не начался!')
    else:
        bot.send_message(call.message.chat.id, 'Марафон ещё не начался!')

def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://www.pugovkabot.ru/'+TOKEN)
    return '!', 200
    
@server.route('/'+TOKEN, methods=['POST', 'GET'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))]) 
    return '!', 200

if __name__ == '__main__':
    #webhook()
    server.run(
        host='213.139.208.120',
	    port=88
    )




