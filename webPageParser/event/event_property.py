#!/usr/bin/env python
# coding: utf-8


class EventProperty(object):

    def __init__(self):
        self.__name = None   # 事件名称
        self.__total_time = None  # 事件执行次数
        self.__waiting_times = None  # 事件执行完等待的时间，秒数
        self.__elements_xpath = None  # 执行事件的多个 Html 控件的 xpath
        self.__element_xpath = None  # 执行事件的一个 Html 控件的 xpath
        self.__set_value = None  # 为控件赋值操作，想要赋的值, 例如给 input text 控件输入值

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def total_time(self):
        return self.__total_time

    @total_time.setter
    def total_time(self, value):
        if value is None:
            self.__total_time = 1
        else:
            self.__total_time = int(value)

    @property
    def waiting_times(self):
        return self.__waiting_times

    @waiting_times.setter
    def waiting_times(self, value):
        self.__waiting_times = value

    @property
    def elements_xpath(self):
        return self.__elements_xpath

    @elements_xpath.setter
    def elements_xpath(self, value):
        self.__elements_xpath = value

    @property
    def element_xpath(self):
        return self.__element_xpath

    @element_xpath.setter
    def element_xpath(self, value):
        self.__element_xpath = value

    @property
    def set_value(self):
        return self.__set_value

    @set_value.setter
    def set_value(self, value):
        self.__set_value = value

    @property
    def is_multi_element(self):
        if self.__elements_xpath is not None and len(self.__elements_xpath) > 0:  # 有多个HTML控件需要被触发事件
            return True
        if self.__element_xpath is not None and len(self.__element_xpath) > 0:  # 有一个HTML控件需要被触发事件
            return False
        else:
            return None  # 没有HTML控件需要被触发事件，如鼠标滑到浏览器最下方

    @property
    def real_element_xpath(self):
        if self.__elements_xpath is None:
            return self.__elements_xpath
        else:
            return self.__element_xpath


