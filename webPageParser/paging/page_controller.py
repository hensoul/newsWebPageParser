#!/usr/bin/env python
# coding: utf-8
from webPageParser.paging.page_property import PageProperty
from webPageParser.constant.field_const import FieldConst
from webPageParser.constant.node_const import NodeConst
from webPageParser.constant.paging_const import PagingConst
from webPageParser.constant.event_const import EventConst
from webPageParser.event.event_property import EventProperty


class PageController(object):

    def __init__(self, logger, web_driver):
        self.logger = logger
        self.web_driver = web_driver

    def get_page_property(self, paging, html_element, get_field_func):
        if paging is None:
            return PageProperty(1)
        try:
            # TODO 硬编码需要改动的地方
            total_page_field = paging.find('.//'+NodeConst.FIELD+'[@name="'+PagingConst.TOTAL_PAGE+'"]')
            total_count_field = paging.find('.//'+NodeConst.FIELD+'[@name="'+PagingConst.TOTAL_COUNT+'"]')
            page_size_field = paging.find('.//'+NodeConst.FIELD+'[@name="'+PagingConst.PAGE_SIZE+'"]')
            turn_page_trigger_field = paging.find('.//'+NodeConst.FIELD+'[@name="'+PagingConst.TURN_PAGE_TRIGGER+'"]')
            url_field = paging.find('.//'+NodeConst.FIELD+'[@name="'+PagingConst.URL+'"]')

            total_page_num, total_page_num_val = get_field_func(total_page_field, html_element)
            total_count, total_count_val = get_field_func(total_count_field, html_element)
            page_size, page_size_val = get_field_func(page_size_field, html_element)

            page_property = PageProperty(total_page_num_val, total_count_val, page_size_val)
            if turn_page_trigger_field is not None:
                page_property.turn_page_ele_xpath = turn_page_trigger_field.get(FieldConst.XPATH)
            if turn_page_trigger_field is not None:
                page_property.turn_page_waiting_times = turn_page_trigger_field.get(FieldConst.WAITING_TIMES)
            if url_field is not None:
                page_property.turn_page_para_url = url_field.get(FieldConst.VALUE)

            return page_property
        except Exception as e:
            self.logger.error("Page: %s,Get page infor error for section: %s" % self.page_url)
            self.logger.error(e.msg)
            return PageProperty(1)

    def turn_page(self, page_property, event_func, reload_func):

        if page_property.has_next_page and self.turn_page_enable(page_property.turn_page_ele_xpath):
            waiting_times = page_property.turn_page_waiting_times
            element_xpath = page_property.turn_page_ele_xpath
            url_pattern = page_property.turn_page_para_url

            event_pro = EventProperty()
            event_pro.waiting_times = waiting_times
            event_pro.element_xpath = element_xpath
            event_pro.total_time = 1
            if waiting_times is None:
                waiting_times = 5
            if url_pattern is not None and url_pattern != "":
                url = self.__build_turn_page_url(url_pattern)
                reload_func(url)
                event_pro.name = EventConst.MOVE_TO_PAGE_DOWN
                event_func(event_pro)
            else:
                event_pro.name = EventConst.CLICK
                event_func(event_pro)
            return True
        else:
            return False

    def __build_turn_page_url(self, url_pattern):
        # 例如 page_url = http://www.xxx.com  url_pattern = ?page=1
        turn_page_url = self.page_url + url_pattern
        return turn_page_url

    def turn_page_enable(self, xpath):
        element = None
        try:
            element = self.web_driver.find_element_by_xpath(xpath)
        except Exception as e:
            self.logger.error("Page trigger: %s, Can not get turn page element by xpath : %s" % xpath)
            self.logger.error(e.msg)
        finally:
            if element is None:
                return False
            else:
                return True
