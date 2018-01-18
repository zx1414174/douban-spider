import pymysql
from ..Config.ConfigTool import ConfigTool


class MysqlTool:
    """
    数据库操作类
    """
    def __init__(self):
        config = ConfigTool()
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







