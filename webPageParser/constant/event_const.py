#!/usr/bin/env python
# coding: utf-8
from webPageParser.constant.base_const import Const


class __EventConst(Const):

    def raise_const_error(self, name):
        raise self.ConstError("Can't change EventConst property '%s'" % name)

    def __init__(self):
        self._CLICK = "click"
        self._MOVE_TO_PAGE_DOWN = "move_down"
        self._MOVE_TO = "move_to"
        self._MOUSE_OVER = "mouse_over"
        self._SET_VALUE = "set_value"

        self._NAME = "name"
        self._TOTAL_TIMES = "totalTimes"
        self._ELEMENT_XPATH = "elementXpath"
        self._ELEMENTS_XPATH = "elementsXpath"
        self._WAITING_TIMES = "waitingTimes"

    @property
    def CLICK(self):
        return self._CLICK

    @property
    def MOVE_TO_PAGE_DOWN(self):
        return self._MOVE_TO_PAGE_DOWN

    @property
    def MOVE_TO(self):
        return self._MOVE_TO

    @property
    def MOUSE_OVER(self):
        return self._MOUSE_OVER

    @property
    def SET_VALUE(self):
        return self._SET_VALUE

    @property
    def NAME(self):
        return self._NAME

    @property
    def TOTAL_TIMES(self):
        return self._TOTAL_TIMES

    @property
    def ELEMENT_XPATH(self):
        return self._ELEMENT_XPATH

    @property
    def ELEMENTS_XPATH(self):
        return self._ELEMENTS_XPATH

    @property
    def WAITING_TIMES(self):
        return self._WAITING_TIMES


EventConst = __EventConst()

