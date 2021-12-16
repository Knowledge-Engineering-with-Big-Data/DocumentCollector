import unittest
from doi.Doi import Doi
from doi.Elsevier import ElsevierChannel


class TestDoi(unittest.TestCase):

    def test_doi(self):
        doi = Doi()
        doi.searchArticle(channel=ElsevierChannel(keyWord='oolitic'))
        doi.saveDoiUuid(path="oolitic_doi_uuid.csv")
    pass


if __name__ == '__main__':
    unittest.main()
