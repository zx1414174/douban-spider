import pymysql
from Config import Config


class MysqlTool:
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='')
        self.cursor = self.db.cursor()
