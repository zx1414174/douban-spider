import requests
import time
from bs4 import BeautifulSoup
from pyquery import PyQuery
from App.Tool.MysqlTool import MysqlTool


class BookSpider:
    """
    豆瓣读书爬虫类
    """
    __detail_info = {
        '作者:': 'author',
        '出版社:': 'publisher',
        '出版年:': 'publication_year',
        '页数:': 'pages',
        '定价:': 'price',
        '装帧:': 'layout',
        'ISBN:': 'isbn',
    }

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
        doc = self.get_pyquery_doc(url)
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
            pid = self.__mysql_tool.insert('db_book_tag', parent_insert_data)
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
        # 测试写死一个链接
        url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={start}&type=T'
        url = url.format(start=0)
        doc = self.get_pyquery_doc(url)
        list = doc('a.nbg')
        print(list)

    def detail_handler(self, url):
        """
        详情处理
        :param str url:
        :return:
        """
        book_info = dict()
        url = 'https://book.douban.com/subject/26698660/'
        url_response = self.get_url_response(url)
        soup = BeautifulSoup(url_response.text, 'lxml')
        div_doc = soup.select('#info span')
        for i, soup_item in enumerate(div_doc):
            if soup_item.string in self.__detail_info.keys():
                book_info[soup_item.string] = self.detail_info_handler(soup_item)
        book_info['grade'] = soup.select('div.rating_self > strong.rating_num')[0].string.strip(' ')
        book_info['five_graded_percent'] = soup.select('div.rating_wrap > span.stars5')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        book_info['four_graded_percent'] = soup.select('div.rating_wrap > span.stars4')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        book_info['three_graded_percent'] = soup.select('div.rating_wrap > span.stars3')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        book_info['two_graded_percent'] = soup.select('div.rating_wrap > span.stars2')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        book_info['one_graded_percent'] = soup.select('div.rating_wrap > span.stars1')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        print(book_info)

    def detail_info_handler(self, soup_item):
        """
        书籍详情信息模块处理
        :param soup_item:
        :return str:
        """
        method = 'static_detail_info_{param}_handler'
        method = method.format(param=self.__detail_info[soup_item.string])
        return getattr(BookSpider, method)(soup_item)

    @staticmethod
    def static_detail_info_author_handler(soup_item):
        """
        处理书籍作者信息
        :param soup_item:
        :return str:
        """
        return soup_item.next_sibling.next_sibling.string.replace(' ', '').replace('\n', '')

    @staticmethod
    def static_detail_info_publisher_handler(soup_item):
        """
        书籍出版社信息
        :return str:
        """
        return BookSpider.static_detail_info_normal_handler(soup_item)

    @staticmethod
    def static_detail_info_publication_year_handler(soup_item):
        """
        书籍出版年份信息
        :param soup_item:
        :return str:
        """
        return BookSpider.static_detail_info_normal_handler(soup_item)

    @staticmethod
    def static_detail_info_pages_handler(soup_item):
        """
        书籍页数信息
        :param soup_item:
        :return str:
        """
        return BookSpider.static_detail_info_normal_handler(soup_item)

    @staticmethod
    def static_detail_info_price_handler(soup_item):
        """
        书籍价格信息
        :param soup_item:
        :return str:
        """
        return soup_item.next_sibling.strip(' ').replace('元', '')

    @staticmethod
    def static_detail_info_isbn_handler(soup_item):
        """
        书籍isbn信息
        :param soup_item:
        :return str:
        """
        return BookSpider.static_detail_info_normal_handler(soup_item)

    @staticmethod
    def static_detail_info_layout_handler(soup_item):
        """
        书籍装帧信息
        :param soup_item:
        :return str:
        """
        return BookSpider.static_detail_info_normal_handler(soup_item)

    @staticmethod
    def static_detail_info_normal_handler(soup_item):
        """
        书籍信息通用处理方案
        :param soup_item:
        :return str:
        """
        return soup_item.next_sibling.strip(' ')

    def get_pyquery_doc(self, url, headers=''):
        """
        获取pyquery处理doc
        :param str url:
        :param dict headers:
        :return:
        """
        url_response = self.get_url_response(url, headers)
        doc = PyQuery(url_response.text)
        return doc

    def get_url_response(self, url, headers=''):
        """
        获取链接请求文本
        :param str url:
        :param dict headers:
        :return:
        """
        if headers == '':
            headers = self.static_get_headers()
        url_response = requests.get(url, headers=headers)
        return url_response


book_spider = BookSpider()
book_spider.detail_handler('asdf')


