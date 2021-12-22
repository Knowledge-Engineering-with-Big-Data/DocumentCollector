from models import Doi,SavePath
import os
import csv


print('[INFO] Start update to db!')
if not Doi.table_exists():
    Doi.create_table()

csv_pathes = [os.path.join(SavePath,i) for i in os.listdir(SavePath)]

for path in csv_pathes:
    with open(path,encoding='utf-8') as f:
        reader = csv.reader(f)
        for item in reader:
            if item[0]!=None and len(item[0])>2:
                po, created = Doi.get_or_create(unique_id=item[1],doi=item[0])
                if created is False:
                    po.save()
print('[INFO] Finished update to db!')