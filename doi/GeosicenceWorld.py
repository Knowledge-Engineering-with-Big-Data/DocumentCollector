import re
import time
from typing import List
from lxml import etree
import requests
from log import lg
from doi.Doi import ResultItem, Channel


class GeosicenceWorldResultItem(ResultItem):
    def __init__(self, title: str, doi: str, journal: str, publisher: str):
        super().__init__(title=title, doi=doi)
        self.journal = journal
        self.publisher = publisher
        pass


class GeosicenceWorldChannel(Channel):
    """
    a class of GeosicenceWorld crawler
    """

    def __init__(self, keyWord: str) -> None:
        self.keyWord = keyWord
        self.task_nums = 0
        self.__getTaskNum()
        pass

    def getSearchResults(self, delay=15) -> List[GeosicenceWorldResultItem]:
        """
        return search result
        :param delay: delay 15s when get page. Defaults to 15.
        :return:List[GeosicenceWorldResultItem]
        """
        res = 0
        for url in self.__genUrls():
            r = self.__parseHtml(self.__getHtml(url))
            for i in r:
                yield i
            res = res + len(r)
            lg.info("There are {} records left.".format(self.task_nums - res))
            time.sleep(delay)
        pass

    def __getTaskNum(self):
        url = 'https://pubs.geoscienceworld.org/journals/search-results?q={}'.format(self.keyWord)
        html = self.__getHtml(url=url)
        tree = etree.HTML(text=html)
        div = tree.xpath("//div[@class='sr-statistics']")[0].text
        self.task_nums = int(re.findall(pattern='OF(.*?)RESULTS FOR',string=div)[0].strip().replace(',', ''))
        lg.info("Search results: {} nums.".format(self.task_nums))

    def __getHtml(self, url: str) -> str:
        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=120)
        return response.text

    def __genUrls(self) -> List[str]:
        urls = []
        for i in range(1, self.task_nums // 20):
            url = "https://pubs.geoscienceworld.org/journals/search-results?q={}&fl_SiteID=9&page={}".format(
                self.keyWord,
                str(i))
            urls.append(url)
        return urls

    def __parseHtml(self, html: str) -> List[GeosicenceWorldResultItem]:
        """
        :param html:
        :return:
        """
        journal_pattern = '<strong>Journal:</strong> <a href="(.*?)">(.*?)</a>'
        publisher_pattern = '<strong>Publisher:</strong> <a href="(.*?)">(.*?)</a>'
        doi_pattern = '<div class="sri-doi">DOI: <a href="(.*?)">(.*?)</a></div>'
        title_pattern = '<a class="js-result-link" href="(.*?)">(.*?)</a>'

        res = []
        for txt in html.split('<div class="sr-list al-article-box al-normal clearfix">')[1:]:
            title = ''
            try:
                title = re.findall(title_pattern, txt)[0][1].replace("<b>", "").replace("</b>", "")
            except Exception as e:
                lg.info('no title')
            journal = ''
            try:
                journal = re.findall(journal_pattern, txt)[0][1]
            except Exception as e:
                lg.info('no journal')
            publisher = ''
            try:
                publisher = re.findall(publisher_pattern, txt)[0][1]
            except Exception as e:
                lg.info('no publisher')
            doi = ''
            try:
                doi = re.findall(doi_pattern, txt)[0][0]
            except Exception as e:
                lg.info("no doi")
                pass
            res.append(GeosicenceWorldResultItem(title=title, doi=doi, journal=journal, publisher=publisher))
        return res
