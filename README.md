# DocumentCollector

A tool for information extraction from paper which get doi from website using keywords.


## Run Locally

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

3. Run

   ```bash
   python3 main.py
   ```

## Authors

- [@brillience](https://github.com/brillience)

