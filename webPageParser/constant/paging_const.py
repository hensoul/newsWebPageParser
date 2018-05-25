#!/usr/bin/env python
# coding: utf-8
from webPageParser.constant.base_const import Const


class __PagingConst(Const):
    def raise_const_error(self, name):
        raise self.ConstError("Can't change PagingConst property '%s'" % name)

    def __init__(self):
        self._TOTAL_PAGE = "totalPage"
        self._TOTAL_COUNT = "totalCount"
        self._PAGE_SIZE = "pageSize"
        self._TURN_PAGE_TRIGGER = "turnPageTrigger"
        self._URL = "url"

    @property
    def TOTAL_PAGE(self):
        return self._TOTAL_PAGE

    @property
    def TOTAL_COUNT(self):
        return self._TOTAL_COUNT

    @property
    def PAGE_SIZE(self):
        return self._PAGE_SIZE

    @property
    def TURN_PAGE_TRIGGER(self):
        return self._TURN_PAGE_TRIGGER

    @property
    def URL(self):
        return self._URL


PagingConst = __PagingConst()


