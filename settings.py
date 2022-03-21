SearchKeys = ['limestone','dolomit*']
SaveFolder = 'results'
dbName = 'db.sqlite'

import os

SavePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), SaveFolder)
DBPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), dbName)

if not os.path.exists(SavePath):
    os.mkdir(SavePath)
