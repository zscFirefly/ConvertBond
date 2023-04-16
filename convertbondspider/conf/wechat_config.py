
import sys
sys.path.append("..")


class WeChatConfig():
    '''企业微信配置类'''
    def __init__(self):
        self.corpid = None
        self.corpsecret = None

    def set_corpid(self,corpid):
        self.corpid = corpid

    def get_corpid(self):
        return self.corpid

    def set_corpsecret(self,corpsecret):
        self.corpsecret = corpsecret
