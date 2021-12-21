SearchKeys = ['ooid', 'oolitic', 'oolite']
SaveFolder = 'results'

import os

SavePath = os.path.join(os.path.abspath(os.path.dirname(__file__)),SaveFolder)
if not os.path.exists(SavePath):
    os.mkdir(SavePath)
