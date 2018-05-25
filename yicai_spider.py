#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/16 17:00
from webPageParser.dynamic_page_parser import DynamicWebPageParser

import logging
import datetime
import time
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("yicai.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class YicaiSpider(object):
    def __init__(self):
        today = datetime.datetime.today()
        self.today_mid_night = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)

    def get_url_list(self, culumn_url_list):
        column_xml_file = "xml/yicai/gu_shi.xml"
        article_url_list = []
        parser = DynamicWebPageParser("", column_xml_file, logger)
        for url in culumn_url_list:
            print(("--------------column url %s start!---------" % url))
            parser.reload_web_page(url)
            articles_json = parser.get_json()
            article_list = articles_json["articleList"]
            print(("--------------column url %s end! 总条数: %d ---------" % (url, len(article_list))))
            for article in article_list:
                date_time_str = article["dateTime"]
                date_time = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
                if date_time > self.today_mid_night:
                    article_url_list.append(article["url"])
                else:
                    print(("=========== Not today article,  url： %s, datetime: %s, " % (article["url"], article["dateTime"])))

        if parser is not None:
            parser.destroy()
        return article_url_list

    def start_spider(self):
        target_url_list = ["http://www.yicai.com/news/gushi/",
                           "http://www.yicai.com/news/policy/",
                           "http://www.yicai.com/news/hongguan/",
                           "http://www.yicai.com/news/jinrong/",
                           "http://www.yicai.com/news/gongsi/",
                           "http://www.yicai.com/news/minsheng/",
                           "http://www.yicai.com/news/shijie/",
                           "http://www.yicai.com/news/comment/",
                           "http://www.yicai.com/news/loushi/",
                           "http://www.yicai.com/news/automobile/",
                           "http://www.yicai.com/news/kechuang/",
                           "http://www.yicai.com/news/fashion/",
                           "http://www.yicai.com/news/jiankangshenghuo/",
                           "http://www.yicai.com/news/dafengwenhua/",
                           "http://www.yicai.com/news/books/",
                           "http://www.yicai.com/news/ad/"]

        start_get_url_time = datetime.datetime.now()
        start_get_url_time.strftime("%Y-%m-%d %H:%M:%S")
        print("############## start get column url ##############")
        print(start_get_url_time)
        url_list = self.get_url_list(target_url_list)

        end_get_url_time = datetime.datetime.now()
        end_get_url_time.strftime("%Y-%m-%d %H:%M:%S")
        print("############## end get column url ##############")
        print(end_get_url_time)

        start_get_detail_time = datetime.datetime.now()
        start_get_detail_time.strftime("%Y-%m-%d %H:%M:%S")
        print("$$$$$$$$$$$$$$$$$$ start get article detail  $$$$$$$$$$$$$$$$$$")
        print(start_get_detail_time)
        detail_page_parser = DynamicWebPageParser("", "xml/yicai/detail.xml", logger)

        for url in url_list:
            print(url)
            detail_page_parser.reload_web_page(url)
            detail_json = detail_page_parser.get_json()
            print(detail_json)

        end_get_detail_time = datetime.datetime.now()
        end_get_detail_time.strftime("%Y-%m-%d %H:%M:%S")
        print("$$$$$$$$$$$$$$$$$$ end get article detail $$$$$$$$$$$$$$$$$$")
        print(end_get_detail_time)


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    start_time.strftime("%Y-%m-%d %H:%M:%S")
    print("******************* start ************************")
    print(start_time)
    yicai_spider = YicaiSpider()
    yicai_spider.start_spider()

    end_time = datetime.datetime.now()
    end_time.strftime("%Y-%m-%d %H:%M:%S")
    print("******************* end ************************")
    print(end_time)
