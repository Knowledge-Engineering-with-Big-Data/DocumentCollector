from peewee import *
import sys
sys.path.append('..')
from settings import DBPath,SavePath


database = SqliteDatabase(DBPath)


class Doi(Model):
    unique_id = CharField(unique=True)
    doi = CharField()

    class Meta:
        database = database
