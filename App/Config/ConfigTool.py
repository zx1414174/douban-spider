import configparser
import os


class ConfigTool:
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
            cls.__install = super(ConfigTool, cls).__new__(cls)
        return cls.__install

    def get_config_value(self, item):
        item_split = item.split('.')
        file_name = item_split[0]
        option = item_split[1]
        key = item_split[2]
        if file_name not in self.__config_data.keys():
            cf = configparser.ConfigParser()
            # 获取文件绝对路径
            config_path = os.path.dirname(__file__) + '/' + file_name + '.conf'
            cf.read(config_path)
            self.__config_data[file_name] = cf
        return self.__config_data[file_name].get(option, key)


