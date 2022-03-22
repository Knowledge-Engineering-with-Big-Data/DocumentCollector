# DocumentCollector

A tool for information extraction from paper which get doi from website using keywords.


## Run Locally

0. Get project.

   ```bash
   git clone https://github.com/brillience/DocumentCollector.git
   cd DocumentCollector
   pip install -r requirements.txt
   ```

1. Add search key words in settings.py.
> Elsevier does not support wildcard searches, eg: `dolomit*`, so you should go to the website first to determine your search terms!
```python
   SearchKeys = ['xxx', 'xxx', 'xxx']
   ```

2. create main.py

   ```python
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
   ```

3. Run

   ```bash
   # get doi
   python3 main.py
   # update to db (optional)
   cd scripts
   python3 update_to_db.py
   
   ```

## Authors

- [@brillience](https://github.com/brillience)

