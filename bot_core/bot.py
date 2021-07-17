# coding = utf-8
# author: holger version: 2.0
# license: AGPL-3.0
# belong: DailyReport-BotCore

import json
import sys
import traceback
from random import randint
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, SessionNotCreatedException

from bot_core import exec_log, version, resources
from bot_core.file import CHROMEDRIVER_FILE, msg_box, MAPPING_FILE, USER_FILE

BOT_DEBUG = '--DEBUG' in sys.argv


class WebBot:
    """
    （核心类）管理 配置数据 与 浏览器驱动程序
    """

    def __init__(self):
        """
        构造函数
        """
        self.__mapping = {}
        self.__user = []
        self.__browser = None

    def __del__(self):
        """
        析构函数
        """
        self.finish()

    def load(self) -> None:
        """
        加载数据
        :return: None
        """
        with open(MAPPING_FILE, 'r', encoding='utf-8') as __mapping_file:
            self.__mapping = json.load(__mapping_file)
            assert version.check_version(version.MAPPING_MIN_VERSION_REQUIRED, self.__mapping['_version']) <= 0
        with open(USER_FILE, 'r', encoding='utf-8') as __user_file:
            __user = json.load(__user_file)
            assert version.check_version(version.USER_MIN_VERSION_REQUIRED, __user['_version']) <= 0
            self.__user = __user['information']
        exec_log.logger(resources.LOAD_MAPPING_USER_JSON)

    def start(self) -> None:
        """
        启动浏览器
        :return: None
        """
        self.finish()
        try:
            self.__browser = webdriver.Chrome(CHROMEDRIVER_FILE)
        except SessionNotCreatedException as e:
            msg_box("请安装最新版Chrome，或将Chrome更新到最新版本。<br />" + e.msg)
            exit(1)

    def get_url(self) -> None:
        """
        访问目标URL
        :return: None
        """
        self.__browser.get(self.mapping['url'])

    def finish(self) -> None:
        """
        关闭浏览器
        :return: None
        """
        if self.__browser is not None:
            self.__browser.close()
            self.__browser = None

    def find(self, key: str):
        """
        元素选择器
        :param key: 选择类型 id, name, class, fuzzy 中的一种
        :return: Function
        """
        if self.__browser is None:
            msg_box(resources.ERR_NOT_START_BOT)
            raise RuntimeError(resources.ERR_NOT_START_BOT)
        return {
            'id': lambda locator: self.__browser.find_elements_by_id(locator),
            'name': lambda locator: self.__browser.find_elements_by_name(locator),
            'class': lambda locator: self.__browser.find_elements_by_class_name(locator),
            'fuzzy': lambda locator: self.__browser.find_elements_by_xpath('//*[contains(@id,\'{}\')]'.format(locator))
        }[key]

    def click(self, find_by: str, value: str, check: str = None, index=0) -> None:
        """
        点击，find_by 属性索引 value
        :param find_by: 选择类型 id, name, class, fuzzy 中的一种
        :param value: 要定位的值
        :param check: 预期 text
        :return: None
        """
        elem = self.find(find_by)(value)
        if len(elem) == 0:
            return
        if BOT_DEBUG:
            for i, e in enumerate(elem):
                print(i, e.get_attribute("innerHTML"))
            print('==' * 10)
        elem = elem[index]
        if check is not None:
            exec_log.logger(resources.CHECK_F2.format(check, elem.text))
            if check != elem.text:
                msg_box(resources.ERR_WEBSITE_UPDATE)
                raise RuntimeError(resources.ERR_WEBSITE_UPDATE)
        if BOT_DEBUG:
            exec_log.logger(elem.get_attribute("innerHTML"))
        elem.click()
        exec_log.logger(resources.CLICK_F2.format(find_by, value))

    def fill(self, find_by: str, value: str, desc: str, check: str = None) -> None:
        """
        填写文本框，find_by属性索引value，填入info
        点击，find_by 属性索引 value
        :param find_by: 选择类型 id, name, class, fuzzy 中的一种
        :param value: 要定位的值
        :param desc: 要填写的内容
        :param check: 预期 text
        :return: None
        """
        elem = self.find(find_by)(value)
        if len(elem) == 0:
            return
        if BOT_DEBUG:
            for i, e in enumerate(elem):
                print(i, e.get_attribute("innerHTML"))
            print('==' * 10)
        elem = elem[0]
        if check is not None:
            exec_log.logger(resources.CHECK_F2.format(check, elem.text))
            if check != elem.text:
                msg_box(resources.ERR_WEBSITE_UPDATE)
                raise RuntimeError(resources.ERR_WEBSITE_UPDATE)
        elem.clear()
        elem.send_keys(desc.strip())
        exec_log.logger(resources.FILL_F3.format(find_by, value, desc))

    @property
    def mapping(self) -> dict:
        """
        :return: mapping 配置数据
        """
        if len(self.__mapping) == 0:
            msg_box(resources.ERR_NOT_LOAD_MAPPING)
            raise ValueError(resources.ERR_NOT_LOAD_MAPPING)
        return self.__mapping

    def user(self, index: int) -> dict:
        """
        加载第 index 个 user 配置
        :param index: user 编号
        :return: user 配置数据
        """
        if len(self.__user) == 0:
            msg_box(resources.ERR_NOT_LOAD_USER)
            raise ValueError(resources.ERR_NOT_LOAD_USER)
        if not 0 <= index <= len(self.__user) - 1:
            msg_box(resources.ERR_USER_INDEX_OVER)
            raise IndexError(resources.ERR_USER_INDEX_OVER)
        return self.__user[index]

    @property
    def user_number(self) -> int:
        """
        :return: user 配置数据个数
        """
        return len(self.__user)

    @property
    def check_map(self) -> dict:
        """
        :return: mapping 配置中 check 部分
        """
        if len(self.__mapping) == 0:
            msg_box(resources.ERR_NOT_LOAD_MAPPING)
            raise ValueError(resources.ERR_NOT_LOAD_MAPPING)
        return self.__mapping['check']

    def reboot(self) -> None:
        """
        重启浏览器实例
        :return: None
        """
        self.finish()
        self.start()


def random_float() -> str:
    """
    随机产生35.8~36.6的体温数值
    :return: 保留一位小数的字符串
    """
    num = 35.8 + 0.1 * randint(0, 8)
    return '%.1f' % num


class Execution:
    """
    执行 mapping 中的自定义方法
    配置数据格式：
    {
        "name": "FunctionName",
        "return": true | false,
        "except": true | false,
        "operating": [
            {
                "action": "可选值：click; fill; fuzzy_click",
                "attribute": [
                    "ClassName",
                    "ObjectName"
                ],
                "user_need": "（action=click时不必要）user.json中'information'相应的键"
            }
        ]
    }
    """

    def __init__(self, circuit_map: dict):
        """
        构造函数
        :param circuit_map: 配置数据
        """
        self.__name: str = circuit_map['name']
        self.__need_return: bool = circuit_map['return']
        self.__catch_exception: bool = circuit_map['except']
        self.__operators: list = circuit_map['operating']
        exec_log.logger(resources.CIRCUIT_FUNC_SETUP_F3.format(self.__name, self.__need_return, self.__catch_exception))

    def run(self, web_bot: WebBot, user_index: int) -> bool:
        """
        运行方法
        :param web_bot: 运行方法的bot
        :param user_index: user 下标
        :return: 是否成功
        """

        def get_mapping_desc(attrs: list) -> dict:
            """
            获取 attribute 所指的 mapping 中数据
            :param attrs: attribute 列表
            :return: attribute 所指的 mapping 中数据
            """
            result = web_bot.mapping['attribute']
            if len(attrs) == 0:
                result = {}
            for attr in attrs:
                result = result[attr]
            return result

        def runnable(opera: dict) -> None:
            """
            执行器
            :param opera: 执行数据
            :return: None
            """
            attribute = opera['attribute']
            user_need = opera.get('user_need', '')
            change_flag = False
            if user_need.startswith('$'):
                user_need = eval(user_need.lstrip('$'))
                change_flag = True
            if opera['action'] == 'fill':
                web_bot.fill(**get_mapping_desc(attribute),
                             desc=user_need if change_flag else web_bot.user(user_index)[user_need].strip(),
                             check=web_bot.check_map.get(attribute[-1] if len(attribute) != 0 else '', None))
            elif opera['action'] == 'click':
                web_bot.click(**get_mapping_desc(attribute),
                              check=web_bot.check_map.get(attribute[-1] if len(attribute) != 0 else '', None))
            elif opera['action'] == 'fuzzy_click':
                value = web_bot.user(user_index)[user_need].strip()
                if len(attribute) != 0:
                    value = get_mapping_desc(attribute)[value]
                web_bot.click('fuzzy', value, index=-1)

        exec_log.logger(resources.CIRCUIT_FUNC_RUNNING_F2.format(self.__name, user_index))
        for operator in self.__operators:
            if self.__catch_exception:
                try:
                    runnable(operator)
                except NoSuchElementException as ex:
                    exec_log.logger(resources.CATCH_EXCEPT_F2.format(ex, traceback.format_exc()))
                    if self.__need_return:
                        return False
            else:
                runnable(operator)
            sleep(0.1)
        exec_log.logger(resources.CIRCUIT_FUNC_FINISHED_F2.format(self.__name, user_index))
        return True


def run_bot(web_bot: WebBot) -> None:
    """
    WebBot 执行器
    :param web_bot: WebBot 对象
    :return: None
    """
    circuit = web_bot.mapping['circuit']
    for index in range(web_bot.user_number):
        web_bot.get_url()
        for circuit_map in circuit:
            execution = Execution(circuit_map)
            try:
                complete = execution.run(web_bot, index)
            except Exception as exception:
                msg_box(resources.CATCH_UNKNOWN_EXCEPT_F2.format(exception, index))
                exec_log.logger(resources.EXCEPT_TRACEBACK + traceback.format_exc())
                if BOT_DEBUG:
                    input()
                return
            if not complete:
                msg_box(resources.CATCH_EXCEPT_SEE_LOG_F1.format(index))
                if BOT_DEBUG:
                    input()
                return
        msg_box("本次打卡成功，10秒后将进行下一任务")
        sleep(10)
        web_bot.reboot()
