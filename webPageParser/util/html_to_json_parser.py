#!/usr/bin/env python
# coding: utf-8
import re
import xml.etree.ElementTree as ET
import yaml
from lxml import html
from webPageParser.constant.field_const import FieldConst


class HtmlTextToJsonParser(object):

    def __init__(self, html_txt, xml_file, logger):
        self.html_element = html.fromstring(html_txt)
        self.xml_root = self.load_xml(xml_file)
        self.logger = logger

    def load_xml(self, xml_file):
        try:
            source = open(xml_file)
            xml = ET.parse(source)
            source.close()
            return xml.getroot()
        except Exception as e:
            self.logger.error("Parse xml file occur exception! xml file: %s" % str(xml_file))
            self.logger.error(e)
            return None

    def get_json(self):
        result = None
        if self.xml_root is not None:
            result = {}
            for field in self.xml_root:
                field_key, field_value = self.__get_one_field(field, self.html_element)
                result[field_key] = field_value
            return result
        else:
            return result

    def __get_one_field(self, field, html_element):
        field_name = field.get(FieldConst.NAME)
        field_type = field.get(FieldConst.RESULT_TYPE)
        xpath = field.get(FieldConst.XPATH)
        try:
            if field_type == FieldConst.RESULT_TYPE_TEXT:
                value = self.__find_one_by_xpath(xpath, html_element)
            elif field_type == FieldConst.RESULT_TYPE_OBJECT:
                value = {}
                if xpath is not None and len(xpath) > 0:
                    html_element = self.__find_one_by_xpath(xpath, html_element)
                for obj_child_field in field:
                    obj_child_field_key, obj_child_field_value = self.__get_one_field(obj_child_field, html_element)
                    value[obj_child_field_key] = obj_child_field_value

            elif field_type == FieldConst.RESULT_TYPE_LIST:
                value = []
                list_field_extend = field.get(FieldConst.EXTEND)
                html_elements = []
                if xpath is not None and len(xpath) > 0:
                    html_elements = self.__find_all_by_xpath(xpath, html_element)
                if len(html_elements) > 0:
                    for html_ele in html_elements:
                        for list_child_field in field:
                            list_child_field_key, list_child_field_value = self.__get_one_field(list_child_field, html_ele)
                            if list_field_extend and str.upper(list_field_extend) == FieldConst.EXTEND_TRUE:
                                value.extend(list_child_field_value)
                            else:
                                value.append(list_child_field_value)
            else:
                self.logger.error("Parse xml occur error, class:HtmlTextToJsonParser,method:get_result")
                self.logger.error("Invalidate resultType : %s in xml : %s"(field_type, str(field)))

        except Exception as e:
            self.logger.error("Parse xml occur error, class:HtmlTextToJsonParser,method:__get_one_field")
            self.logger.error("Field: %s", str(field))
            self.logger.error(e)
        return field_name, value

    @staticmethod
    def __find_one_by_xpath(xpath, html_element):
        result = None
        if html_element is not None:
            value = html_element.xpath(xpath)
            if value and len(value) > 0:
                result = value[0]
        return result

    @staticmethod
    def __find_all_by_xpath(xpath, html_element):
        result = None
        if html_element is not None:
            result = html_element.xpath(xpath)
        return result

    def __find_js_variable(self, js_script_xpath, variable_regex, variable_index, key=None):
        js_str = self.find_one_by_xpath(js_script_xpath)
        js_variables = re.findall(variable_regex, js_str)
        js_variable = js_variables[variable_index]
        js_variable = js_variable.strip()
        js_variable = js_variable.replace("\r", "")
        js_variable = js_variable.replace("\n", "")
        js_variable_value = re.findall(r"{.*}", js_variable)[0]
        js_variable_value = js_variable_value.strip()
        if key:
            valid_json = yaml.load(js_variable_value)
            return valid_json[key]
        else:
            valid_json = yaml.load(js_variable_value)
            return valid_json

