# coding = utf-8
"""
file: bot/error.py
author: holger
version: 3.0
license: AGPL-3.0
belongs: WebBot-BotCore
"""


class BotWarning(RuntimeError):
    def __init__(self, what=''):
        super(BotWarning, self).__init__()
        self._what = what

    @property
    def what(self):
        return '[BotWarning] what: {}'.format(self._what)

    def __str__(self):
        return self.what


class FatalError(RuntimeError):
    def __init__(self, what=''):
        super(FatalError, self).__init__()
        self._what = what

    @property
    def what(self):
        return '[FatalError] what: {}'.format(self._what)

    def __str__(self):
        return self.what


class SymbolTypeError(FatalError):
    def __init__(self, what, obj):
        super(SymbolTypeError, self).__init__(what)
        self._type = type(obj)

    @property
    def what(self):
        return '[SymbolTypeError]{}; Type {} is given'.format(super(SymbolTypeError, self).what, self._type)


class UnexpectedValueError(FatalError):
    def __init__(self, what, value):
        super(UnexpectedValueError, self).__init__(what)
        self._value = value

    @property
    def what(self):
        return '[UnexpectedValueError]{}; Unexpected value {} is given'.format(super(UnexpectedValueError, self).what,
                                                                               self._value)


class NameNotFoundError(FatalError):
    def __init__(self, what, name):
        super(NameNotFoundError, self).__init__(what)
        self._name = name

    @property
    def what(self):
        return '[NameNotFoundError]{}; Name "{}" is given'.format(super(NameNotFoundError, self).what, self._name)


class ScriptSyntaxError(FatalError):
    def __init__(self, what, line: int, func_name: str):
        super(ScriptSyntaxError, self).__init__(what)
        self._line = line
        self._name = func_name

    @property
    def what(self):
        return '[ScriptSyntaxError]{}; in script line {}, func {}'.format(super(ScriptSyntaxError, self).what,
                                                                          self._line, self._name)


class IncompleteConfigError(FatalError):
    def __init__(self, config: str):
        super(IncompleteConfigError, self).__init__("incomplete configuration '{}'".format(config))

    @property
    def what(self):
        return '[IncompleteConfigError]{}'.format(super(IncompleteConfigError, self).what)

# def func():
#     raise IncompleteConfigError('map')
#
#
# func()
