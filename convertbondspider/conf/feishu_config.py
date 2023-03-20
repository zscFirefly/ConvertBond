
import sys
sys.path.append("..")


class FeishuConfig():
    '''飞书配置类'''
    def __init__(self):
        self.app_id = None
        self.app_secret = None
        self.user_id = None
        self.union_id = None
        self.open_id = None

    def set_app_id(self,app_id):
        self.app_id = app_id

    def set_app_secret(self,app_secret):
        self.app_secret = app_secret

    def set_user_id(self,user_id):
        self.user_id = user_id

    def set_union_id(self,union_id):
        self.union_id = union_id

    def set_open_id(self,open_id):
        self.open_id = open_id