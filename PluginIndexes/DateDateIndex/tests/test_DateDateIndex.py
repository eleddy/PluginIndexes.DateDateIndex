import unittest


class Dummy:

    def __init__(self, name, date):
        self._name  = name
        self._date = date

    def name(self):
        return self._name

    def date(self):
        return self._date

    def __str__(self):
        return "<Dummy %s, date %s>" % (self._name, str(self._date))

class DateDateIndexTests(unittest.TestCase):

    def _getTargetClass(self):
        from PluginIndexes.DateDateIndex.DateDateIndex import DateDateIndex
        return DateDateIndex

    def _makeOne(self, id='date'):
        return self._getTargetClass()(id)

    def _getValues(self):
        from DateTime import DateTime
        from datetime import date
        from datetime import datetime
        return [
            (0, Dummy('a', None)),                            # None
            (1, Dummy('b', DateTime(0))),                     # 0
            (2, Dummy('c', DateTime('2002-05-08 15:16:17'))), # 5/8/2002
            (3, Dummy('d', DateTime('2032-05-08 15:16:17'))), # 5/8/2032
            (4, Dummy('e', '2062-05-08 15:16:17')),           # 5/8/2062
            (5, Dummy('f', DateTime('2002/05/08 23:59:59'))), # 5/8/2002
            (6, Dummy('g', date(2034,2,5))),                  # 2/5/2034
            (7, Dummy('h', datetime(2034,2,5,15,20,5))),      # 2/5/2034
        ]

    def _populateIndex(self, index):
        for k, v in self._getValues():
            index.index_object(k, v)

    def _checkApply(self, index, req, expectedValues):
        result, used = index._apply_index(req)
        if hasattr(result, 'keys'):
            result = result.keys()
        self.assertEqual(used, ('date',))
        self.assertEqual(len(result), len(expectedValues),
            '%s | %s' % (result, expectedValues))
        for k, v in expectedValues:
            self.assertTrue(k in result)

    def test_retrieval( self ):
        from DateTime import DateTime
        index = self._makeOne()
        self._populateIndex(index)
        values = self._getValues()

        self.assertEqual(len(index), 5) # two duplicates, one empty
        self.assertEqual(len(index.referencedObjects()), len(values) - 1)

        self.assertEqual(len(index.uniqueValues('date')), 5)
        self.assertTrue(index._apply_index({'bar': 123}) is None)

        self._checkApply(index,
                         {'date': DateTime(0)}, values[1:2])
        self._checkApply(index,
                         {'date': {'query': DateTime('2032-05-08'),
                                   'range': 'min'}},
                         values[3:5] + values[6:8])
        
        self._checkApply(index,
                         {'date': {'query': DateTime('2032-05-08 15:16:17'),
                                   'range': 'min'}},
                         values[3:5] + values[6:8])
                         
        self._checkApply(index,
                         {'date': {'query': DateTime('2032-05-08 15:16:17'),
                                   'range': 'max'}},
                         values[1:4] + values[5:6])
        self._checkApply(index,
                         {'date': {'query':(DateTime('2002-05-08 15:16:17'),
                                            DateTime('2062-05-08 15:16:17')),
                                   'range': 'min:max'}},
                         values[2:] )
        self._checkApply(index,
                         {'date': {'query':('2002-05-08 15:16:17',
                                            '2062-05-08 15:16:17'),
                                   'range': 'min:max'}},
                         values[2:] )
        self._checkApply(index,
                         {'date': {'query':('2002-05-08',
                                            '2002/05/08'),
                                   'range': 'min:max'}},
                         values[2:3] + values[5:6])
        self._checkApply(index,
                         {'date': {'query':('2002-05-08',
                                            '2032-05-08'),
                                   'range': 'min:max'}},
                         values[2:4] + values[5:6])



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest( unittest.makeSuite( DateDateIndexTests ) )
    return suite
