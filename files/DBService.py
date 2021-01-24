import pymysql
from pymysql.cursors import DictCursor
# from User import *

class DBService:
    def __init__ (self):
        self.connection = pymysql.connect(
            host = 'localhost',
            user = 'admin',
            passwd = 'Minecraft_11',
            db = 'pugovka',
            cursorclass = DictCursor
        )
        self.cursor = self.connection.cursor()
        
    def execute(self,query):
        self.cursor.execute(query)
        self.connection.commit()

    def select(self, table_name, col='*', where='1', query=None):
        if query is None:
            query = "SELECT {} FROM {} WHERE {}".format(col,table_name,where)
        self.execute(query)
        return self.cursor


    def insert(self,table_name,data):
        """
        Вставка
        :param table_name:  - имя таблицы
        :param data:        - данные для вставки (dict)
        """
        keys = ","
        keys = keys.join(data.keys())
        values = ','
        values = values.join("'"+str(el)+"'" for el in data.values())
        query = "INSERT INTO {} ({}) VALUES ({})".format(table_name,keys,values)
        self.execute(query)

    def update(self,table_name,data,where=None):
        data = [i + '='+"'"+str(data[i])+"'" for i in data]
        d = ','.join(data)
                
        if where is None:
            query = "UPDATE {} SET {}".format(table_name,d)
        else:
            query = 'UPDATE {} SET {} WHERE {}'.format(table_name,d,where)
        
        self.execute(query)
    
    def close(self):
        self.cursor.close()
        self.connection.close()
