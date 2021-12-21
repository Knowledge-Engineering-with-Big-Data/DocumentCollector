# DocumentCollector

A tool for information extraction from paper which get doi from website using keywords.


## Run Locally

0. Get project.

   ```bash
   git clone https://github.com/brillience/DocumentCollector.git
   cd DocumentCollector
   conda install --yes --file requirements.txt
   ```

1. Add search key words in settings.py.

   ```python
   SearchKeys = ['xxx', 'xxx', 'xxx']
   ```

2. create main.py

   ```python
   from doi.CanadianScience import CanadianScienceChannel
   from settings import SearchKeys, SavePath
   from doi.Doi import Doi
   import os
   
   doi = Doi()
   channel_name = '_CanadianScience'
   for searchKey in SearchKeys:
       channel = CanadianScienceChannel(keyWord=searchKey)
       doi.searchArticle(channel=channel)
       fileName = searchKey + channel_name + '.csv'
       doi.saveDoiUuid(path=os.path.join(SavePath, fileName))
   ```

3. Run

   ```bash
   python3 main.py
   ```

## Authors

- [@brillience](https://github.com/brillience)

