import mysql.connector
from sqlalchemy import create_engine


class Db:

    def __init__(self):
        self.host = 'ironhack.c1wtctuqirxg.eu-central-1.rds.amazonaws.com'
        self.port = '3306'
        self.user = 'final_admin'
        self.password = 'GBL7CG93bgc4!jT%'
        self.database = 'final_project'

    def connect(self):
        cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.database
        )
        return cnx

    def create_cursor(self, cnx):
        return cnx.cursor(dictionary=True)

    def close_connection(self,cnx):
        cnx.close()

    def select(self, query, all=True):
        cnx = self.connect()
        cx = self.create_cursor(cnx)
        cx.execute(query)
        if all:
            q_result = cx.fetchall()
        else:
            q_result = cx.fetchone()
        self.close_connection(cnx)
        return q_result

    def insert(self, query, val):
        cnx = self.connect()
        cx = self.create_cursor(cnx)
        cx.execute(query, val)
        cnx.commit()
        inserted_rows = cx.rowcount
        self.close_connection(cnx)
        return inserted_rows

    def update(self, query, val):
        cnx = self.connect()
        cx = self.create_cursor(cnx)
        cx.execute(query, val)
        cnx.commit()
        updated_rows = cx.rowcount
        self.close_connection(cnx)
        return updated_rows
