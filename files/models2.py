# -*- coding: utf-8 -*-
from DBService import *

class User (object):
    @classmethod
    def is_exist(cls, tg_id):
        """
        :param tg_id: - айди пользователя
        :return True: - уже существует
        :return False:- не существует
        """
        db = DBService()
        
        stat = db.select(
            'user', 
            query = 'SELECT EXISTS (SELECT * FROM user WHERE tg_id = {})'.format(tg_id)
        )

        db.close()

        if str(stat.fetchall()[0]['EXISTS (SELECT * FROM user WHERE tg_id = {})'.format(tg_id)]) == '0':
            return False
        else:
            return True

    @classmethod
    def finish_task(cls, tg_id, task):
        """
        выполняет задание пользователю
        :param tg_id: - айди пользователя
        :param task:  - номер задания
        """
        db = DBService()
        stat = db.select(
            'user', 
            'tasks_status',
            'tg_id = {}'.format(tg_id)
        )
        
        stat = stat.fetchall()

        s = stat[0]['tasks_status']
        
        if task != 3:
            data = s[:task - 1] + '1' + s[task:]
        else:
            data = s[:task-1] + str(int(s[task-1])+1) + s[task:]

        db.update(
            'user',
            {'tasks_status' : data},
            'tg_id = {}'.format(tg_id)
        )

        db.close()
    
    @classmethod
    def set_t6_status(cls, tg_id, stat):
        """
        :param tg_id: - айди пользователя
        :param stat: - статус
        """
        db = DBService()
        db.update(
            'user', 
            {'t6_status' : stat}, 
            'tg_id = {}'.format(tg_id)
        )
        db.close()
        
    @classmethod
    def get_t6_status(cls, tg_id):
        """
        -1 - нет первогого голоса, иначе хранит первый голос
        :param tg_id: - айди пользователя
        :return int: - статус 6 задания
        """
        db = DBService()
        stat = db.select(
            'user',
            't6_status',
            'tg_id = {}'.format(tg_id)
        )
        db.close()

        for i in stat:
            res = i['t6_status']

        return res

    @classmethod
    def add_points(cls, tg_id, points):
        """
        выполняет задание пользователю
        :param tg_id: - айди пользователя
        :param points:- инкремент баланса
        """
        db = DBService()
        db.select(
            'user',
            query = "update user set points = points + {} where tg_id = {}".format(points, tg_id)
        )
        db.close()
        
    @classmethod
    def create(cls, tg_id):
        """
        добавляет пользователя в бд
        :param tg_id: - айди пользователя
        """ 
        db = DBService()
        db.insert(
            'user', 
            { 'tg_id' : tg_id}
        )
        db.close()
    
    @classmethod
    def is_task_finished(cls, tg_id, task):
        """
        :param tg_id: - айди пользователя
        :param task:  - номер задания
        :return True: - задание выполнено
        :return False:- задание не выполнено
        """
        db = DBService()
        stat = db.select(
            'user', 
            'tasks_status', 
            'tg_id = {}'.format(tg_id)
        )
        db.close()  

        stat = stat.fetchall()

        if task != 3:
            if stat[0]['tasks_status'][task - 1] == '0':
                return False
            else:
                return True
        else:
            if int(stat[0]['tasks_status'][task-1]) < 5:
                return False
            else:
                return True
    @classmethod
    def t3_is_finished(cls,user_id):
        db = DBService()
        tasks = db.select('user',query='SELECT tasks_status FROM user WHERE tg_id={}'.format(user_id))
        db.close()
        for i in tasks:
            if i['tasks_status'][2] == '0':
                return False
            else:
                return True
    



        

    @classmethod
    def finish_marathon(cls):
        """
        заканчивает марафон для всех
        """
        db = DBService()
        users = db.update(
            'user', 
            {'win' : 1}, 
            'win = 0'
        )
        db.close()


    @classmethod
    def is_win(cls, tg_id):
        """
        :param tg_id: - айди пользователя
        :return True: - если уже участвовал
        :return False:- ещё не участвовал
        """
        db = DBService()
        res = db.select(
            'user', 
            'win', 
            'tg_id = {}'.format(tg_id)
        )

        stat = res.fetchall()
        if str(stat[0]['win']) == '0':
            return False
        else:
            return True

    @classmethod
    def get_balance(cls, tg_id):
        """
        :param tg_id: - айди пользователя
        :return int: - баланс
        """
        db = DBService()
        bal = db.select(
            'user', 
            'points', 
            'tg_id = {}'.format(tg_id)
        )
        db.close()

        b = bal.fetchall()

        return b[0]['points']

    @classmethod
    def get_members_id(cls):
        """
        :return list: - айди участников
        """
        db = DBService()
        res = db.select(
            'user',
            'tg_id', 
            'win = 0'
        )
        db.close()

        return res.fetchall()
    @classmethod
    def delete_user(cls,tg_id):
        """
        param tg_id: телеграм айди юзера
        function deletes user from database
        """
        db = DBService()
        db.select('user',
        query='DELETE FROM user WHERE tg_id = {}'.format(tg_id)
        )
        db.close()

class Marathon (object):
    @classmethod
    def get_link(cls):
        """
        :return str: - ссылка на марафон
        """
        db = DBService()
        link = db.select(
            'marathon', 
            'link', 
            'status = 0' 
        )
        db.close()

        for i in link:
            k = i['link']
            
        return k

    @classmethod
    def start(cls, link):
        """
        начинает новый марафон
        """
        db = DBService()
        db.insert(
            'marathon', 
            {'link' : link}, 
        )
        db.close()

    

    @classmethod
    def open_reward(cls):
        db = DBService()
        db.update('marathon',
        {'reward':1},
        'status = 0')
        db.close()
        

    @classmethod
    def is_open_reward(cls):
        db = DBService()
        rew = db.select('marathon',query='SELECT reward FROM marathon ORDER BY id DESC LIMIT 0, 1')
        db.close()
        for i in rew:
            if i['reward'] == 1:
                return True
            else:
                return False

    @classmethod
    def finish(cls):
        """
        заканчивает марафон
        """
        db = DBService()
        db.update(
            'marathon', 
            {'status' : 1}, 
            'status = 0'            
        )
        db.close()

    @classmethod
    def get_task_link(cls,task):
        db = DBService()
        link = db.select('marathon', query='SELECT t{}_link FROM marathon ORDER BY id DESC LIMIT 0, 1'.format(task))
        db.close()
        for i in link:
            return i['t{}_link'.format(task)]

    @classmethod
    def is_active(cls):
        """
        :return True: - если марафон идёт
        :return False:- ещё не начался
        """
        db = DBService()
        stat = db.select(
            'marathon', 
            query = "SELECT status FROM marathon ORDER BY id DESC LIMIT 0, 1"
        )
        db.close()
        
        if str(stat.rowcount) == '0':
            return False
        
        stat = stat.fetchall()
        
        if stat[0]['status'] == 1:
            return False
        elif stat[0]['status'] == 0:
            return True
    
    @classmethod
    def get_t_available(cls):
        """
        :return int: - номер задания
        """
        db = DBService()
        res = db.select(
            'marathon', 
            query = "SELECT t_available FROM marathon ORDER BY id DESC LIMIT 0, 1"
        )
        db.close()

        stat = res.fetchall()

        return stat[0]['t_available']
        
    @classmethod
    def is_task_opened(cls, task):
        """
        :param task: - номер задания
        :return True: - доступно
        :return False: - не доступно
        """
        return cls.get_t_available() >= task

    @classmethod
    def open_task(cls, task):
        """
        открывает задание в бд
        :param task: - номер задания
        """
        db = DBService()
        db.update(
            'marathon', 
            {'t_available' : task},
            'status = 0'
        )
        db.close()

    @classmethod
    def set_task_link(cls, task, link):
        """
        :param task: - номер задания
        :param link: - ссылка
        """
        db = DBService()
        db.update(
            'marathon', 
            {'t{}_link'.format(task) : link}, 
            'status = 0'
        )
        db.close()


        