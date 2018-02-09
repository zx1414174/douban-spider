from App.Tool.MysqlTool import MysqlTool
from App.Url.Common import Common


class ProxySpider:
    """
    免费代理数据爬取
    """
    def __init__(self):
        self.__mysql_tool = MysqlTool()
        self.__common = Common()
        self.__common.set_header({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        })

    def xici_spider(self):
        """
        爬取西刺代理
        :return:
        """
        url = 'http://www.xicidaili.com/wn/{page}'
        for i in range(10):
            now_url = url.format(page=i+1)
            doc = self.__common.get_pyquery_doc(now_url)
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
                print(insert_proxy_data)
                break


proxy_spider = ProxySpider()
proxy_spider.xici_spider()
