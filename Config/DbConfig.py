class DbConfig:
    """
    数据库配置
    """
    HOST = ''
    USER = ''
    PASSWORD = ''
    PORT = ''
    DB = ''

    @staticmethod
    def getStaticConfig(key):
        """
        获取动态配置
        :param key:
        :return: string
        """
        return DbConfig.key


