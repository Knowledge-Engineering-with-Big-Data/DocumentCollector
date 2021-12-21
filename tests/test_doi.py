import os.path
import unittest

from doi.Doi import Doi
from doi.Elsevier import ElsevierChannel
from doi.Wiley import WileyChannel
from doi.GeosicenceWorld import GeosicenceWorldChannel
from doi.CanadianScience import CanadianScienceChannel
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
        for searchKey in SearchKeys[0:1]:
            # TODO: why uuid didn't save into csv
            doi.searchArticle(channel=WileyChannel(keyWord=searchKey))
            fileName = searchKey + channel_name + '.csv'
            doi.saveDoiUuid(path=os.path.join(SavePath, fileName))

    def test_canadiansciencec(self):
        doi = Doi()
        channel_name = '_CanadianScienceChannel'
        for searchKey in SearchKeys:
            doi.searchArticle(channel=CanadianScienceChannel(keyWord=searchKey))
            fileName = searchKey + channel_name + '.csv'
            doi.saveDoiUuid(path=os.path.join(SavePath, fileName))
        pass

    def test_geosicenceworld(self):
        doi = Doi()
        channel_name = '_GeosicenceWorld'
        for searchKey in SearchKeys:
            doi.searchArticle(channel=GeosicenceWorldChannel(keyWord=searchKey))
            fileName = searchKey + channel_name + '.csv'
            doi.saveDoiUuid(path=os.path.join(SavePath, fileName))
        pass



if __name__ == '__main__':
    unittest.main()
