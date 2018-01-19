import requests
import time
from pyquery import PyQuery
from App.Tool.MysqlTool import MysqlTool


class BookSpider:
    """
    豆瓣读书爬虫类
    """
    def __init__(self):
        self.__mysql_tool = ''
        # self.__mysql_tool = MysqlTool()

    @staticmethod
    def static_get_headers():
        """
        获取请求头配置
        :return Dict:
        """
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Cookie': 'bid=ymkWnDhkpU8; gr_user_id=879bd70d-a9f5-4221-be9e-1ef0d3b227b8; _vwo_uuid_v2=56F5845AAF682CCA6AAA6E84C7DECF9F|a9b1c518f8c45aee9f5ccda10c6f1ba3; __yadk_uid=8xXrlsG2IbCkbhiSnhttF4Ui9RQSAQCp; __utmz=30149280.1514881536.2.2.utmcsr=jianshu.com|utmccn=(referral)|utmcmd=referral|utmcct=/p/555e85a29ec7; __utmz=81379588.1514881536.2.2.utmcsr=jianshu.com|utmccn=(referral)|utmcmd=referral|utmcct=/p/555e85a29ec7; __utmc=30149280; __utmc=81379588; viewed="2230208_26698660_25862578_26740503_27138747"; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1515208888%2C%22https%3A%2F%2Fwww.jianshu.com%2Fp%2F555e85a29ec7%22%5D; _pk_id.100001.3ac3=9024db9782721515.1513136377.4.1515208888.1515206167.; _pk_ses.100001.3ac3=*; __utma=30149280.1058233073.1513136377.1515205493.1515208888.4; __utmt_douban=1; __utmb=30149280.1.10.1515208888; __utma=81379588.270456487.1513136377.1515205493.1515208888.4; __utmt=1; __utmb=81379588.1.10.1515208888',
        }

    def tag_spider(self):
        """
        豆瓣热门标签爬取
        :return:
        """
        url = 'https://book.douban.com/tag/?view=type'
        headers = self.static_get_headers()
        url_response = requests.get(url, headers=headers)
        doc = PyQuery(url_response.text)
        div_list = doc('div.article > div:eq(1) > div')
        now_time = time.time()
        for div_item in div_list.items():
            parent_insert_data = dict()
            parent_insert_data['name'] = div_item.children('a').attr('name')
            parent_insert_data['pid'] = 0
            parent_insert_data['url'] = ''
            parent_insert_data['book_count'] = 0
            parent_insert_data['create_time'] = now_time
            parent_insert_data['update_time'] = now_time
            pid = self.__mysql_tool.insert('db_hot_tag', parent_insert_data)
            child_items = div_item.find('table > tbody > tr > td')
            for child_item in child_items.items():
                children_insert_data = dict()
                base_url = 'https://book.douban.com/tag/'
                child_a = child_item.children('a')
                children_insert_data['url'] = base_url + child_a.attr('href')
                children_insert_data['name'] = child_a.text()
                book_count = child_item.children('b').text()
                children_insert_data['book_count'] = book_count[1:-1]
                children_insert_data['pid'] = pid
                children_insert_data['create_time'] = now_time
                children_insert_data['update_time'] = now_time
                self.__mysql_tool.insert('db_hot_tag', children_insert_data)

    def list_handler(self, url):
        """
        热门标签列表处理
        :param str url:
        :return:
        """
        #测试写死一个链接
        url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={start}&type=T'
        url = url.format(start=0)
        headers = self.static_get_headers()
        url_response = requests.get(url, headers=headers)
        doc = PyQuery(url_response.text)
        list = doc('a.nbg')
        print(list)

    def detail_handler(self, url):
        """
        详情处理
        :param str url:
        :return:
        """




book_spider = BookSpider()
book_spider.list_handler('asdf')


