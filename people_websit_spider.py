#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/16 17:00
from webPageParser.dynamic_page_parser import DynamicWebPageParser

import logging
import datetime
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("people.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class PeopleWebSiteSpider(object):
    def __init__(self):
        today = datetime.datetime.today()
        self.today_mid_night = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)

    def get_url_list(self, culumn_url_list):
        column_xml_file = "xml/peopel/cai_jing.xml"
        article_list = []
        parser = DynamicWebPageParser("", column_xml_file, logger)
        for url in culumn_url_list:
            parser.reload_web_page(url)
            articles_json = parser.get_json()
            article_list = articles_json["articleList"]
        if parser is not None:
            parser.destroy()
        return article_list

    def start_spider(self):
        target_url_list = ["http://finance.people.com.cn/index.html"]

        url_list = self.get_url_list(target_url_list)
        detail_page_parser = DynamicWebPageParser("", "xml/yicai/detail.xml", logger)

        for url in url_list:
            detail_page_parser.reload_web_page(url)
            detail_json = detail_page_parser.get_json()
            print(detail_json)


if __name__ == '__main__':

    yicai_spider = PeopleWebSiteSpider()
    yicai_spider.start_spider()

