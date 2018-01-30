import pymysql
from ..Config.ConfigTool import ConfigTool
from .Builder import Builder


class MysqlTool:
    """
    数据库操作类
    """
    # 查询表名
    __table = ''
    # 表主键名
    __primary_key = 'id'
    # 查询构造器
    __builder = None

    def __init__(self):
        config = ConfigTool()
        self.__builder = Builder()
        host = config.get_config_value('mysql.db.host')
        user = config.get_config_value('mysql.db.user')
        password = config.get_config_value('mysql.db.password')
        port = int(config.get_config_value('mysql.db.port'))
        db = config.get_config_value('mysql.db.db')
        self.__db = pymysql.connect(host=host, user=user, password=password, port=port, db=db)
        self.__db.set_charset('utf8')
        self.__cursor = self.__db.cursor()
        self.__cursor.execute('SET NAMES utf8;')
        self.__cursor.execute('SET CHARACTER SET utf8;')
        self.__cursor.execute('SET character_set_connection=utf8;')

    def insert(self, table, data):
        """
        插入数据
        :param str table:表名
        :param dict data:插入数据
        :return:
        """
        keys = data.keys()
        key_string = ','.join(keys)
        # 拼接%s
        value_string = '%s,' * len(data)
        value_string = value_string[:-1]
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=key_string, values=value_string)
        try:
            result = self.__cursor.execute(sql, tuple(data.values()))
            self.__db.commit()
            return result
        except Exception:
            self.__db.rollback()
            return False

    def count(self):
        """
        表数据数量
        :return:
        """
        sql = 'select count({primary_key}) as mysql_total from {table} {where}'.\
            format(primary_key=self.__primary_key, table=self.__table, where=self.__builder).strip(' ')
        try:
            self.__cursor.execute(sql)
            row = self.__cursor.fetchone()
            return row['mysql_total']
        except:
            return False

    def exit(self):
        """
        是否存在数据
        :return:
        """
        count = self.count()
        if count > 0:
            return True
        return False

    def sql(self, sql_str):
        """
        设置 查询sql
        :param sql_str:
        :return:
        """
        self.__builder.sql(sql_str)
        return self

    def set_table(self, table):
        """
        设置表名
        :param table:
        :return:
        """
        self.__table = table
        return self









