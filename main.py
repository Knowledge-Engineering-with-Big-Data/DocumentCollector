from doi.GeosicenceWorld import GeosicenceWorldChannel
from doi.Elsevier import ElsevierChannel
from doi.CanadianScience import CanadianScienceChannel
from doi.Wiley import WileyChannel
from multiprocessing import Pool

from settings import SearchKeys, SavePath
from doi.Doi import Doi
import os


def GetDoi(searchKey):

    channel_name = '_GeosicenceWorldChannel'
    fileName = searchKey + channel_name + '.csv'
    channel = GeosicenceWorldChannel(keyWord=searchKey)
    doi = Doi(os.path.join(SavePath, fileName))
    doi.searchArticle(channel=channel)


    channel_name = '_ElsevierChannel'
    fileName = searchKey + channel_name + '.csv'
    channel = ElsevierChannel(keyWord=searchKey)
    doi = Doi(os.path.join(SavePath, fileName))
    doi.searchArticle(channel=channel)


    channel_name = '_CanadianScienceChannel'
    fileName = searchKey + channel_name + '.csv'
    channel = CanadianScienceChannel(keyWord=searchKey)
    doi = Doi(os.path.join(SavePath, fileName))
    doi.searchArticle(channel=channel)

    # channel_name = '_WileyChannel'
    # fileName = searchKey + channel_name + '.csv'
    # channel = WileyChannel(keyWord=searchKey)
    # doi = Doi(os.path.join(SavePath, fileName))
    # doi.searchArticle(channel=channel)

if __name__ =='__main__':
    pool = Pool(len(SearchKeys))
    pool.map(GetDoi,SearchKeys)
    pool.close()
    pool.join()