import time
from pyquery import PyQuery
from bs4 import BeautifulSoup
from App.Mysql.Proxy import Proxy as MysqlProxy
from App.Mysql.BookTag import BookTag
from App.Mysql.Error import Error
from App.Mysql.Book import Book
from App.Mysql.BookTagRelation import BookTagRelation
from App.Url.Proxy import Proxy
from CommonSpider import CommonSpider
from multiprocessing import Pool
import os


class BookSpider(CommonSpider):
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
        CommonSpider.__init__(self)
        self.__proxy_mysql = MysqlProxy()
        self.__book_tag_mysql = BookTag()
        self.__error_mysql = Error()
        self.__book_mysql = Book()
        self.__book_tag_relation_mysql = BookTagRelation()

    def _set_request_tool(self):
        self._request_tool = Proxy()

    def get_response_use_proxy(self, url):
        """
        获取请求信息
        :return:
        """
        is_can_use = False
        proxy_url = ''
        proxy_type = ''
        proxy_data = dict()
        for i in range(5):
            proxy_data = self.__proxy_mysql.get_rand_proxy()
            proxy_url = proxy_data['ip'] + ':' + proxy_data['port']
            proxy_type = proxy_data['protocol_type'].lower()
            is_can_use = self._request_tool.is_proxy_alive(proxy_url, proxy_type)
            if not is_can_use:
                self.__proxy_mysql.increase(proxy_data['id'], {
                    'fail_num': 1
                })
            else:
                self.__proxy_mysql.update({
                    'fail_num': 0
                })
                break
        if is_can_use:
            proxies = {
                proxy_type: proxy_type + '://' + proxy_url,
            }
            url_response = self._request_tool.set_proxies(proxies).get_url_response(url)
            if not url_response:
                return False
                # url_response = self._request_tool.del_proxies().get_url_response(url)
            else:
                print('成功！！')
        else:
            return False
            # url_response = self._request_tool.del_proxies().get_url_response(url)
        return url_response

    def tag_spider(self):
        """
        豆瓣热门标签爬取
        :return:
        """
        url = 'https://book.douban.com/tag/?view=type'
        doc = self._request_tool.get_pyquery_doc(url)
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
            pid = self.__book_tag_mysql.insert(parent_insert_data)
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
                self.__book_tag_mysql.insert(children_insert_data)

    def book_spider(self):
        """
        爬取豆瓣书籍(多线程)
        :return:
        """
        tag_list = self.__book_tag_mysql.get()
        for tag in tag_list:
            if tag['url'] != '':
                url = tag['url'].replace('tag//tag', 'tag')

    def one_tag_book_spider(self, tag_id):
        """
        爬取单个tag数据数据
        :param tag_id:
        :return:
        """
        tag = self.__book_tag_mysql.search_sql('where id={tag_id}'.format(tag_id=tag_id)).find()
        url = tag['url'].replace('tag//tag', 'tag')
        self.list_handler(url, tag_id)

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
            url_response = self.get_response_use_proxy(page_url)
            if not url_response:
                self.__error_mysql.insert({
                    'message': 'list,miss:'+page_url,
                    'create_time': int(now_time),
                    'update_time': int(now_time),
                })
                continue
            doc = PyQuery(url_response.text)
            detail_doc_list = doc('ul.subject-list > li > div.info > h2 a')
            is_end = True
            for detail_item in detail_doc_list.items():
                is_end = False
                start = start+1
                detail_url = detail_item.attr('href')
                print(detail_url)
                book_info = self.detail_handler(detail_url)
                if not book_info:
                    self.__error_mysql.insert({
                        'message': detail_url,
                        'create_time': int(now_time),
                        'update_time': int(now_time),
                    })
                    continue
                book_info['create_time'] = int(now_time)
                book_info['update_time'] = int(now_time)
                book_where_sql = "where subject_id='{subject_id}'".format(subject_id=book_info['subject_id'])
                if not self.__book_mysql.search_sql(book_where_sql).exit():
                    book_id = self.__book_mysql.insert(book_info)
                    if not book_id:
                        raise Exception('书籍添加错误')
                else:
                    db_book_info = self.__book_mysql.search_sql(book_where_sql).find()
                    book_id = db_book_info['id']
                tag_where_sql = "where tag_id={tag_id} and book_id={book_id}".format(tag_id=tag_id, book_id=book_id)
                if not self.__book_tag_relation_mysql.search_sql(tag_where_sql).exit():
                    tag_relation = {
                        'book_id': book_id,
                        'tag_id': tag_id,
                        'create_time': now_time,
                        'update_time': now_time,
                    }
                    self.__book_tag_relation_mysql.insert(tag_relation)

    def detail_handler(self, url):
        """
        详情处理
        :param str url:
        :return:
        """
        book_info = dict()
        url_response = self.get_response_use_proxy(url)
        if not url_response:
            return url_response
        soup = BeautifulSoup(url_response.text, 'lxml')
        div_doc = soup.select('#info span')
        for i, soup_item in enumerate(div_doc):
            if soup_item.string in self.__detail_info.keys():
                book_info[self.__detail_info[soup_item.string]] = self.detail_info_handler(soup_item)
        book_info['url'] = url.strip('/')
        book_info['subject_id'] = book_info['url'][book_info['url'].rfind('/')+1:]
        if len(soup.select('#wrapper > h1 > span')) > 0:
            book_info['title'] = soup.select('#wrapper > h1 > span')[0].string
        else:
            book_info['title'] = ''
        if len(soup.select('#mainpic > a > img')) > 0:
            book_info['book_img'] = soup.select('#mainpic > a > img')[0].attrs['src']
        else:
            book_info['book_img'] = ''
        if len(soup.select('div.rating_self > strong.rating_num')) > 0:
            book_info['grade'] = soup.select('div.rating_self > strong.rating_num')[0].string.strip(' ')
        else:
            book_info['grade'] = 0
        if len(soup.select('div.rating_sum > span > a > span')) > 0:
            book_info['graded_number'] = soup.select('div.rating_sum > span > a > span')[0].string
        else:
            book_info['graded_number'] = 0

        if len(soup.select('div.rating_wrap > span.stars5')) > 0:
            book_info['five_graded_percent'] = soup.select('div.rating_wrap > span.stars5')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        else:
            book_info['five_graded_percent'] = 0
        if len(soup.select('div.rating_wrap > span.stars4')) > 0:
            book_info['four_graded_percent'] = soup.select('div.rating_wrap > span.stars4')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        else:
            book_info['four_graded_percent'] = 0
        if len(soup.select('div.rating_wrap > span.stars3')) > 0:
            book_info['three_graded_percent'] = soup.select('div.rating_wrap > span.stars3')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        else:
            book_info['three_graded_percent'] = 0
        if len(soup.select('div.rating_wrap > span.stars2')) > 0:
            book_info['two_graded_percent'] = soup.select('div.rating_wrap > span.stars2')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        else:
            book_info['two_graded_percent'] = 0
        if len(soup.select('div.rating_wrap > span.stars1')) > 0:
            book_info['one_graded_percent'] = soup.select('div.rating_wrap > span.stars1')[0].next_sibling.next_sibling.next_sibling.next_sibling.string.strip(' ').replace('%', '')
        else:
            book_info['one_graded_percent'] = 0
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


def process_book(tag_id):
    print('process %s.' % os.getpid())
    book_spider = BookSpider()
    book_spider.one_tag_book_spider(tag_id)


# process_book(4)
if __name__ == '__main__':
    # 多进程爬取
    p = Pool(9)
    for i in range(2, 9):
        p.apply_async(process_book, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
# print(book_spider.detail_handler('https://book.douban.com/subject/26963900/'))


