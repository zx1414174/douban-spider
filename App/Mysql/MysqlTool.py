import pymysql
from App.Config.ConfigTool import ConfigTool
from App.Tool.Builder import Builder


class MysqlTool:
    """
    数据库操作类
    """
    # 查询表名
    _table = ''
    # 表前缀
    _prefix_table = ''
    # 表主键名
    _primary_key = 'id'
    # 查询构造器
    __builder = None

    def __init__(self):
        con_data = MysqlTool.static_get_connect_data()
        self.__builder = Builder()
        self.__db = pymysql.connect(**con_data)
        self.__cursor = self.__db.cursor(pymysql.cursors.DictCursor)
        MysqlTool.static_language_handler(self.__db, self.__cursor)

    @staticmethod
    def static_get_connect_data():
        """
        获取连接配置信息
        :return:
        """
        config = ConfigTool()
        con_data = dict()
        con_data['host'] = config.get_config_value('mysql.db.host')
        con_data['user'] = config.get_config_value('mysql.db.user')
        con_data['password'] = config.get_config_value('mysql.db.password')
        con_data['port'] = int(config.get_config_value('mysql.db.port'))
        con_data['db'] = config.get_config_value('mysql.db.db')
        return con_data

    @staticmethod
    def static_language_handler(db, cursor):
        """
        数据库语言处理
        :param db:
        :param cursor:
        :return:
        """
        db.set_charset('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')

    def get_table_name(self):
        return self._prefix_table + self._table

    def insert(self, data):
        """
        插入数据
        :param dict data:插入数据
        :return:
        """
        table = self.get_table_name()
        keys = data.keys()
        key_string = ','.join(keys)
        # 拼接%s
        value_string = '%s,' * len(data)
        value_string = value_string[:-1]
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'\
            .format(table=table, keys=key_string, values=value_string)
        try:
            self.__cursor.execute(sql, tuple(data.values()))
            last_id = self.__cursor.lastrowid
            self.__db.commit()
            return last_id
        except Exception:
            self.__db.rollback()
            return False

    def count(self):
        """
        表数据数量
        :return:
        """
        table = self.get_table_name()
        sql = 'select count({primary_key}) as mysql_total from {table} {where}'\
            .format(primary_key=self._primary_key, table=table, where=self.__builder.build()).strip(' ')
        try:
            self.__cursor.execute(sql)
            row = self.__cursor.fetchone()
            return row['mysql_total']
        except:
            return False

    def find(self):
        """
        查找单条数据
        :return tuple:
        """
        table = self.get_table_name()
        sql = 'select * from {table} {where}'\
            .format(table=table, where=self.__builder.build()).strip(' ')
        try:
            self.__cursor.execute(sql)
            row = self.__cursor.fetchone()
            return row
        except:
            return False

    def get(self):
        """
        获取多条数据
        :return tuple:
        """
        sql = 'select * from {table} {where}'\
            .format(table=self.get_table_name(), where=self.__builder.build()).strip(' ')
        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            return results
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

    def search_sql(self, sql_str):
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









