from pyquery import PyQuery
import requests
import time


class Common:
    """
    url处理公共类
    """
    def get_pyquery_doc(self, url, headers=''):
        """
        获取pyquery处理doc
        :param str url:
        :param dict headers:
        :return:
        """
        doc = False
        url_response = self.get_url_response(url, headers)
        if not url_response:
            doc = PyQuery(url_response.text)
        return doc

    def get_url_response(self, url, headers=''):
        """
        获取链接请求文本
        :param str url:
        :param dict headers:
        :return:
        """
        url_response = False
        err_count = 1
        # 5次循环重试
        while err_count <= 5:
            try:
                if headers == '':
                    headers = self.static_get_headers()
                url_response = requests.get(url, timeout=3, headers=headers)
                # 7 代表成功
                err_count = 7
            except:
                time.sleep(1)
                err_count = err_count + 1
        return url_response

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

    @staticmethod
    def static_is_proxy_alive(proxy):
        """
        检测代理是否可用
        :param proxy:
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        test_url = 'www.baidu.com'
        try:
            response = requests.get(test_url, allow_redirects=False, headers=headers, timeout=2)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False

