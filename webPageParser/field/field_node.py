# #!/usr/bin/env python
# # coding: utf-8
#
#
# class FieldNode(object):
#
#     NAME = "name"
#     XPATH = "xpath"
#     RESULT_TYPE = "resultType"
#     VALUE = "value"
#     EXTEND = "extend"
#     URL = "url"
#     REGEXP = "regexp"
#     WAITING_TIMES = "waitingTimes"
#
#     RESULT_TYPE_CONST = "const"
#     RESULT_TYPE_STRING = "string"
#     RESULT_TYPE_BOOLEAN = "boolean"
#     RESULT_TYPE_OBJECT = "object"
#     RESULT_TYPE_LIST = "list"
#     RESULT_TYPE_CONST_LIST = "constList"
#
#     EXTEND_TRUE = "TRUE"
#     EXTEND_FALSE = "FALSE"
#
#     def __init__(self, name, result_type, xpath, is_extend, html_element):
#         self._name = name
#         self._result_type = result_type
#         self._xpath = xpath
#         self._is_extend = is_extend
#         self._html_element = html_element
#
#     def _get_one_field(self):
#         try:
#             if self._result_type == FieldNode.FIELD_ATTR_RESULT_TYPE_VAL_STRING:
#                 value = self.__find_one_by_xpath(self._xpath, html_element)
#                 if value:
#                     value = self.clean_html_val(value.encode("utf-8"))
#             elif self._result_type == FieldNode.FIELD_ATTR_RESULT_TYPE_VAL_OBJECT:
#                 value = {}
#                 if self._xpath is not None and len(self._xpath) > 0:
#                     html_element = self.__find_one_by_xpath(self._xpath, html_element)
#                 for obj_child_field in field.findall(FieldNode.TAG_FIELD):
#                     obj_child_field_key, obj_child_field_value = self.__get_one_field(obj_child_field, html_element)
#                     value[obj_child_field_key] = obj_child_field_value
#
#             elif self._result_type == FieldNode.FIELD_ATTR_RESULT_TYPE_VAL_LIST:
#                 value = []
#                 list_field_extend = field.get(FieldNode.FIELD_ATTR_EXTEND)
#                 html_elements = []
#                 if self._xpath is not None and len(self._xpath) > 0:
#                     html_elements = self.__find_all_by_xpath(self._xpath, html_element)
#                 if len(html_elements) > 0:
#                     for html_ele in html_elements:
#                         for list_child_field in field.findall(FieldNode.TAG_FIELD):
#                             list_child_field_key, list_child_field_value = self.__get_one_field(list_child_field,
#                                                                                                 html_ele)
#                             if list_field_extend and str.upper(list_field_extend) == FieldNode.FIELD_ATTR_EXTEND_VAL_TRUE:
#                                 value.extend(list_child_field_value)
#                             else:
#                                 value.append(list_child_field_value)
#             else:
#                 self.logger.error("Parse xml occur error, class:HtmlTextToJsonParser,method:get_result")
#                 self.logger.error("Invalidate resultType : %s in xml : %s"(field_type, str(field)))
#
#         except Exception as e:
#             self.logger.error("Parse xml occur error, class:HtmlTextToJsonParser,method:__get_one_field")
#             self.logger.error("Field: %s", str(field))
#             self.logger.error(e)
#         return field_name, value
#
#
