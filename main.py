from doi.Wiley import WileyChannel
from doi.CanadianScience import CanadianScienceChannel
from settings import SearchKeys, SavePath
from doi.Doi import Doi
import os

channel_name = '_CanadianScience'
for searchKey in SearchKeys:
    doi = Doi()
    channel = CanadianScienceChannel(keyWord=searchKey)
    doi.searchArticle(channel=channel)
    fileName = searchKey + channel_name + '.csv'
    doi.saveDoiUuid(path=os.path.join(SavePath, fileName))
