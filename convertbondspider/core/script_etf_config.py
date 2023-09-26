from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class ScriptETFConfig():
    '''爬虫cookies信息配置'''
    def __init__(self):
        self.xq_a_token = None

    def get_cookies(self):
        cookies = {
            # 'xq_a_token': '23d28dd06c5e86518de4b9c356b67467ae1e5405'
            # 'xq_a_token': 'e7e72ed2e6dfd5fc2d499073162b061a3fd82622'
            # 'xq_a_token': '29bdb37dee2432c294425cc9e8f45710a62643a5'
            'xq_a_token': self.xq_a_token

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

    def get_xq_a_token(self):
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        option.add_argument('--disable-gpu')
        # option.add_argument("window-size=1024,768")
        option.add_argument("--no-sandbox")
        # s = Service(executable_path='/Users/zhengshuocong/Documents/component/chromedriver')#selenium4中，把executable_path重构到了service中，如果系统变量中已有driver路径，则可以省略此行
        s = Service(executable_path='/opt/chromedriver/chromedriver-linux64/chromedriver')#selenium4中，把executable_path重构到了service中，如果系统变量中已有driver路径，则可以省略此行
        driver = webdriver.Chrome(service=s,options=option)
        driver.get("https://www.xueqiu.com/")
        cookies = driver.get_cookies()
        for item in cookies:
            if item['name'] == 'xq_a_token':
                self.xq_a_token = item['value']
        print("获取xq_a_token: "+self.xq_a_token)


if __name__ == '__main__':
    sc = ScriptETFConfig()
    sc.get_xq_a_token()
    sc.get_cookies()

