from App.Mysql.MysqlTool import MysqlTool
from App.Url.Proxy import Proxy
from CommonSpider import CommonSpider
import time


class MoguSpider(CommonSpider):
    """
    免费代理数据爬取
    """
    def __init__(self):
        self.__mysql_tool = MysqlTool()
        self.now_time = time.time()
        CommonSpider.__init__(self)

    def _set_request_tool(self):
        self._request_tool = Proxy()
        self._request_tool.set_header({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        })

    def mogu_spider(self, url):
        """
        提取蘑菇代理数据
        :param url:
        :return dist :
        """
        url = url.strip('/') + '/{page}'
        for i in range(100):
            now_url = url.format(page=i+1)
            doc = self._request_tool.get_pyquery_doc(now_url)
            tr_doc_list = doc('#ip_list > tr')
            is_first = True
            for tr_doc in tr_doc_list.items():
                if is_first:
                    is_first = False
                    continue
                td_list = tr_doc.find("td")
                insert_proxy_data = dict()
                insert_proxy_data['ip'] = td_list.eq(1).text()
                insert_proxy_data['port'] = td_list.eq(2).text()
                insert_proxy_data['protocol_type'] = td_list.eq(5).text()
                where_sql = "where ip='{ip}' and port='{port}' and protocol_type='{protocol_type}'"\
                    .format(**insert_proxy_data)
                if self.__mysql_tool.search_sql(where_sql).exit():
                    continue
                is_live = self._request_tool.repeat_proxy_test(insert_proxy_data['port'],insert_proxy_data['protocol_type'])
                if not is_live:
                    continue
                insert_proxy_data['create_time'] = self.now_time
                insert_proxy_data['update_time'] = self.now_time
                self.__mysql_tool.set_table('db_proxy').insert(insert_proxy_data)
                print(insert_proxy_data)


proxy_spider = MoguSpider()
proxy_spider.mogu_spider('http://www.xicidaili.com/nn/')
