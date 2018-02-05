import requests
import time
from urllib.parse import urlencode
import random
from bs4 import BeautifulSoup
from pyquery import PyQuery
from App.Tool.MysqlTool import MysqlTool


class BookSpider:
    """
    豆瓣读书爬虫类
    """
    __detail_info = {
        '作者:': 'author',
        '作者': 'author',
        '出版社:': 'publisher',
        '出版年:': 'publication_year',
        '页数:': 'pages',
        '定价:': 'price',
        '装帧:': 'layout',
        'ISBN:': 'isbn',
    }

    def __init__(self):
        # self.__mysql_tool = ''
        self.__mysql_tool = MysqlTool()

    @staticmethod
    def static_get_headers():
        """
        获取请求头配置
        :return Dict:
        """
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Referer': 'https://book.douban.com/',
            'Host': 'book.douban.com',
            'Cookie': 'bid=ymkWnDhkpU8; gr_user_id=879bd70d-a9f5-4221-be9e-1ef0d3b227b8; _vwo_uuid_v2=56F5845AAF682CCA6AAA6E84C7DECF9F|a9b1c518f8c45aee9f5ccda10c6f1ba3; __yadk_uid=8xXrlsG2IbCkbhiSnhttF4Ui9RQSAQCp; ap=1; ct=y; ll="108169"; __utmc=30149280; __utmz=30149280.1517625096.21.8.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmc=81379588; __utmz=81379588.1517625096.21.8.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=5dd46054-be0e-44a4-acb9-a9964ac04558; gr_cs1_5dd46054-be0e-44a4-acb9-a9964ac04558=user_id%3A0; __utma=30149280.1058233073.1513136377.1517820579.1517825577.26; __utma=81379588.270456487.1513136377.1517820579.1517825577.25; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1517825577%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; viewed="4820710_5431784_26431618_3826899_25779593_27025036_26680113_1456692_2257283_26963900"; __utmt_douban=1; __utmb=30149280.6.10.1517825577; __utmt=1; __utmb=81379588.6.10.1517825577; _pk_id.100001.3ac3=9024db9782721515.1513136377.27.1517827998.1517823290.',
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

    def book_spider(self):
        """
        爬取豆瓣书籍
        :return:
        """
        tag_list = self.__mysql_tool.set_table('db_book_tag').get()
        for tag in tag_list:
            if tag['url'] != '':
                url = tag['url'].replace('tag//tag', 'tag')
                self.list_handler(url, tag['id'])

    def list_handler(self, url, tag_id):
        """
        热门标签列表处理
        :param str url:
        :param int tag_id:
        :return:
        """
        # 测试写死一个链接
        url = url.strip('/')
        is_end = False
        start = 0
        now_time = time.time()
        while not is_end:
            param = '?start={start}&type=T'.format(start=start)
            page_url = url + param
            doc = self.get_pyquery_doc(page_url)
            detail_doc_list = doc('ul.subject-list > li > div.info > h2 a')
            is_end = True
            for detail_item in detail_doc_list.items():
                is_end = False
                start = start+1
                detail_url = detail_item.attr('href')
                print(detail_url)
                err_count = 1
                while err_count <= 5:
                    try:
                        book_info = self.detail_handler(detail_url)
                        #7 代表成功
                        err_count = 7
                    except:
                        time.sleep(1)
                        err_count = err_count + 1
                else:
                    #6 代表重试后失败
                    if err_count == 6:
                        continue
                book_info['create_time'] = int(now_time)
                book_info['update_time'] = int(now_time)
                book_where_sql = "where subject_id='{subject_id}'".format(subject_id=book_info['subject_id'])
                if not self.__mysql_tool.set_table('db_book').sql(book_where_sql).exit():
                    book_id = self.__mysql_tool.insert('db_book', book_info)
                    if book_id == False: raise Exception('书籍添加错误')
                else:
                    db_book_info = self.__mysql_tool.sql(book_where_sql).find()
                    book_id = db_book_info['id']
                tag_where_sql = "where tag_id={tag_id} and book_id={book_id}".format(tag_id=tag_id, book_id=book_id)
                if not self.__mysql_tool.sql(tag_where_sql).exit():
                    tag_relation = {
                        'book_id': book_id,
                        'tag_id': tag_id,
                        'create_time': now_time,
                        'update_time': now_time,
                    }
                    self.__mysql_tool.insert('db_book_tag_relation', tag_relation)
                time.sleep(random.randint(1, 5))

    def detail_handler(self, url):
        """
        详情处理
        :param str url:
        :return:
        """
        book_info = dict()
        url_response = self.get_url_response(url)
        soup = BeautifulSoup(url_response.text, 'lxml')
        div_doc = soup.select('#info span')
        for i, soup_item in enumerate(div_doc):
            if soup_item.string in self.__detail_info.keys():
                book_info[self.__detail_info[soup_item.string]] = self.detail_info_handler(soup_item)
        book_info['url'] = url.strip('/')
        book_info['title'] = soup.select('#wrapper > h1 > span')[0].string
        book_info['subject_id'] = book_info['url'][book_info['url'].rfind('/')+1:]
        book_info['book_img'] = soup.select('#mainpic > a > img')[0].attrs['src']
        book_info['grade'] = soup.select('div.rating_self > strong.rating_num')[0].string.strip(' ')
        book_info['graded_number'] = soup.select('div.rating_sum > span > a > span')[0].string
        book_info['five_graded_percent'] = soup.select('div.rating_wrap > span.stars5')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        book_info['four_graded_percent'] = soup.select('div.rating_wrap > span.stars4')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        book_info['three_graded_percent'] = soup.select('div.rating_wrap > span.stars3')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        book_info['two_graded_percent'] = soup.select('div.rating_wrap > span.stars2')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        book_info['one_graded_percent'] = soup.select('div.rating_wrap > span.stars1')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        if len(soup.select('div.mod-hd > h2 > span.pl > a')) > 0:
            book_info['short_comment_count'] = soup.select('div.mod-hd > h2 > span.pl > a')[0].string.replace('全部', '').replace('条', '').strip(' ')
        else:
            book_info['short_comment_count'] = 0
        if len(soup.select('section.reviews > p.pl > a')) > 0:
            book_info['book_review_count'] = soup.select('section.reviews > p.pl > a')[0].string.replace('更多书评', '').replace('篇', '').replace('\n', '').replace(' ', '')
        else:
            book_info['book_review_count'] = 0
        if len(soup.select('div.ugc-mod > div.hd > h2 > span.pl > a > span')) > 0:
            book_info['note_count'] = soup.select('div.ugc-mod > div.hd > h2 > span.pl > a > span')[0].string
        else:
            book_info['note_count'] = 0
        return book_info

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
        return BookSpider.static_detail_info_normal_handler(soup_item).replace('页', '').strip(' ')

    @staticmethod
    def static_detail_info_price_handler(soup_item):
        """
        书籍价格信息
        :param soup_item:
        :return str:
        """
        return soup_item.next_sibling.\
            replace('元', '').replace('CNY', '').replace('HK$', '').replace('NTD', '').\
            replace('（全两册）', '').replace('（全三册）', '').strip(' ')

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
book_spider.book_spider()
# print(book_spider.detail_handler('https://book.douban.com/subject/26963900/'))


