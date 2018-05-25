#!/usr/bin/env python
# coding: utf-8
from webPageParser.constant.node_const import NodeConst
from selenium.webdriver.common.action_chains import ActionChains
import time
from webPageParser.event.event_property import EventProperty
from webPageParser.constant.event_const import EventConst


class EventHandler(object):

    def __init__(self, web_driver, logger):
        self.web_driver = web_driver
        self.logger = logger

    def _execute_event(self, xml_element):
        """如果有<events><events>节点，定义有事件动作需要执行"""
        events = xml_element.find(NodeConst.EVENTS)
        if events is not None:
            for event in events:

                event_property = EventProperty()
                event_property.name = event.get(EventConst.NAME)
                event_property.total_time = event.get(EventConst.TOTAL_TIMES)
                event_property.element_xpath = event.get(EventConst.ELEMENT_XPATH)
                event_property.elements_xpath = event.get(EventConst.ELEMENTS_XPATH)
                event_property.waiting_times = event.get(EventConst.WAITING_TIMES)
                event_property.set_value = event.get(EventConst.SET_VALUE)

                if event_property.total_time == -1:   # 一直执行事件，直到条件不满足，退出
                    self.__event_loop_forever(event_property)
                else:
                    self.__event_loop(event_property)

            return True
        else:
            return False

    def __event_loop_forever(self, event_property):
        """
        一直执行事件，直到执行事件的 html 控件在 html 页面里面找不到，
        例如下拉翻页，直到最后一页没有下一页按钮出现 ,事件执行结束 
               """

        # 这个判断条件可扩展
        while self.__get_element_by_xpath(event_property.real_element_xpath) is not None:
            self.execute_action(event_property)

    def __event_loop(self, event_property):
        """执行固定次数的事件，例如翻页，知道总页数"""
        for x in range(0, event_property.total_time):
            self.execute_action(event_property)

    def execute_action(self, event_property):
        try:
            if event_property.is_multi_element is True:
                event_elements = self.__get_elements_by_xpath(event_property.elements_xpath)
                for event_element in event_elements:
                    self.__execute_event_on_element(event_property, event_element)
            elif event_property.is_multi_element is False:
                event_element = self.__get_element_by_xpath(event_property.element_xpath)
                self.__execute_event_on_element(event_property, event_element)
            elif event_property.is_multi_element is None:  # 鼠标滑到浏览器最下面，就不需要指定页面上的 HTML 控件
                self.__execute_event_on_element(event_property, None)

        except Exception as e:
            self.logger.error("Page: %s, Event error! event name:%s, event element xpath: %s" %
                              (self.page_url, event_property.name, event_property.element_xpath))
            self.logger.error(e.msg)

    def __execute_event_on_element(self, event_property, element):
        # do not use the selenium action chain click,because the element which you want click probably invisible in
        # phantomJS when the element out of the range of max window size ,
        # PhantomJS uses 400x300 by default for window size(set a bigger size is not the perfect solution).
        # So use javascript to click element. (the others event should consider this situation
        # and can reference this solution too ) like move to ,mouse over and so on
        # http://stackoverflow.com/questions/19663963/element-click-not-executed-when-using-phantomjs-selenium-webdriver-in-net
        # TODO selenium 最新版本已经不支持 phantomjs，没有测试过 chromeserver.exe 是否有这个问题，
        # TODO 如果没有可以不用使用js执行事件,直接用 selenium Action
        if event_property.name == EventConst.CLICK:
            self.web_driver.execute_script("arguments[0].click();", element)
        elif event_property.name == EventConst.MOVE_TO_PAGE_DOWN:
            self.web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        elif event_property.name == EventConst.MOUSE_OVER:
            self.web_driver.execute_script("arguments[0].onmouseover();", element)
        elif event_property.name == EventConst.SET_VALUE:
            self.web_driver.execute_script("arguments[0].value = %;" % str(event_property.set_value), element)
        elif event_property.name == EventConst.MOVE_TO:
            actions = ActionChains(self.web_driver)
            actions.move_to_element(element)
            actions.click(element)
            actions.perform()
        waiting_times = int(event_property.waiting_times)
        time.sleep(waiting_times)

    def __get_element_by_xpath(self, xpath):
        element = None
        try:
            element = self.web_driver.find_element_by_xpath(xpath)
        except Exception as e:
            self.logger.error("Page: %s, Can not get event element by xpath : %s" % (self.page_url, xpath))
            self.logger.error(e.msg)
        finally:
            return element

    def __get_elements_by_xpath(self, xpath):
        element = None
        try:
            element = self.web_driver.find_elements_by_xpath(xpath)
        except Exception as e:
            self.logger.error("Page: %s, Can not get event element by xpath : %s" % (self.page_url, xpath))
            self.logger.error(e.msg)
        finally:
            return element


