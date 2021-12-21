# DocumentCollector
A tool for information extraction from paper.
## What this tool do?
1. Get DOI from Wiley, Elsevier, GeoScienceWorld, CanadianScience.
2. After de-duplicating all DOI， get their paper document from Internet.

## How to use?
0. Get project.
   ```bash
   git clone https://github.com/brillience/DocumentCollector.git
    ```
1. Add search key words in settings.py.
    ```python
    SearchKeys = ['xxx', 'xxx', 'xxx']
    ```
2. create main.py
    ```python
    from doi.Wiley import WileyChannel
    from settings import SearchKeys, SavePath
    
    doi = Doi()
    channel_name = '_wiley'
    for searchKey in SearchKeys:
        doi.searchArticle(channel=WileyChannel(keyWord=searchKey))
        fileName = searchKey + channel_name + '.csv'
        doi.saveDoiUuid(path=os.path.join(SavePath, fileName))
    
    ```