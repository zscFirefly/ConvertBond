
class ScriptETFConfig():
    '''爬虫cookies信息配置'''
    def __init__(self):
        pass

    def get_cookies(self):
        cookies = {
            # 'xq_a_token': '23d28dd06c5e86518de4b9c356b67467ae1e5405'
            # 'xq_a_token': 'e7e72ed2e6dfd5fc2d499073162b061a3fd82622'
            # 'xq_a_token': '29bdb37dee2432c294425cc9e8f45710a62643a5'
            'xq_a_token': '936cf930ee4bd46499c2611037893c558c5e65ba'

        }
        return cookies

    def get_headers(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
        return headers

    def get_data(self):
        data = {
            'type': '18',
            'parent_type': '1',
            'order': 'desc',
            'order_by': 'percent',
            'page': '1',
            'size': '1000',
        }
        return data
