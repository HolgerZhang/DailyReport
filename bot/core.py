# coding = utf-8
"""
file: bot/core.py
author: holger
version: 3.0
license: AGPL-3.0
belongs: WebBot-BotCore
"""
import os
import traceback
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from bot import error
from bot import exec_log
from bot import resources
from bot import util
from bot import xml_parser
from bot.resources import R


class WebBot:
    """
    （核心类）管理 配置数据 与 浏览器驱动程序
    """

    def __init__(self):
        """
        构造函数
        """
        self.__mapping = util.Mapping()
        self.__user = []
        self.__browser = None
        self.__mapping_name = self.__mapping.name

    def __del__(self):
        """
        析构函数
        """
        self.finish()

    def load(self, map_name=None):
        """
        加载数据
        :return: None
        """
        maps = xml_parser.get_mapping_list(resources.MAP_FILE)
        if map_name is not None:
            for item in maps:
                if item.name == map_name:
                    self.__mapping = item
                    self.__mapping_name = self.__mapping.name
                    break
        else:
            if len(maps) > 0:
                self.__mapping = maps[0]
        self.__mapping_name = self.__mapping.name
        self.__user = xml_parser.get_user_cfg_list(resources.CONFIGURATION_FILE)
        if len(self.__user) == 0:
            raise error.IncompleteConfigError(R.string.ERR_INCOMPLETE_USER_CFG)
        exec_log.logger(R.string.LOAD_MAPPING_USER)

    def start(self):
        """
        启动浏览器
        :return: None
        """
        if self.__browser is not None:
            raise error.FatalError(R.string.ERR_NOT_CLOSE_BOT)
        if not os.path.isfile(resources.CHROMEDRIVER_FILE):
            resources.get_driver()
        self.__browser = webdriver.Chrome(resources.CHROMEDRIVER_FILE)

    def go(self):
        """
        访问目标URL
        :return: None
        """
        self.__browser.get(self.mapping.url)

    def reboot(self):
        """
        重启浏览器实例
        :return: None
        """
        self.finish()
        self.start()

    def finish(self):
        """
        关闭浏览器
        :return: None
        """
        if self.__browser is not None:
            self.__browser.close()
            self.__browser = None

    def _find(self, find_by: str, value: str):
        """
        元素选择器
        :param find_by: 选择类型 id, name, class 中的一种
        :param value: 要定位的值
        :return: Function
        """
        if self.__browser is None:
            raise error.FatalError(R.string.ERR_NOT_START_BOT)
        exec_log.logger(R.string.FIND_F2.format(find_by, value))
        if find_by == 'id':
            return self.__browser.find_element_by_id(value)
        elif find_by == 'name':
            return self.__browser.find_element_by_name(value)
        elif find_by == 'class':
            return self.__browser.find_element_by_class_name(value)
        else:
            raise error.UnexpectedValueError(R.string.ERR_UNSUPPORTED_TARGET, find_by)

    def _search_by_id(self, text: str):
        exec_log.logger(R.string.SEARCH_ID_CONTAINS_F1.format(text))
        return self.__browser.find_element_by_xpath(R.string.SEARCH_ID_XPATH_F1.format(text))

    def _find_xpath(self, xpath: str):
        exec_log.logger(R.string.FIND_XPATH_F1.format(xpath))
        return self.__browser.find_element_by_xpath(xpath)

    def _click(self, find_by: str, value: str, check: str = None):
        """
        点击，find_by 属性索引 value
        :param find_by: 选择类型 id, name, class 中的一种
        :param value: 要定位的值
        :param check: 预期 text
        :return: None
        """
        elem = self._find(find_by, value)
        if check is not None:
            exec_log.logger(R.string.CHECK_F2.format(check, elem.text))
            if check != elem.text:
                raise error.BotWarning(R.string.ERR_WEBSITE_UPDATE)
        WebBot._click_elem(elem)

    @staticmethod
    def _click_elem(elem):
        elem.click()
        exec_log.logger(R.string.CLICK_F1.format(elem))

    def _fill(self, find_by: str, value: str, desc: str, check: str = None):
        """
        填写文本框，find_by属性索引value，填入info
        点击，find_by 属性索引 value
        :param find_by: 选择类型 id, name, class 中的一种
        :param value: 要定位的值
        :param desc: 要填写的内容
        :param check: 预期 text
        :return: None
        """
        elem = self._find(find_by, value)
        if check is not None:
            exec_log.logger(R.string.CHECK_F2.format(check, elem.text))
            if check != elem.text:
                raise error.BotWarning(R.string.ERR_WEBSITE_UPDATE)
        WebBot._fill_elem(elem, desc)

    @staticmethod
    def _fill_elem(elem, desc: str):
        elem.clear()
        elem.send_keys(desc.strip())
        exec_log.logger(R.string.FILL_F2.format(elem, desc))

    def _save_text(self, find_by: str, value: str) -> str:
        return WebBot._save_elem_text(self._find(find_by, value))

    @staticmethod
    def _save_elem_text(elem) -> str:
        return elem.text

    @property
    def mapping(self) -> util.Mapping:
        """
        :return: mapping 配置数据
        """
        return self.__mapping

    @property
    def mapping_name(self) -> str:
        return self.__mapping_name

    def user(self, user_id=None) -> util.User:
        """
        获取编号为 user_id 的 user 配置
        :param user_id: user 编号，不填为 XML 第一个 User
        :return: user 配置数据
        """
        if len(self.__user) == 0:
            raise error.FatalError(R.string.ERR_NO_USER)
        if user_id is None:
            return self.__user[0]
        user_id = str(user_id)
        for user_obj in self.__user:
            if user_obj.id == user_id:
                return user_obj
        raise error.NameNotFoundError(R.string.ERR_USER_NOT_FOUND_F1.format(user_id), user_id)

    @property
    def user_ids(self) -> tuple:
        return tuple((user.id for user in self.__user))

    @property
    def all_user(self) -> list:
        return self.__user

    def run(self, user_id=None):
        if user_id is None:
            for user in self.__user:
                self._run_with_user(user)
                self.reboot()
        else:
            self._run_with_user(self.user(user_id))

    def _run_with_user(self, user: util.User):
        if self.__browser is None:
            raise error.FatalError(R.string.ERR_NOT_START_BOT)
        for action in self.mapping.actions:
            func = self.mapping.find_function(action)
            if func.return_type == str:
                exec_log.text_saver(R.string.RETURN_STR_SAVE_F2.format(func.name, self._exec(func, user, str_get=True)))
            else:
                self._exec(func, user)

    @staticmethod
    def _find_symbol(symbol: str, static_symbols: dict, dynamic_symbols: dict):
        obj = static_symbols.get(symbol, None)
        if obj is None:
            obj = dynamic_symbols.get(symbol, None)
        if obj is None:
            raise error.NameNotFoundError(R.string.ERR_SYMBOL_NOT_FOUND_F1.format(symbol), symbol)
        return obj

    def _exec(self, func: util.Function, user: util.User, str_get=False):
        str_return = ''
        dynamic_symbol = {}
        for idx in range(len(func.script)):
            try:
                if len(func.script[idx]) == 0:
                    continue
                if func.script[idx][0] == 'CLICK':
                    if len(func.script[idx]) != 2:
                        raise error.ScriptSyntaxError(R.string.ERR_STAT_ARGC_F1.format('CLICK'), idx + 1, func.name)
                    elem_name = func.script[idx][1]
                    if util.Function.is_valid_symbol(elem_name):
                        elem = WebBot._find_symbol(elem_name, func.static_symbol, dynamic_symbol)
                        if isinstance(elem, str):
                            raise error.SymbolTypeError(R.string.ERR_ARGV_NEED_ELEM, elem)
                        self._click_elem(elem)
                    else:
                        elem = self.mapping.find_element(elem_name)
                        self._click(elem.target, elem.value, check=elem.text if elem.check else None)
                elif func.script[idx][0] == 'FILL':
                    if len(func.script[idx]) != 3:
                        raise error.ScriptSyntaxError(R.string.ERR_STAT_ARGC_F1.format('FILL'), idx + 1, func.name)
                    elem_name = func.script[idx][1]
                    text = WebBot._find_symbol(func.script[idx][2], func.static_symbol, dynamic_symbol)
                    if not isinstance(text, str):
                        raise error.SymbolTypeError(R.string.ERR_ARGV_NEED_STR, text)
                    if util.Function.is_valid_symbol(elem_name):
                        elem = WebBot._find_symbol(elem_name, func.static_symbol, dynamic_symbol)
                        if isinstance(elem, str):
                            raise error.SymbolTypeError(R.string.ERR_ARGV_NEED_ELEM, elem)
                        self._fill_elem(elem, text)
                    else:
                        elem = self.mapping.find_element(elem_name)
                        self._fill(elem.target, elem.value, text, check=elem.text if elem.check else None)
                elif func.script[idx][0] == 'SAVE-TEXT':
                    if len(func.script[idx]) != 4:
                        raise error.ScriptSyntaxError(R.string.ERR_STAT_ARGC_F1.format('SAVE-TEXT'), idx + 1, func.name)
                    elem_name = func.script[idx][1]
                    if util.Function.is_valid_symbol(elem_name):
                        elem = WebBot._find_symbol(elem_name, func.static_symbol, dynamic_symbol)
                        if isinstance(elem, str):
                            raise error.SymbolTypeError(R.string.ERR_ARGV_NEED_ELEM, elem)
                    else:
                        elem = self.mapping.find_element(elem_name)
                    if func.script[idx][2] != 'AS':
                        raise error.ScriptSyntaxError(R.string.ERR_STAT_MISS_AS_F1.format('SAVE-TEXT'), idx + 1,
                                                      func.name)
                    symbol_name = func.script[idx][3]
                    if not util.Function.is_valid_symbol(symbol_name):
                        raise error.ScriptSyntaxError(R.string.ERR_SYMBOL_NAME_ERROR_F1.format(symbol_name), idx + 1,
                                                      func.name)
                    dynamic_symbol[symbol_name] = self._save_text(elem.target, elem.value)
                elif func.script[idx][0] == 'USE':
                    if len(func.script[idx]) != 4:
                        raise error.ScriptSyntaxError(R.string.ERR_STAT_ARGC_F1.format('USE'), idx + 1, func.name)
                    if func.script[idx][2] != 'AS':
                        raise error.ScriptSyntaxError(R.string.ERR_STAT_MISS_AS_F1.format('USE'), idx + 1, func.name)
                    symbol_name = func.script[idx][3]
                    if not util.Function.is_valid_symbol(symbol_name):
                        raise error.ScriptSyntaxError(R.string.ERR_SYMBOL_NAME_ERROR_F1.format(symbol_name), idx + 1,
                                                      func.name)
                    dynamic_symbol[symbol_name] = user.get(func.script[idx][1])
                elif str_get and func.script[idx][0] == 'STRING-RETURN':
                    if len(func.script[idx]) < 2:
                        raise error.ScriptSyntaxError(R.string.ERR_STAT_ARGC_F1.format('STRING-RETURN'), idx + 1,
                                                      func.name)
                    for symbol_name in func.script[idx][1:]:
                        if not util.Function.is_valid_symbol(symbol_name):
                            raise error.ScriptSyntaxError(R.string.ERR_SYMBOL_NAME_ERROR_F1.format(symbol_name),
                                                          idx + 1, func.name)
                        text = WebBot._find_symbol(symbol_name, func.static_symbol, dynamic_symbol)
                        if not isinstance(text, str):
                            raise error.SymbolTypeError(R.string.ERR_ARGV_NEED_STR, text)
                        str_return += text
                elif str_get and func.script[idx][0] == 'STRING-RETURN-CLEAR':
                    if len(func.script[idx]) != 1:
                        raise error.ScriptSyntaxError(R.string.ERR_STAT_ARGC_F1.format('STRING-RETURN-CLEAR'), idx + 1,
                                                      func.name)
                    str_return = ''
                elif func.script[idx][0] == 'SLEEP':
                    if len(func.script[idx]) != 2:
                        raise error.ScriptSyntaxError(R.string.ERR_STAT_ARGC_F1.format('SLEEP'), idx + 1, func.name)
                    if not func.script[idx][1].isdigit():
                        raise error.UnexpectedValueError(R.string.ERR_ARGV_NEED_INT, func.script[idx][1])
                    sleep(int(func.script[idx][1]))
                elif func.script[idx][0] == 'FIND-XPATH':
                    if len(func.script[idx]) != 4:
                        raise error.ScriptSyntaxError(R.string.ERR_STAT_ARGC_F1.format('FIND-XPATH'), idx + 1,
                                                      func.name)
                    if func.script[idx][2] != 'AS':
                        raise error.ScriptSyntaxError(R.string.ERR_STAT_MISS_AS_F1.format('FIND-XPATH'), idx + 1,
                                                      func.name)
                    save_symbol_name = func.script[idx][3]
                    if not util.Function.is_valid_symbol(save_symbol_name):
                        raise error.ScriptSyntaxError(R.string.ERR_SYMBOL_NAME_ERROR_F1.format(save_symbol_name),
                                                      idx + 1, func.name)
                    xpath = WebBot._find_symbol(func.script[idx][1], func.static_symbol, dynamic_symbol)
                    dynamic_symbol[save_symbol_name] = self._find_xpath(xpath)
                elif func.script[idx][0] == 'SEARCH':
                    if len(func.script[idx]) != 4:
                        raise error.ScriptSyntaxError(R.string.ERR_STAT_ARGC_F1.format('SEARCH'), idx + 1, func.name)
                    if func.script[idx][2] != 'AS':
                        raise error.ScriptSyntaxError(R.string.ERR_STAT_MISS_AS_F1.format('SEARCH'), idx + 1, func.name)
                    save_symbol_name = func.script[idx][3]
                    if not util.Function.is_valid_symbol(save_symbol_name):
                        raise error.ScriptSyntaxError(R.string.ERR_SYMBOL_NAME_ERROR_F1.format(save_symbol_name),
                                                      idx + 1, func.name)
                    text = WebBot._find_symbol(func.script[idx][1], func.static_symbol, dynamic_symbol)
                    if not isinstance(text, str):
                        raise error.SymbolTypeError(R.string.ERR_ARGV_NEED_STR, text)
                    dynamic_symbol[save_symbol_name] = self._search_by_id(text)
                else:
                    raise error.ScriptSyntaxError(R.string.ERR_STAT_ERROR_F1.format(func.script[idx][0]), idx + 1,
                                                  func.name)
            except error.BotWarning as warning:
                resources.msg_box(R.string.CATCH_WARNING_F3.format(warning.what, user.id, traceback.format_exc()))
            except NoSuchElementException as exception:
                if func.exception == 'escape':
                    pass
                elif func.exception == 'throw':
                    resources.msg_box(R.string.CATCH_EXCEPT_F3.format(exception, user.id, traceback.format_exc()))
                    return str_return if str_get else None
                elif func.exception == 'log':
                    exec_log.logger(R.string.CATCH_EXCEPT_F3.format(exception, user.id, traceback.format_exc()))
            except error.FatalError as exception:
                resources.msg_box(R.string.CATCH_EXCEPT_F3.format(exception.what, user.id, traceback.format_exc()))
                return str_return if str_get else None
            except Exception as exception:
                resources.msg_box(R.string.CATCH_INNER_ERROR_F3.format(exception, user.id, traceback.format_exc()))
                return str_return if str_get else None
        return str_return if str_get else None
