#!/usr/bin/env python
# coding: utf-8
import requests


DEFAULT_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# DEFAULT_PROXIES = {"http": "http://101.68.73.54:53281", "https": "https://114.235.82.126:8118"}


class UrlRequest(object):

    @staticmethod
    def get_response(url, method="GET", headers=None, data=None, proxy=None):
        if headers is not None:
            request_headers = headers
        else:
            request_headers = DEFAULT_HEADER
        time_out_second = 300
        request_data = None
        if data is not None:
            request_data = data
        request_proxy = None
        if proxy is not None:
            request_proxy = proxy
        # else:
        #     request_proxy = DEFAULT_PROXIES
        response = requests.request(url=url, method=method, headers=request_headers,
                                    timeout=time_out_second, proxies=request_proxy, data=request_data)
        return response

    @staticmethod
    def get_content(url, method="GET", headers=None, data=None, proxy=None):
        response = UrlRequest.get_response(url, method, headers, data, proxy)
        is_gbk = response.headers.get("content-type", "").find("gbk") >= 0
        response_data = response.content
        if is_gbk:
            result = response_data.decode("gbk")
        else:
            result = response_data

        return result

    @staticmethod
    def get_json(url, method="GET", headers=None, data=None, proxy=None):
        response = UrlRequest.get_response(url, method, headers, data, proxy)
        is_gbk = response.headers.get("content-type", "").find("gbk") >= 0
        response_data = response.json()
        if is_gbk:
            result = response_data.decode("gbk")
        else:
            result = response_data

        return result

