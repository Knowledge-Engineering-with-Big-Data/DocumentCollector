from typing import List
import hashlib
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

    def __init__(self, path: str) -> None:
        self.path = path
        self.firstSave = True

    def searchArticle(self, channel: Channel) -> None:
        for item in channel.getSearchResults():
            doi = self.__foramtDoi(item.doi)
            uuid = self.__gen_uuid_of_doi(doi)
            self.__saveDoiUuid(doi,uuid)

    def __foramtDoi(self, doi: str) -> str:
        doi = doi.replace('https://doi.org/', '').replace('/doi/', '').replace('full/', '').replace('book/', '')
        return doi

    def __gen_uuid_of_doi(self, doi: str) -> str:
        # self.uuid[doi] = str(uuid.uuid3(uuid.NAMESPACE_OID, doi))
        md5 = hashlib.md5()
        md5.update(doi.encode('utf-8'))
        res = md5.hexdigest()
        return res

    def __saveDoiUuid(self, doi: str, uuid: str):
        header = ['doi', 'uuid']
        rows = []
        if doi != None and len(doi) > 2:
            rows.append([doi, uuid])
        # rows = [[i, self.uuid[i]] for i in self.doi]
        with open(self.path, 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            if self.firstSave == True:
                writer.writerow(header)
                self.firstSave = False
            writer.writerows(rows)
