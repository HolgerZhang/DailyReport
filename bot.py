# coding = utf-8
# author: holger version: 1.3
# license: AGPL-3.0

import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint

import version

_mapping = {}
_user = {}


def load():
    """ 加载数据 """
    global _mapping, _user
    with open('mapping.json', 'r', encoding='utf-8') as __mapping_file:
        _mapping = json.load(__mapping_file)
        assert version.check_version(version.MAPPING_MIN_VERSION_REQUIRED, _mapping['_version']) <= 0
    with open('user.json', 'r', encoding='utf-8') as __user_file:
        __user = json.load(__user_file)
        assert version.check_version(version.USER_MIN_VERSION_REQUIRED, __user['_version']) <= 0
        _user = __user['information']


class DailyReport:

    def __init__(self):
        self.__now_positions = _mapping['now_positions_mapping']
        self.__attribute = _mapping['attribute']
        self.user_id = _user['user_id'].strip()
        self.passwd = _user['password'].strip()
        self.now_position = _user['now_position'].strip()
        self.province = _user['province'].strip()
        self.city = _user['city'].strip()
        self.qu = _user['qu'].strip()
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
        info = self.__attribute['click']['uncheck']
        try:
            while True:
                self.__click(**info)
        except NoSuchElementException:
            pass

    def login(self):
        """ 统一身份认证登录 """
        info = self.__attribute['login']
        self.__fill(**info['user_id'], desc=self.user_id)  # 输入学号
        self.__fill(**info['password'], desc=self.passwd)  # 输入密码
        sleep(1)
        btn = self.__attribute['button']['login']
        self.__click(**btn)  # 点击登录
        print('Login, {}!'.format(self.user_id))

    def need_login(self) -> bool:
        """ 测试是否需要登录，调用report方法前必须判断 """
        btn = self.__attribute['button']['report_post']
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
        click = self.__attribute['click']
        self.__click(**click['health_status_normal'])  # 个人健康状况：正常
        self.__click(**click['now_positions'])  # 现人员位置选择
        self.__click('fuzzy', self.__now_positions[self.now_position])
        # 具体地址
        self.__click(**click['province'])  # 选择省份
        self.__click('fuzzy', self.province)
        self.__click(**click['city'])  # 选择地级市
        self.__click('fuzzy', self.city)
        self.__click(**click['qu'])  # 选择区
        self.__click('fuzzy', self.qu)
        self.__click(**click['medical_observation_no'])  # 医学观察中：否
        self.__click(**click['actions_trajectory_no'])  # 当日行动轨迹是否有外出：否
        self.__click(**click['infected_exposed_no'])  # 是否与新冠确诊病例/无症状感染者接触过：否
        self.__click(**click['infected_crossed_no'])  # 是否与新冠确诊病例/无症状感染者有行程轨迹交叉：否
        self.__click(**click['history_risk_areas_no'])  # 是否有中高风险地区旅居史（包括途径中高风险地区）：否
        self.__click(**click['risk_areas_person_exposed_no'])  # 是否与中高风险地区人员接触：否
        # self.__click(**click['observation_finished_yes'])  # 已经结束观察：是
        sleep(1)
        # 填写文字信息
        input_ = self.__attribute['input']
        self.__fill(**input_['temperature_morning'], desc=self.__random_float())  # 上午体温
        self.__fill(**input_['temperature_afternoon'], desc=self.__random_float())  # 下午体温
        self.__fill(**input_['detail_address'], desc=self.detail)  # 输入具体地址
        sleep(1)
        # 提交
        buttons = self.__attribute['button']
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
