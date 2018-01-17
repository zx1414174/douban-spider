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
        self.__cursor = self.__db.cursor()
