#!/usr/bin/env python
# coding: utf-8
from webPageParser.util.html_to_json_parser import HtmlTextToJsonParser
from webPageParser.util.request_util import UrlRequest
import sys
print(sys.path)

class StaticPageParser(object):

    def __init__(self, url, xml_file, logger):
        self.logger = logger
        self.xml_file = xml_file
        self.url = url

    def get_json(self):
        html_txt = UrlRequest.get_content(self.url)
        parser = HtmlTextToJsonParser(html_txt, self.xml_file, self.logger)
        result_json = parser.get_json()
        return result_json




