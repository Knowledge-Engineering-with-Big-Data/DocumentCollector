from doi.GeosicenceWorld import GeosicenceWorldChannel
from settings import SearchKeys, SavePath
from doi.Doi import Doi
import os

channel_name = '_GeosicenceWorld'
for searchKey in SearchKeys:
    doi = Doi()
    channel = GeosicenceWorldChannel(keyWord=searchKey)
    doi.searchArticle(channel=channel)
    fileName = searchKey + channel_name + '.csv'
    doi.saveDoiUuid(path=os.path.join(SavePath, fileName))
