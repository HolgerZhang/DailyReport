# coding = utf-8
"""
file: bot/xml_parser.py
author: holger
version: 3.0
license: AGPL-3.0
belongs: WebBot-BotCore
"""

from xml.etree import ElementTree

import bot.util
from bot import version

__all__ = ['get_mapping_list', 'get_scheduler_cfg', 'get_user_cfg_list', 'xml2dict', 'Resources']


def _get_elem_obj(elem_root: ElementTree.Element) -> bot.util.Element:
    target, value, text = '', '', ''
    for child in elem_root:
        if child.tag == 'target':
            target = child.text
        elif child.tag == 'value':
            value = child.text
        elif child.tag == 'text':
            text = child.text
    if elem_root.get('check').lower() == 'true':
        check = True
    elif elem_root.get('check').lower() == 'false':
        check = False
    else:
        raise ValueError()
    return bot.util.Element(name=elem_root.get('name'),
                            target=target,
                            value=value,
                            text=text,
                            check=check)


def _get_func_obj(func_root: ElementTree.Element) -> bot.util.Function:
    func = bot.util.Function(name=func_root.get('name'),
                             return_type=func_root.get('return'),
                             exception=func_root.get('exception'))
    func.script = func_root.text
    return func


def _get_mapping_obj(mapping_root: ElementTree.Element) -> bot.util.Mapping:
    mapping = bot.util.Mapping(name=mapping_root.get('name'))
    for child in mapping_root:
        if child.tag == 'Url':
            mapping.url = child.text
        elif child.tag == 'ElementsList':
            for elem_root in child:
                mapping.elements.append(_get_elem_obj(elem_root))
        elif child.tag == 'FunctionsList':
            for func_root in child:
                mapping.functions.append(_get_func_obj(func_root))
        elif child.tag == 'Action':
            if child.text is not None:
                mapping.actions = child.text.split()
    return mapping


def get_mapping_list(xml_file_path: str) -> list:
    _root = ElementTree.ElementTree(file=xml_file_path).getroot()
    assert version.check_version(version.MAP_MIN_VERSION, float(_root.find('version').text)) <= 0
    _map_list_root = _root.find('MapList')
    if _map_list_root is None:
        raise ValueError()
    return [_get_mapping_obj(map_root) for map_root in _map_list_root]


def get_scheduler_cfg(xml_cfg_path: str) -> bot.util.SchedulerInfo:
    _root = ElementTree.ElementTree(file=xml_cfg_path).getroot()
    assert version.check_version(version.CONFIGURATION_MIN_VERSION, float(_root.find('version').text)) <= 0
    scheduler_cfg_root = _root.find('Scheduler')
    if scheduler_cfg_root is None:
        raise ValueError()
    hour, minute, second = '*', '*', '*'
    for child in scheduler_cfg_root:
        if child.tag == 'hour':
            hour = child.text
        elif child.tag == 'minute':
            minute = child.text
        elif child.tag == 'second':
            second = child.text
    return bot.util.SchedulerInfo(hour, minute, second)


def xml2dict(root: ElementTree.Element) -> dict:
    return {child.tag: child.text for child in root}


def _get_user_cfg(user_root: ElementTree.Element) -> bot.util.User:
    return bot.util.User(user_id=user_root.get('id'), data=xml2dict(user_root))


def get_user_cfg_list(xml_cfg_path: str) -> list:
    _root = ElementTree.ElementTree(file=xml_cfg_path).getroot()
    assert version.check_version(version.CONFIGURATION_MIN_VERSION, float(_root.find('version').text)) <= 0
    user_cfg_root = _root.find('UserList')
    if user_cfg_root is None:
        raise ValueError()
    return [_get_user_cfg(user_root) for user_root in user_cfg_root]


class Resources:
    class Container:
        def __init__(self, root: ElementTree.Element):
            assert root is not None, 'Incomplete resource file'
            self.__data = xml2dict(root)

        def __getattr__(self, item: str) -> str:
            return_str = self.__data.get(item, None)
            if return_str is None:
                raise AttributeError("Program has no resource named '{}'".format(item))
            return return_str

    def __init__(self, xml_res_path: str):
        _root = ElementTree.ElementTree(file=xml_res_path).getroot()
        self.string = Resources.Container(_root.find('String'))
        self.api = Resources.Container(_root.find('API'))
        self.res = Resources.Container(_root.find('Res'))
