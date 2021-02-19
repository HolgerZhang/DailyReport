# coding = utf-8
"""
file: bot/util.py
author: holger
version: 3.0
license: AGPL-3.0
belongs: WebBot-BotCore
"""

import re
import traceback

from bot import error
from bot import resources
from bot import xml_parser


class SchedulerInfo:
    def __init__(self, hour='9', minute='30', second='0'):
        self.__hour = '9'
        self.__minute = '30'
        self.__second = '0'
        self.set_time(hour, minute, second)

    def __str__(self) -> str:
        return 'SchedulerInfo {}:{}:{}'.format(self.__hour, self.__minute, self.__second)

    def __eq__(self, other) -> bool:
        return self.hour == other.hour and self.minute == other.minute and self.second == other.second

    def set_time(self, hour: str, minute: str, second: str) -> None:
        self.__hour = hour
        self.__minute = minute
        self.__second = second

    @property
    def hour(self) -> str:
        return str(self.__hour)

    @property
    def minute(self) -> str:
        return str(self.__minute)

    @property
    def second(self) -> str:
        return str(self.__second)


class Element:
    def __init__(self, name='default', target='id', value='null', text='', check=False):
        self.__name = name
        self.__target = target
        self.__value = value
        self.__text = text
        self.__check = check

    @property
    def name(self) -> str:
        return self.__name

    @property
    def target(self) -> str:
        return self.__target

    @property
    def value(self) -> str:
        return self.__value

    @property
    def text(self) -> str:
        return self.__text

    @property
    def check(self) -> bool:
        return self.__check

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.target == other.target and self.value == other.value and \
               self.text == other.text and self.check == other.check

    def __str__(self) -> str:
        return 'Element <{}>, @{}={}, inner text: "{}"'.format(self.__name, self.__target, self.__value, self.__text)


class User:
    def __init__(self, user_id='100', data={}):
        self.__id = user_id
        self._data = data

    def __str__(self) -> str:
        return 'User id={}'.format(self.__id)

    def get(self, item):
        return_obj = self._data.get(item, None)
        if return_obj is None:
            raise error.UnexpectedValueError('Unexpected field {}'.format(self.__class__), item)
        return return_obj

    def __getattr__(self, item):
        if item == 'id':
            return self.__id
        elif item == 'data':
            return self._data
        else:
            return self.get(item)

    def __eq__(self, other) -> bool:
        return self.id == other.id and self.data == other.data


class void: pass


class Function:
    def __init__(self, name='default', return_type='void', exception='escape'):
        self.__name = name
        self.__return_type = {'str': str, 'bool': bool, 'void': void}.get(return_type, None)
        if self.__return_type is None:
            raise error.SymbolTypeError('Unsupported return type "{}"'.format(return_type),
                                        self.__return_type)
        if exception not in ('escape', 'log', 'throw'):
            raise error.UnexpectedValueError('Unsupported exception statement "{}"'.format(exception), exception)
        self.__exception = exception
        self.__script = []
        self.static_symbol = {}

    def __str__(self) -> str:
        return 'Function <{}>, return type: {}, exception: {}'.format(self.__name,
                                                                      self.__return_type.__class__,
                                                                      self.__exception)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def return_type(self):
        return self.__return_type

    @property
    def exception(self) -> str:
        return self.__exception

    @property
    def script(self) -> list:
        return self.__script

    @script.setter
    def script(self, src: str):
        self.__script = []
        self.__script = Function._src_split(src)
        self.__static_symbol_setup()

    @staticmethod
    def _src_split(src: str):  # 最丑的一段代码（
        src_list = []
        for line in re.sub('//.+', '', src).strip().split('\n'):
            result = []
            line = line.strip()
            i = 0
            this = ''
            str_flag = False
            py_flag = False
            while i < len(line):
                if line[i].isspace():
                    if str_flag or py_flag:
                        this += line[i]
                    else:
                        if this != '':
                            result.append(this)
                            this = ''
                else:
                    this += line[i]
                    if line[i] == '"':
                        if str_flag and not (i != 0 and line[i - 1] == '\\'):
                            if this != '':
                                result.append(this)
                                this = ''
                            str_flag = False
                        elif py_flag:
                            pass
                        else:
                            str_flag = True
                    elif line[i] == '`':
                        if py_flag:
                            if this != '':
                                result.append(this)
                                this = ''
                            py_flag = False
                        if str_flag:
                            pass
                        else:
                            py_flag = True
                i += 1
            if this != '':
                result.append(this)
            src_list.append(result)
        return src_list

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.return_type == other.return_type and \
               self.exception == other.exception and self.script == other.script

    def __static_symbol_setup(self):
        static_id = 0
        for idx in range(len(self.__script)):
            for i in range(len(self.__script[idx])):
                if self.__script[idx][i].startswith('"') and self.__script[idx][i].endswith('"'):  # string
                    try:
                        str_obj = eval(self.__script[idx][i])
                    except Exception:
                        raise error.ScriptSyntaxError('(static compile) Invalid string {}'
                                                      .format(self.__script[idx][i]), idx + 1, self.__name)
                    if not isinstance(str_obj, str):
                        raise error.ScriptSyntaxError('(static compile) Invalid string {}'
                                                      .format(self.__script[idx][i]), idx + 1, self.__name)
                    symbol = '$_static_{:#x}'.format(static_id)
                    static_id += 1
                    self.static_symbol[symbol] = str_obj
                    self.__script[idx][i] = symbol
                    continue
                if self.__script[idx][i].startswith('$'):  # symbol
                    if not Function.is_valid_symbol(self.__script[idx][i]):
                        raise error.ScriptSyntaxError('(static compile) Invalid symbol name "{}"'
                                                      .format(self.__script[idx][i]), idx + 1, self.__name)
                    continue
                if self.__script[idx][i].startswith('`') and self.__script[idx][i].endswith('`'):  # python
                    try:
                        obj = eval(self.__script[idx][i].strip('`'))
                    except Exception:
                        raise error.ScriptSyntaxError('(static compile) Execute Python {} got Error, call stack: {}'
                                                      .format(self.__script[idx][i], traceback.format_exc()), idx + 1,
                                                      self.__name)
                    if not isinstance(obj, str):
                        obj = str(obj)
                    symbol = '$_static_{:#x}'.format(static_id)
                    static_id += 1
                    self.static_symbol[symbol] = obj
                    self.__script[idx][i] = symbol
                    continue
                if i == 0:  # begin of statement
                    if self.__script[idx][i] not in ('STRING-RETURN-CLEAR', 'CLICK', 'FILL', 'FIND-XPATH',
                                                     'STRING-RETURN', 'SLEEP', 'SEARCH', 'SAVE-TEXT', 'USE'):
                        raise error.ScriptSyntaxError('(static compile) Unsupported KEY {}'
                                                      .format(self.__script[idx][i]), idx + 1, self.__name)

    @staticmethod
    def is_valid_symbol(symbol: str):
        return re.match(r'^\$[a-zA-Z_][a-zA-Z0-9_]*$', symbol) is not None


class Mapping:
    def __init__(self, name='default', url='about:blank'):
        self.__name = name
        self.__url = url
        self.functions = []
        self.elements = []
        self.actions = []

    def __str__(self) -> str:
        return 'Mapping <{}> @ {}'.format(self.__name, self.__url)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name: str):
        self.__name = new_name

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, new_url: str):
        self.__url = new_url

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.url == other.url and len(self.functions) == len(other.functions) and \
               len(self.elements) == len(other.elements) and len(self.actions) == len(other.actions) and \
               all(map(lambda item: item[0] == item[1], zip(self.functions, other.functions))) and \
               all(map(lambda item: item[0] == item[1], zip(self.elements, other.elements))) and \
               all(map(lambda item: item[0] == item[1], zip(self.actions, other.actions)))

    def find_function(self, name: str) -> Function:
        for func in self.functions:
            if func.name == name:
                return func
        raise error.NameNotFoundError('Function (name={}) not found, in Mapping {}'.format(name, self.name), name)

    def find_element(self, name: str) -> Element:
        for elem in self.elements:
            if elem.name == name:
                return elem
        raise error.NameNotFoundError('Element (name={}) not found, in Mapping {}'.format(self.name, name), name)


def same(obj) -> bool:
    """
    根据类型与比较文件夹中的数据比较
    :param obj: 数据对象
    :return: 是否与比较文件夹中的数据相同
    """
    if isinstance(obj, Mapping):
        map_list = xml_parser.get_mapping_list(resources.MAP_FILE)
        for map_obj in map_list:
            if map_obj.name == obj.name:
                return map_obj == obj
        return False
    if isinstance(obj, list) and isinstance(obj[0], User):
        user_list = xml_parser.get_user_cfg_list(resources.CONFIGURATION_FILE)
        user_list.sort(key=lambda user_obj: user_obj.id)
        obj = sorted(obj, key=lambda user_obj: user_obj.id)
        return user_list == obj
    if isinstance(obj, SchedulerInfo):
        return obj == xml_parser.get_scheduler_cfg(resources.CONFIGURATION_FILE)
    raise TypeError('unsupported type: {}'.format(obj.__class__))
