from typing import List
import uuid
from collections import defaultdict
import csv


class ResultItem:
    def __init__(self, title: str, doi: str) -> None:
        self.title = title
        self.doi = doi
        pass


class Channel:
    def __init__(self) -> None:
        pass

    def getSearchResults(self, delay=15) -> List[ResultItem]:
        pass


class Doi:

    def __init__(self) -> None:
        self.doi = set()
        self.uuid = defaultdict(str)

    def searchArticle(self, channel: Channel) -> None:
        results = channel.getSearchResults()
        for item in results:
            self.doi.add(self.__foramtDoi(item.doi))
            self.__gen_uuid_of_doi(doi=item.doi)

    def __foramtDoi(self, doi: str) -> str:
        doi = doi.replace('https://doi.org/', '').replace('/doi/', '').replace('full/', '').replace('book/', '')
        return doi

    def __gen_uuid_of_doi(self, doi: str) -> None:
        self.uuid[doi] = str(uuid.uuid3(uuid.NAMESPACE_OID, doi))

    def saveDoiUuid(self, path: str):
        header = ['doi', 'uuid']
        rows = [[i, self.uuid[i]] for i in self.doi]
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
