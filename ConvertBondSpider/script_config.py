

class ScriptConfig():
    '''爬虫cookies信息配置'''
    def __init__(self):
        self.session = None
        self.user_login = None

    def set_session(self,session):
        self.session = session

    def set_user_login(self,user_login):
        self.user_login = user_login
  
    def get_cookies(self):
        cookies = {
            'kbzw__Session': self.session,
            'Hm_lvt_164fe01b1433a19b507595a43bf58262': '1658332080',
            'kbz_newcookie': '1',
            'kbzw__user_login': self.user_login,
            'Hm_lpvt_164fe01b1433a19b507595a43bf58262': '1659969041',
        }
        return cookies

    def get_headers(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'init': '1',
        }
        return headers

    def get_data(self):
        data = {
            'rp': '50',
            'page': '1',
        }
        return data
