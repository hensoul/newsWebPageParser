#!/usr/bin/env python
# coding: utf-8
from webPageParser.constant.base_const import Const


class __FieldConst(Const):
    def raise_const_error(self, name):
        raise self.ConstError("Can't change FieldConst property '%s'" % name)

    def __init__(self):
        self._NAME = "name"
        self._XPATH = "xpath"
        self._RESULT_TYPE = "resultType"
        self._VALUE = "value"
        self._EXTEND = "extend"
        self._URL = "url"
        self._REGEXP = "regexp"
        self._WAITING_TIMES = "waitingTimes"

        self._RESULT_TYPE_CONST = "const"
        self._RESULT_TYPE_TEXT = "text"
        self._RESULT_TYPE_TEXT_CONTENT = "textContent"
        self._RESULT_TYPE_TEXT_HTML = "textHtml"
        self._RESULT_TYPE_BOOLEAN = "boolean"
        self._RESULT_TYPE_OBJECT = "object"
        self._RESULT_TYPE_LIST = "list"
        self._RESULT_TYPE_CONST_LIST = "constList"

        self._EXTEND_TRUE = "TRUE"
        self._EXTEND_FALSE = "FALSE"

    @property
    def NAME(self):
        return self._NAME

    @property
    def XPATH(self):
        return self._XPATH

    @property
    def RESULT_TYPE(self):
        return self._RESULT_TYPE

    @property
    def VALUE(self):
        return self._VALUE

    @property
    def EXTEND(self):
        return self._EXTEND

    @property
    def URL(self):
        return self._URL

    @property
    def REGEXP(self):
        return self._REGEXP

    @property
    def WAITING_TIMES(self):
        return self._WAITING_TIMES

    @property
    def RESULT_TYPE_CONST(self):
        return self._RESULT_TYPE_CONST

    @property
    def RESULT_TYPE_TEXT(self):
        return self._RESULT_TYPE_TEXT

    @property
    def RESULT_TYPE_TEXT_COTENT(self):
        return self._RESULT_TYPE_TEXT_CONTENT

    @property
    def RESULT_TYPE_TEXT_HTML(self):
        return self._RESULT_TYPE_TEXT_HTML

    @property
    def RESULT_TYPE_BOOLEAN(self):
        return self._RESULT_TYPE_BOOLEAN

    @property
    def RESULT_TYPE_OBJECT(self):
        return self._RESULT_TYPE_OBJECT

    @property
    def RESULT_TYPE_LIST(self):
        return self._RESULT_TYPE_LIST

    @property
    def RESULT_TYPE_CONST_LIST(self):
        return self._RESULT_TYPE_CONST_LIST

    @property
    def EXTEND_TRUE(self):
        return self._EXTEND_TRUE

    @property
    def EXTEND_FALSE(self):
        return self._EXTEND_FALSE

FieldConst = __FieldConst()

"""
FieldConst = __FieldConst()
FieldConst.NAME = "name"  
也可以这么定义常量，但是使用常量时，IDE不会提示，使用不便
所以使用property
"""
