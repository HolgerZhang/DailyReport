# coding = utf-8
# author: holger version: 1.2
# license: AGPL-3.0

import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint

from version import VERSION, MAPPING_MIN_VERSION_REQUIRED, USER_MIN_VERSION_REQUIRED

# Load
with open('mapping.json', 'r', encoding='utf-8') as __mapping_file:
    _mapping = json.load(__mapping_file)
    assert MAPPING_MIN_VERSION_REQUIRED <= _mapping['_version'] <= VERSION
with open('user.json', 'r', encoding='utf-8') as __user_file:
    __user = json.load(__user_file)
    assert USER_MIN_VERSION_REQUIRED <= __user['_version'] <= VERSION
    _user = __user['information']


class DailyReport:
    __now_positions = _mapping['now_positions_mapping']
    __attribute = _mapping['attribute']

    def __init__(self):
        self.user_id = _user['user_id'].strip()
        self.passwd = _user['password'].strip()
        self.__now_position = DailyReport.__now_positions[_user['now_position'].strip()]
        self.province = _user['province'].strip()
        self.city = _user['city'].strip()
        self.detail = _user['detail_address'].strip()
        self.__browser = webdriver.Chrome()
        self.__browser.get(_mapping['url'])
        print('Welcome!')

    def __find_by(self, key: str):
        """ 元素选择器 """
        return {
            'id': lambda locator: self.__browser.find_element_by_id(locator),
            'name': lambda locator: self.__browser.find_element_by_name(locator),
            'class': lambda locator: self.__browser.find_element_by_class_name(locator),
            'fuzzy': lambda locator: self.__browser.find_element_by_xpath('//*[contains(@id,\'{}\')]'.format(locator))
        }[key]

    def __click(self, find_by: str, value: str):
        """ 点击，find_by属性索引value """
        self.__find_by(find_by)(value).click()
        print('Click @{}={}.'.format(find_by, value))

    def __fill(self, find_by: str, value: str, desc: str):
        """ 填写文本框，find_by属性索引value，填入info """
        elem = self.__find_by(find_by)(value)
        elem.clear()
        elem.send_keys(desc.strip())
        print('Fill @{}={} with "{}".'.format(find_by, value, desc))

    @staticmethod
    def __random_float() -> str:
        """ 随机产生35.8~36.6的体温数值 """
        num = 35.8 + 0.1 * randint(0, 8)
        return '%.1f' % num

    def __uncheck(self):
        """ 将所有勾选的复选框取消勾选 """
        info = DailyReport.__attribute['click']['uncheck']
        try:
            while True:
                self.__click(**info)
        except NoSuchElementException:
            pass

    def login(self):
        """ 统一身份认证登录 """
        info = DailyReport.__attribute['login']
        self.__fill(**info['user_id'], desc=self.user_id)  # 输入学号
        self.__fill(**info['password'], desc=self.passwd)  # 输入密码
        sleep(1)
        btn = DailyReport.__attribute['button']['login']
        self.__click(**btn)  # 点击登录
        print('Login, {}!'.format(self.user_id))

    def need_login(self) -> bool:
        """ 测试是否需要登录，调用report方法前必须判断 """
        btn = DailyReport.__attribute['button']['report_post']
        try:
            self.__find_by(btn['find_by'])(btn['value'])
        except NoSuchElementException:
            return True
        else:
            return False

    def report(self):
        """ 上报并提交体温信息（覆盖已有记录） """
        self.__uncheck()  # 取消勾选
        # 勾选选项
        click = DailyReport.__attribute['click']
        self.__click(**click['health_status_normal'])  # 健康状况：正常
        self.__click(click['now_positions']['find_by'], self.__now_position)  # 人员位置
        self.__click(**click['province'])  # 选择省份
        self.__click('fuzzy', self.province)
        self.__click(**click['city'])  # 选择地级市
        self.__click('fuzzy', self.city)
        self.__click(**click['medical_observation_no'])  # 是否医学观察中：否
        # self.__click(**click['observation_finished_yes'])  # 已经结束观察：是
        sleep(1)
        # 填写文字信息
        input_ = DailyReport.__attribute['input']
        self.__fill(**input_['temperature_morning'], desc=DailyReport.__random_float())  # 上午体温
        self.__fill(**input_['temperature_afternoon'], desc=DailyReport.__random_float())  # 下午体温
        self.__fill(**input_['detail_address'], desc=self.detail)  # 输入具体地址
        sleep(1)
        # 提交
        buttons = DailyReport.__attribute['button']
        self.__click(**buttons['report_post'])  # 点击提交
        self.__click(**buttons['report_confirm'])  # 点击确认
        try:
            self.__click(**buttons['report_confirm'])  # 覆盖确认
        except NoSuchElementException:
            pass
        print('打卡完成，请查看打卡记录!')

    需要登录 = need_login
    登录 = login
    打卡 = report
