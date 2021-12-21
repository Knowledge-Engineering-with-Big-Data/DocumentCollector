import os.path
import unittest

from doi.Doi import Doi
from doi.Elsevier import ElsevierChannel
from doi.Wiley import WileyChannel
from settings import SearchKeys, SavePath


class TestDoi(unittest.TestCase):

    def test_elsevier(self):
        doi = Doi()
        channel_name = '_Elsevier'
        for searchKey in SearchKeys:
            doi.searchArticle(channel=ElsevierChannel(keyWord=searchKey))
            fileName = searchKey + channel_name + '.csv'
            doi.saveDoiUuid(path=os.path.join(SavePath, fileName))
        pass

    def test_wiley(self):
        doi = Doi()
        channel_name = '_wiley'
        for searchKey in SearchKeys:
            doi.searchArticle(channel=WileyChannel(keyWord=searchKey))
            fileName = searchKey + channel_name + '.csv'
            doi.saveDoiUuid(path=os.path.join(SavePath, fileName))



if __name__ == '__main__':
    unittest.main()
