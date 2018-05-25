#!/usr/bin/env python
# coding: utf-8
from webPageParser.dynamic_page_parser import DynamicWebPageParser

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class LianjiaData(object):

    def get_ershou_house(self):
        url = "https://sh.lianjia.com/ershoufang/"
        xml_file = "xml/lianjia.xml"

        parser = DynamicWebPageParser(url, xml_file, logger)
        result = parser.get_json()
        print(result)


if __name__ == '__main__':
    lianjia = LianjiaData()
    lianjia.get_ershou_house()