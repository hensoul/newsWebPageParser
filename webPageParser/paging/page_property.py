#!/usr/bin/env python
# coding: utf-8


class PageProperty(object):

    def __init__(self, total_page_num, total_count=None, page_size=None):
        self._total_page_num = total_page_num
        self._total_count = total_count
        self._page_size = page_size
        self._turn_page_para_url = None
        self._turn_page_ele_xpath = None
        self._turn_page_waiting_times = None
        self._current_page_num = None

    @property
    def current_page_num(self):
        return self._current_page_num

    @current_page_num.setter
    def current_page_num(self, value):
        self._current_page_num = int(value)

    @property
    def turn_page_para_url(self):
        return self._turn_page_para_url

    @turn_page_para_url.setter
    def turn_page_para_url(self, value):
        self._turn_page_para_url = value


    @property
    def turn_page_ele_xpath(self):
        return self._turn_page_ele_xpath

    @turn_page_ele_xpath.setter
    def turn_page_ele_xpath(self, value):
        self._turn_page_ele_xpath = value

    @property
    def turn_page_waiting_times(self):
        return self._turn_page_waiting_times

    @turn_page_waiting_times.setter
    def turn_page_waiting_times(self, value):
        self._turn_page_waiting_times = value

    @property
    def total_page_num(self):
        if self._total_page_num is not None:
            return int(self._total_page_num)
        else:
            if self._total_count is None or len(self._total_count) == 0 or self._page_size is None or len(self._page_size) == 0:
                return 1
            else:
                return (int(self._total_count) + int(self._page_size) - 1) / int(self._page_size)

    @property
    def has_next_page(self):
        if self._current_page_num == self.total_page_num:
            return False
        else:
            return True