from ..Config import ConfigTool


class MysqlTool:
    """
    数据库操作类
    """
    def __init__(self):
        config = ConfigTool()
        user = config.get_config_value('db.db.user')
        print(user)
        #self.db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='')
        #self.cursor = self.db.cursor()
