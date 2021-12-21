#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    wiley 结果最多显示2000条，需要按照年份分别导出
"""

# !/usr/bin/python3
# -*- coding: utf-8 -*-
import csv
import re
import time
from typing import List
from log import lg

import requests
from doi.Doi import ResultItem, Channel


class WileyResultItem(ResultItem):
    def __init__(self, title: str, doi: str):
        super().__init__(title=title, doi=doi)
        pass


class WileyChannel(Channel):
    """
    a class of Wiley crawler
    """

    def __init__(self, keyWord: str) -> None:
        self.keyWord = keyWord
        self.task_nums = 0
        self.__getTaskNums()
        pass

    def getSearchResults(self, delay=15) -> List[WileyResultItem]:
        """
        return search result
        :param delay: delay 15s when get page. Defaults to 15.
        :return:List[WileyResultItem]
        """
        res = []
        urls = []
        for item in self.__getYearNums():
            start_year, end_year, nums = item[0], item[1], item[2]
            urls = urls + self.__genUrls(start_year=start_year, end_year=end_year, res_nums=nums)
        for url in urls:
            res = res + self.__parsePage(self.__getHtml(url=url))
            lg.info("There are {} records left.".format(self.task_nums - len(res)))
            time.sleep(delay)
        return res

    def __parsePage(self, response: str) -> List[WileyResultItem]:
        """
        return  a list of WileyResultItem
        :param response:
        :return:
        """
        pattern = """<a href="(.*?)" class="publication_title visitable">(.*?)</a>"""
        res = re.findall(pattern, response)
        result_item = []
        for i in res:
            doi = i[0]
            title = i[1]
            title = title.replace('<span onclick="highlight()" class="single_highlight_class">', '').replace('</span>',
                                                                                                             '')
            result_item.append(WileyResultItem(title=title, doi=doi))
        return result_item

    def __getHtml(self, url: str) -> str:
        """
        return html txt
        :param url:
        :return:
        """

        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=120)

        return response.text

    def __genUrls(self, start_year: int, end_year: int, res_nums: int):
        """
        gennerate detail urls
        :param start_year:
        :param end_year:
        :param res_nums:
        :return:
        """
        urls = []
        for i in range(res_nums // 100):
            url = 'https://onlinelibrary.wiley.com/action/doSearch?AfterYear={}&AllField={}&BeforeYear={}&target=default&pageSize=100&startPage={}'
            url = url.format(start_year, self.keyWord, end_year, str(i))
            urls.append(url)
        return urls

    def __getYearNums(self) -> List[List[int]]:
        begin_yaer = 1841
        end_year = int(time.localtime().tm_year)
        # get search result per 15 year
        step = 15
        num_pattern = '<span class="result__count">(.*?)</span>'
        url_pattern = 'https://onlinelibrary.wiley.com/action/doSearch?AllField={}&target=default&AfterYear={}&BeforeYear={}'
        years = [i for i in range(begin_yaer, end_year, step)]
        res = []
        if end_year not in years:
            years.append(end_year)
        for i in range(1, len(years)):
            start_year = years[i - 1]
            end_year = years[i]
            url = url_pattern.format(self.keyWord, start_year, end_year)
            lg.info('当前url： '+url)
            html = self.__getHtml(url=url)
            re_res = re.findall(num_pattern, html)
            if re_res is None or len(re_res)<1:
                lg.info("No paper in these years!")
                continue
            paper_nums = int(re_res[0].replace(',', ''))
            if paper_nums != 0:
                res.append([start_year, end_year, paper_nums])
        return res

    def __getTaskNums(self):
        url = 'https://onlinelibrary.wiley.com/action/doSearch?AllField={}'.format(self.keyWord)
        num_pattern = '<span class="result__count">(.*?)</span>'
        html = self.__getHtml(url=url)
        paper_nums = int(re.findall(num_pattern, html)[0].replace(',', ''))
        self.task_nums = paper_nums
        lg.info("Search results: {} nums.".format(self.task_nums))
