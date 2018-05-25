#!/usr/bin/env python
# coding: utf-8
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from lxml import html
import xml.etree.ElementTree as ET
from webPageParser.constant.field_const import FieldConst
from webPageParser.constant.node_const import NodeConst
from webPageParser.event.event_handler import EventHandler
from webPageParser.paging.page_controller import PageController
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DynamicWebPageParser(EventHandler, PageController):

    def __init__(self, page_url, xml_path, logger, req_headers=None):
        self.logger = logger
        self.root_html = None
        self.page_url = page_url
        self.load_page_success = False
        self.web_driver = None
        self.root_json = None
        self.req_headers = req_headers
        self.load_web_driver_by_url(page_url)
        self.load_xml(xml_path)

        EventHandler.__init__(self, self.web_driver, self.logger)
        PageController.__init__(self, self.logger, self.web_driver)

    @staticmethod
    def is_xpath_ele_exist(content, xpath):
        import lxml.html as PARSER
        root = PARSER.fromstring(content)
        if root.xpath(xpath):
            return True
        return False

    def load_xml(self, xml_file):
        try:
            source = open(xml_file, encoding='utf-8')
            xml = ET.parse(source)
            source.close()
            self.root_json = xml.getroot()
        except Exception as e:
            self.logger.error("Parse xml file occur exception! xml file: %s" % str(xml_file))
            self.logger.error(e)

    def load_web_driver_by_url(self, url):
        try:
            if self.web_driver:
                self.web_driver.quit()
            # if self.req_headers:
            #     for key in self.req_headers:
            #         val = self.req_headers[key]
            #         DesiredCapabilities.CHROME[key] = val

            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            self.web_driver = webdriver.Chrome(chrome_options=chrome_options)
            self.web_driver.implicitly_wait(20)
            self.web_driver.set_page_load_timeout(300)
            self.load_page_success = True

            if url is not None and url != "":
                self.web_driver.get(url)
                self.root_html = self.__build_html_element(self.web_driver.page_source)
        except Exception as e:
            self.load_page_success = False
            self.logger.error("Load page occur error ! url: %s" % str(url))
            self.logger.error(e.msg)

    def reload_web_page(self, url):
        try:
            self.web_driver.get(url)
            self.load_page_success = True
            self.root_html = self.__build_html_element(self.web_driver.page_source)
        except Exception as e:
            self.load_page_success = False
            self.logger.error("Reload page occur error ! url: %s" % str(url))
            self.logger.error(e.msg)

    def __refresh_root_html(self):
        self.root_html = self.__build_html_element(self.web_driver.page_source)

    def get_web_driver_current_url(self):
        current_url = self.web_driver.current_url
        return current_url

    def get_json(self):
        if self.web_driver is None or self.load_page_success is False:
            return None
        result = {}
        if self.root_json is not None:
            result = self.root_json.attrib
            for field in self.root_json:
                name, value = self.get_one_field(field, self.root_html)
                result[name] = value
        # self.destroy()
        return result

    def get_one_field(self, field, html_element):

        field_name = field.get(FieldConst.NAME)
        field_type = field.get(FieldConst.RESULT_TYPE)
        xpath = field.get(FieldConst.XPATH)

        # 常量值，在配置文件直接指定
        const_value = field.get(FieldConst.VALUE)
        if const_value and len(const_value) > 0:
            return field_name, const_value

        # 页面需要根据配置 URL 加载
        field_url = field.get(FieldConst.URL)
        if field_url is not None:
            self.reload_web_page(field_url)
            html_element = self.root_html

            # 页面加载失败
            if self.load_page_success is False:
                return field_name, None

        # 执行事件，如一些页面需要鼠标执行一些动作， html控件才会加载出来
        execute_event_result = self._execute_event(field)
        # 执行完事件，刷新html页面数据，
        if execute_event_result:
            self.__refresh_root_html()
            html_element = self.root_html

        value = None
        try:
            if field_type == FieldConst.RESULT_TYPE_TEXT:
                value = self.__find_one_by_xpath(xpath, html_element)
                if value is not None:
                    value = self.clean_html_val(value)
            elif field_type == FieldConst.RESULT_TYPE_TEXT_COTENT:
                value = self.__find_one_by_xpath(xpath, html_element)
                if value is not None:
                    text_content = value.text_content()
                    value = self.clean_html_val(text_content)
            elif field_type == FieldConst.RESULT_TYPE_TEXT_HTML:
                value = self.__find_one_by_xpath(xpath, html_element)
                if value is not None:
                    value = html.tostring(value, encoding="utf-8", pretty_print=True, method="html")
            elif field_type == FieldConst.RESULT_TYPE_OBJECT:
                value = {}
                if xpath is not None and len(xpath) > 0:
                    html_element = self.__find_one_by_xpath(xpath, html_element)
                for obj_child_field in field.findall(NodeConst.FIELD):
                    obj_child_field_key, obj_child_field_value = self.get_one_field(obj_child_field, html_element)
                    value[obj_child_field_key] = obj_child_field_value

            elif field_type == FieldConst.RESULT_TYPE_LIST:
                value = []
                is_extend = field.get(FieldConst.EXTEND)

                # 分页数据 只有result type 是list 的时候才会存在分页
                paging = field.find(NodeConst.PAGING)
                page_property = self.get_page_property(paging, html_element, self.get_one_field)
                # TODO 分页需要修改，应该改成是否有下一页，？ 是不是可以使用 yield
                for x in range(1, page_property.total_page_num + 1):
                    html_elements = []
                    if xpath is not None and len(xpath) > 0:
                        html_elements = self.__find_all_by_xpath(xpath, html_element)
                    if len(html_elements) > 0:
                        for html_ele in html_elements:
                            for list_child_field in field.findall(NodeConst.FIELD):
                                list_child_field_key, list_child_field_value = self.get_one_field(list_child_field, html_ele)
                                if is_extend and str.upper(is_extend) == FieldConst.EXTEND_TRUE:
                                    value.extend(list_child_field_value)
                                else:
                                    value.append(list_child_field_value)
                    # 翻页， 刷新页面
                    page_property.current_page_num = x

                    # 翻页失败结束查找分页数据
                    turn_page_result = self.turn_page(page_property, self.execute_action, self.reload_web_page)
                    if turn_page_result is False:
                        break
                    self.__refresh_root_html()
                    html_element = self.root_html
            else:
                self.logger.error("Parse xml occur error, class:HtmlTextToJsonParser,method:get_result")
                self.logger.error("Invalidate resultType : %s in xml : %s"(field_type, str(field)))

        except Exception as e:
            self.logger.error("Parse xml occur error, class:HtmlTextToJsonParser,method:__get_one_field")
            self.logger.error("Field: %s", str(field))
            self.logger.error(e)
        finally:
            return field_name, value

    @staticmethod
    def __build_html_element(html_text):
        html_element = html.fromstring(html_text.encode('utf-8'))
        return html_element

    @staticmethod
    def __find_one_by_xpath(xpath, html_element):
        result = None
        if html_element is not None:
            value = html_element.xpath(xpath)
            if value and len(value) > 0:
                result = value[0]
        return result

    @staticmethod
    def clean_html_val(val):
        result = val
        if result:
            result = str(result).strip()
            result = result.replace("\n", "")
            result = result.replace("\t", "")
        return result

    @staticmethod
    def __find_all_by_xpath(xpath, html_element):
        result = None
        if html_element is not None:
            result = html_element.xpath(xpath)
        return result

    def destroy(self):
        if self.web_driver is not None:
            self.web_driver.quit()


if __name__ == '__main__':
    print("xxxxxxxxxxxxxxxxxxxxxxx")

