import time
from typing import List
import requests
from lxml import etree
from log import lg
from doi.Doi import ResultItem, Channel


class CanadianScienceResultItem(ResultItem):
    def __init__(self, title: str, doi: str):
        super().__init__(title=title, doi=doi)
        pass


class CanadianScienceChannel(Channel):
    """
    a class of CanadianScience crawler
    """

    def __init__(self, keyWord: str) -> None:
        self.keyWord = keyWord
        self.task_nums = 0
        self.__getTaskNum()
        pass

    def getSearchResults(self, delay=15) -> List[CanadianScienceResultItem]:
        """
        return search result
        :param delay: delay 15s when get page. Defaults to 15.
        :return:List[CanadianScienceResultItem]
        """
        res = []
        for url in self.__genUrls():
            r = self.__parseHtml(self.__getHtml(url))
            res = res + r
            lg.info("There are {} records left.".format(self.task_nums - len(res)))
            time.sleep(delay)
        return res
        pass

    def __getTaskNum(self):
        url = 'https://cdnsciencepub.com/action/doSearch?AllField={}'.format(self.keyWord)
        html = self.__getHtml(url)
        tree = etree.HTML(text=html)
        div = tree.xpath("//span[@class='result__count']']")[0].text
        self.task_nums = int(div.strip().replace(',', ''))
        lg.info("Search results: {} nums.".format(self.task_nums))
        pass

    def __getHtml(self, url: str) -> str:
        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=120)
        return response.text

    def __parseHtml(self, html: str) -> List[CanadianScienceResultItem]:
        """
        return [CanadianScienceResultItem]
        :param html:
        :return:
        """
        result = []
        dom = etree.HTML(html)
        title_xpath = "//div[@class='issue-item__title']"
        for title in dom.xpath(title_xpath):
            t = title.xpath('./a/@title')[0]
            doi = title.xpath('./a/@href')[0]
            result.append(CanadianScienceResultItem(title=t, doi=doi))
        return result

    def __genUrls(self) -> List[str]:
        urls = []
        for i in range(0, self.task_nums // 20):
            url = "https://cdnsciencepub.com/action/doSearch?AllField={}&pageSize=20&startPage={}".format(self.keyWord,
                                                                                                          str(i))
            urls.append(url)
        return urls

