from .Common import Common


class Proxy(Common):
    """
    代理功能url请求类
    """
    def is_proxy_alive(self, proxy, protocol_type='https'):
        """
        检测代理是否可用
        :param str proxy: 代理链接
        :param str protocol_type: 代理协议类型
        :return:
        """
        protocol_type = protocol_type.lower()
        request_param = dict()
        request_param['headers'] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        request_param['proxies'] = {
            protocol_type: protocol_type + '://' + proxy,
        }
        request_param['allow_redirects'] = False
        request_param['timeout'] = 2
        url = 'https://www.baidu.com'
        response = self.set_request_param(request_param).get_url_response(url)
        if response:
            return True
        return False

    def repeat_proxy_test(self, proxy, protocol_type='https'):
        """
        重复测试代理是否可用
        :param proxy:
        :param protocol_type:
        :return:
        """
        for i in range(5):
            result = self.is_proxy_alive(proxy, protocol_type.lower())
            if result:
                return True
        return False

# common = Common()
# print(common.is_proxy_alive('114.115.140.25:3128'))

