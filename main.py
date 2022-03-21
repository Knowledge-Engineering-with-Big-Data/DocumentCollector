from doi.GeosicenceWorld import GeosicenceWorldChannel
from doi.Elsevier import ElsevierChannel
from doi.CanadianScience import CanadianScienceChannel
from doi.Wiley import WileyChannel
from multiprocessing import Pool

from settings import SearchKeys, SavePath
from doi.Doi import Doi
import os


def GetDoi(searchKey):
    doi = Doi()

    channel_name = '_GeosicenceWorldChannel'
    channel = GeosicenceWorldChannel(keyWord=searchKey)
    doi.searchArticle(channel=channel)
    fileName = searchKey + channel_name + '.csv'
    doi.saveDoiUuid(path=os.path.join(SavePath, fileName))

    channel_name = '_ElsevierChannel'
    channel = ElsevierChannel(keyWord=searchKey)
    doi.searchArticle(channel=channel)
    fileName = searchKey + channel_name + '.csv'
    doi.saveDoiUuid(path=os.path.join(SavePath, fileName))

    channel_name = '_CanadianScienceChannel'
    channel = CanadianScienceChannel(keyWord=searchKey)
    doi.searchArticle(channel=channel)
    fileName = searchKey + channel_name + '.csv'
    doi.saveDoiUuid(path=os.path.join(SavePath, fileName))

    channel_name = '_WileyChannel'
    channel = WileyChannel(keyWord=searchKey)
    doi.searchArticle(channel=channel)
    fileName = searchKey + channel_name + '.csv'
    doi.saveDoiUuid(path=os.path.join(SavePath, fileName))

if __name__ =='__main__':
    pool = Pool(len(SearchKeys))
    pool.map(GetDoi,SearchKeys)
    pool.close()
    pool.join()