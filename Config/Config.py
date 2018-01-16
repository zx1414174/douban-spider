import configparser
class DbConfig:
    """
    数据库配置
    """
    __install = ''
    __config_data = {}

    def __new__(cls, *args, **kwargs):
        """
        单例
        :param args:
        :param kwargs:
        :return: DbConfig
        """
        if cls.__install == '':
            cls.__install = super(DbConfig, cls).__new__(cls)
        return cls.__install

    def __getattr__(self, item):
        item_split = item.split('.')
        file_name = item_split[0]
        option = item_split[1]
        key = item_split[2]
        if file_name not in self.__config_data.keys():
            cf = configparser.ConfigParser()
            self.__config_data[file_name] = cf.read(file_name + '.py')


