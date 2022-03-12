# coding = utf-8
# author: holger
# version: 4.0.0
# license: AGPL-3.0
# belong: DailyReport-BotCore

import json
import os
import traceback
from random import randint
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from BotCore import version, logger
from BotCore.file import MAPPING_FILE
from mail import Mail

BOT_DEBUG = os.environ.get('BOT_CORE_DEBUG', 'FALSE').strip().upper() == 'TRUE'


class WebBot:
    """
    （核心类）管理 配置数据 与 浏览器驱动程序
    """

    def __init__(self, user_config_file, browser_type='Chrome', driver_path=None):
        with open(MAPPING_FILE, 'r', encoding='utf-8') as __mapping_file:
            self.__mapping = json.load(__mapping_file)
            assert version.check_version(version.MAPPING_MIN_VERSION, self.__mapping['VERSION']), '版本号不匹配'
        with open(user_config_file, 'r', encoding='utf-8') as __user_file:
            self.__user = json.load(__user_file)
            assert version.check_version(version.USER_MIN_VERSION, self.__user['VERSION']), '版本号不匹配'
        logger.info('加载文件: "{}", "{}"'.format(MAPPING_FILE, user_config_file))
        self._browser_type = browser_type.lower()
        if driver_path is not None and len(driver_path.strip()) != 0:
            self._driver_path = driver_path.strip()
        else:
            self._driver_path = None
        self.__browser = None

    def __del__(self):
        self.finish()

    def start(self) -> None:
        """
        启动浏览器
        :raises SessionNotCreatedException
        :return: None
        """
        self.finish()
        if self._browser_type == 'chrome':
            if self._driver_path is not None:
                self.__browser = webdriver.Chrome(self._driver_path)
            else:
                self.__browser = webdriver.Chrome()
        elif self._browser_type == 'firefox':
            if self._driver_path is not None:
                self.__browser = webdriver.Firefox(self._driver_path)
            else:
                self.__browser = webdriver.Firefox()
        elif self._browser_type == 'edge':
            if self._driver_path is not None:
                self.__browser = webdriver.Edge(self._driver_path)
            else:
                self.__browser = webdriver.Edge()
        elif self._browser_type == 'safari':
            self.__browser = webdriver.Safari()
        elif self._browser_type == 'ie':
            if self._driver_path is not None:
                self.__browser = webdriver.Ie(self._driver_path)
            else:
                self.__browser = webdriver.Ie()
        elif self._browser_type == 'opera':
            if self._driver_path is not None:
                self.__browser = webdriver.Opera(self._driver_path)
            else:
                self.__browser = webdriver.Opera()
        else:
            raise ValueError('不支持的浏览器')

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
            logger.error('Error: 实例化(start)浏览器前使用 WebBot')
            raise RuntimeError('Error: 实例化(start)浏览器前使用 WebBot')
        return {
            'id': lambda locator: self.__browser.find_elements_by_id(locator),
            'name': lambda locator: self.__browser.find_elements_by_name(locator),
            'class': lambda locator: self.__browser.find_elements_by_class_name(locator),
            'fuzzy': lambda locator: self.__browser.find_elements_by_xpath('//*[contains(@id,\'{}\')]'.format(locator)),
            'text': lambda locator: self.__browser.find_elements_by_xpath(
                '//li[contains(string(),\'{}\')]'.format(locator))
        }[key]

    def click(self, find_by: str, value: str, check: str = None, index=0) -> None:
        """
        点击，find_by 属性索引 value
        :param find_by: 选择类型 id, name, class, fuzzy 中的一种
        :param value: 要定位的值
        :param check: 预期 text
        :param index
        :return: None
        """
        elem = self.find(find_by)(value)
        if len(elem) == 0:
            logger.info("元素未找到")
            raise NoSuchElementException("元素未找到")
        if BOT_DEBUG:
            for i, e in enumerate(elem):
                print(i, e.get_attribute("innerHTML"))
            print('==' * 10)
        elem = elem[index]
        if check is not None:
            logger.info('检查 "{}"(预期)=="{}"(实际)'.format(check, elem.text))
            if check != elem.text:
                logger.error('Error: 网页发生更新，请联系mapping提供方更新数据')
                raise RuntimeError('Error: 网页发生更新，请联系mapping提供方更新数据')
        logger.debug(elem.get_attribute("innerHTML"))
        elem.click()
        logger.info('点击 @{}={}.'.format(find_by, value))

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
            logger.info('检查 "{}"(预期)=="{}"(实际)'.format(check, elem.text))
            if check != elem.text:
                logger.error('Error: 网页发生更新，请联系mapping提供方更新数据')
                raise RuntimeError('Error: 网页发生更新，请联系mapping提供方更新数据')
        elem.clear()
        elem.send_keys(desc.strip())
        logger.info('填写 @{}={}，值为 "{}"'.format(find_by, value, desc))

    @property
    def mapping(self) -> dict:
        """
        :return: mapping 配置数据
        """
        return self.__mapping

    @property
    def user(self) -> dict:
        """
        :return: user 配置数据
        """
        return self.__user

    @property
    def check_map(self) -> dict:
        """
        :return: mapping 配置中 check 部分
        """
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
        logger.info('自定义方法 "{}" 建立成功，需要返回值: {}, 捕获异常: {}'.format(self.__name,
                                                                 self.__need_return, self.__catch_exception))

    def run(self, web_bot: WebBot):
        """
        运行方法
        :param web_bot: 运行方法的bot
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
                             desc=user_need if change_flag else web_bot.user[user_need].strip(),
                             check=web_bot.check_map.get(attribute[-1] if len(attribute) != 0 else '', None))
            elif opera['action'] == 'click':
                web_bot.click(**get_mapping_desc(attribute),
                              check=web_bot.check_map.get(attribute[-1] if len(attribute) != 0 else '', None))
            elif opera['action'] == 'fuzzy_click':
                value = web_bot.user[user_need].strip()
                if len(attribute) != 0:
                    value = get_mapping_desc(attribute)[value]
                web_bot.click('fuzzy', value, index=-1)
            elif opera['action'] == 'text':
                value = web_bot.user[user_need].strip()
                web_bot.click('text', value, index=-1)

        logger.info('自定义方法 "{}" 正在运行'.format(self.__name))
        for operator in self.__operators:
            if self.__catch_exception:
                try:
                    runnable(operator)
                except NoSuchElementException as ex:
                    logger.warning('捕获异常: {}\n{}'.format(ex, traceback.format_exc()))
                    if self.__need_return:
                        return False, ex
            else:
                runnable(operator)
            sleep(0.1)
        logger.info('自定义方法 "{}" 结束'.format(self.__name))
        return True, None


def run_bot(web_bot: WebBot, mail: Mail) -> None:
    """
    WebBot 执行器
    :param web_bot: WebBot 对象
    :param mail: Mail 对象
    :return: None
    """

    def inner_runner(circuit):
        web_bot.get_url()
        for circuit_map in circuit:
            execution = Execution(circuit_map)
            try:
                complete, ex = execution.run(web_bot)
            except Exception as exception:
                msg = '捕获未知异常: {}'.format(exception)
                logger.info(msg)
                logger.warning('异常堆栈信息：\n' + traceback.format_exc())
                mail.fail_mail(
                    to=[web_bot.user.get('email', web_bot.user['user_id'] + '@stu.suda.edu.cn')],
                    stu_id=web_bot.user['user_id'],
                    detail={'message': Mail.html(msg),
                            '\nStack': Mail.html(traceback.format_exc())})
                if BOT_DEBUG:
                    input()
                return 1
            if not complete:
                msg = '捕获异常 {}, 详见data文件夹下BotLog.log文件'.format(ex)
                logger.info(msg)
                mail.fail_mail(
                    to=[web_bot.user.get('email', web_bot.user['user_id'] + '@stu.suda.edu.cn')],
                    stu_id=web_bot.user['user_id'],
                    detail={'message': Mail.html(msg)})
                if BOT_DEBUG:
                    input()
                return 1
        return 0

    circuit = web_bot.mapping['circuit']
    retry = 0
    while True:
        if inner_runner(circuit) == 0:
            break
        else:
            retry += 1
            if retry >= 5:
                break
            sleep(5)
            web_bot.reboot()
    if retry >= 5:
        msg = {'ERROR': '5次尝试均打卡失败！'}
        msg.update(web_bot.user)
        mail.fail_mail(to=[web_bot.user.get('email', web_bot.user['user_id'] + '@stu.suda.edu.cn')],
                       stu_id=web_bot.user['user_id'],
                       detail=msg)
        logger.error('5次尝试均打卡失败！')
    else:
        mail.success_mail(
            to=[web_bot.user.get('email', web_bot.user['user_id'] + '@stu.suda.edu.cn')],
            stu_id=web_bot.user['user_id'],
            detail=web_bot.user)
        logger.info("本次打卡成功，10秒后将进行下一任务")
    sleep(10)
    web_bot.reboot()
