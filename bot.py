# coding = utf-8
import config
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint


class DailyReport:
    __positions = {  # 现人员位置
        '在校': 'radio_xrywz5',
        '在苏州': 'radio_xrywz7',
        '江苏省内其他地区': 'radio_xrywz9',
        '在其他地区': 'radio_xrywz25'
    }

    def __init__(self):
        self.username = config.User.strip()
        self.passwd = config.Passwd.strip()
        self.__position = DailyReport.__positions[config.Position.strip()]
        self.province = config.Province
        self.city = config.City
        self.detail = config.DetailAddress
        self.__browser = webdriver.Chrome()
        self.__browser.get("http://dk.suda.edu.cn/default/work/suda/jkxxtb/jkxxcj.jsp")

    def __find_by(self, key: str):
        """ 元素选择器 """
        return {
            'id': lambda locator: self.__browser.find_element_by_id(locator),
            'name': lambda locator: self.__browser.find_element_by_name(locator),
            'class': lambda locator: self.__browser.find_element_by_class_name(locator)
        }[key]

    @staticmethod
    def __send_text(elem, key: str):
        """ 填写文本框 """
        elem.clear()
        elem.send_keys(key.strip())

    def __click_class(self, classname: str):
        """ 点击，class属性索引 """
        self.__find_by('class')(classname).click()

    def __click_id(self, id_: str):
        """ 点击，id属性索引 """
        self.__find_by('id')(id_).click()

    def __fuzzy_click(self, val: str):
        """ 模糊点击，xpath模糊查找id """
        self.__browser.find_element_by_xpath('//*[contains(@id,\'{}\')]'.format(val)).click()  # tmd, debug一小时，结果忘记点击了

    @staticmethod
    def __random_float() -> str:
        """ 随机产生35.8~36.6的体温数值 """
        num = 35.8 + 0.1 * randint(0, 8)
        return '%.1f' % num

    def __uncheck(self):
        """ 将所有勾选的复选框取消勾选 """
        try:
            while True:
                self.__click_class('icheckbox_square-green checked')
        except NoSuchElementException:
            pass

    def login(self):
        """ 统一身份认证登录 """
        DailyReport.__send_text(self.__find_by('name')('username'), self.username)  # 输入学号
        DailyReport.__send_text(self.__find_by('name')('password'), self.passwd)  # 输入密码
        sleep(1)
        self.__click_class('login-btn')  # 点击登录

    def need_login(self) -> bool:
        """ 测试是否需要登录，调用report方法前必须判断 """
        try:
            self.__find_by('name')('swtw')
        except NoSuchElementException:
            return True
        else:
            return False

    def report(self):
        """ 上报并提交体温信息（覆盖已有记录） """
        DailyReport.__send_text(self.__find_by('id')('input_swtw'), DailyReport.__random_float())  # 上午体温
        DailyReport.__send_text(self.__find_by('id')('input_xwtw'), DailyReport.__random_float())  # 下午体温
        self.__uncheck()  # 取消勾选
        self.__click_id('checkbox_jkzk35')  # 健康状况：正常
        self.__click_id(self.__position)  # 人员位置
        # 勾选省份
        self.__click_id('select2-select_jtdzshen-container')
        self.__fuzzy_click(self.province)
        # 勾选地级市
        self.__click_id('select2-select_jtdzshi-container')
        self.__fuzzy_click(self.city)
        # 输入具体地址
        DailyReport.__send_text(self.__find_by('id')('input_jtdz'), self.detail)
        self.__click_id('radio_sfyxglz29')  # 是否医学观察中：否
        self.__click_id('radio_yjcyxgl31')  # 已经结束观察：是
        sleep(1)
        self.__click_id('tpost')  # 点击提交
        self.__click_class('layui-layer-btn0')  # 点击确认
        try:
            self.__click_class('layui-layer-btn0')  # 覆盖确认
        except NoSuchElementException:
            pass
        print('打卡完成，请查看打卡记录')

    需要登录 = need_login
    登录 = login
    打卡 = report
