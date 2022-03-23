#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    elsevier 结果最多显示6000条，若超过6000条，需要按照文章类型分别导出
"""


import time
from typing import List
from log import lg


import requests
from doi.Doi import ResultItem,Channel


class ElsevierResultItem(ResultItem):

    def __init__(self, title: str, doi: str, link: str, pdfName: str, articleType: str) -> None:
        super().__init__(title=title,doi=doi)
        self.link = link
        self.pdfName = pdfName
        self.articleType = articleType
        pass


class ElsevierChannel(Channel):
    """a class of Elsevier crawler
    """

    def __init__(self, keyWord: str) -> None:
        """init an object of ElsevisetChannel

        Args:
            keyWord (str): the search key word
        """
        self.base_url = 'https://www.sciencedirect.com/search/api?qs={}'.format(
            keyWord)
        self.offset = 0
        self.articleTypes = ''
        self.token = 'VkpQTi0mNr1cvMPj9YjSL0JEUiamPgFfLE1JCWelNuDUxq5CkGPSHzjKmtgHLBUpSUpuDKOKD0%2FBCmiYMANVgj1bui3%2B%2BLbxysr3jtlDm%2FE2ZzewNcQ6r8nN5wSsvRzwvKdDbfVcomCzYflUlyb3MA%3D%3D'

        pass

    def __gen_urls(self, articleType: List) -> List[str]:
        """generate pages' url of search result

        Args:
            articleType (List): a list of articles types; the item is a list : [article type , article nums of this type]

        Return:
            a list of urls of pages
        """
        urls = []
        baseUrl = self.base_url+"&show=100&offset={}&lastSelectedFacet=articleTypes&articleTypes={}&t=" + \
            self.token+"&hostname=www.sciencedirect.com"
        t, num = articleType[0], int(articleType[1])
        for i in range(0, num, 100):
            url = baseUrl.format(i, t)
            urls.append(url)
        return urls

    def __getPageContent(self, url: str) -> dict:
        """get reponse of this url

        Args:
            url (str): page url

        Returns:
            dict: a json object of page content , in python this is a dic type;
        """
        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52',
            'Referer': url,
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'sec-ch-ua-mobil': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-mode': 'cors',
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        return response.json()

    def __parsePageContent(self, response: dict) -> List[ElsevierResultItem]:
        """
        parse json from resopnse, return a list of articles info
        :param response:
        :return:[[title,doi,link,pdfName,articleType],...]
        """

        results = []
        
        for item in response['searchResults']:
            title = item['title']
            doi = ''
            link = ''
            pdfName = ''
            articleType = ''
            try:
                doi = item['doi']
            except Exception as e:
                lg.error(str(e))
                pass
            try:
                link = item['pdf']['downloadLink']
            except Exception as e:
                lg.error(str(e))
            try:
                pdfName = item['pdf']['filename']
            except Exception as e:
                lg.error(str(e))
            try:
                articleType = item['articleTypeDisplayName']
            except Exception as e:
                lg.error(str(e))
            if doi=='':
                continue
            results.append(ElsevierResultItem(title=title,doi=doi,link=link,pdfName=pdfName,articleType=articleType))
        return results

    def __get_article_type(self) -> List[List]:
        """get article type of all search results

        Returns:
            List[List]: [[type name, nums of this type],...]
        """
        url = self.base_url+"&t="+self.token+"&hostname=www.sciencedirect.com"
        response = self.__getPageContent(url)
        articleInfo = []
        for item in response['facets']['articleTypes']:
            articleInfo.append([item['key'], item['value']])
        return articleInfo

    def getSearchResults(self,delay=15) -> List[ElsevierResultItem]:
        """return search result

        Args:
            delay (int, optional): delay 15s when get page. Defaults to 15.

        Returns:
            List[ElsevierResultItem]: [description]
        """
        res = []
        articleTypes = self.__get_article_type()
        lg.info("Already get article type!")
        task_nums = sum([int(i[1]) for i in articleTypes])
        lg.info("Search results: {} nums.".format(task_nums))
        for at in articleTypes:
            urls = self.__gen_urls(at)
            for url in urls:
                content = self.__getPageContent(url)
                results = self.__parsePageContent(content)
                res = res + results
                lg.info("There are {} records left.".format(task_nums-len(res)))
                time.sleep(15)
        return res
