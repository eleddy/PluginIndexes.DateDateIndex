import time
from datetime import date, datetime

from App.special_dtml import DTMLFile
from DateTime.DateTime import DateTime
from OFS.PropertyManager import PropertyManager
from zope.interface import implements

from Products.PluginIndexes.DateIndex.DateIndex import DateIndex, MAX32
from interfaces import IDateDateIndex
from DateTime.DateTime import DateError


class DateDateIndex(DateIndex):
    """
    Variation on the DateTime index. It strips all times so that queries 
    on just dates will not be affected by timezones.
    """
    implements(IDateDateIndex)

    meta_type = 'DateDateIndex'
    query_options = ('query', 'range')

    manage = manage_main = DTMLFile( 'dtml/manageDateIndex', globals() )
    manage_browse = DTMLFile('dtml/browseIndex', globals())

    manage_main._setName( 'manage_main' )
    manage_options = ( { 'label' : 'Settings'
                       , 'action' : 'manage_main'
                       },
                       {'label': 'Browse',
                        'action': 'manage_browse',
                       },
                     ) + PropertyManager.manage_options

    def _convert( self, value, default=None ):
        """
        Convert any dates into the appropriate date format. Strips times and timezones.
        This format is compatible with the other date indexes so that all the remaining 
        functions work as expected
        """
        if isinstance(value, DateTime):
            t_tup = value.parts()
        elif isinstance(value, (float, int)):
            t_tup = time.gmtime( value )
        elif isinstance(value, str) and value:  
            # prune times if they are there since datetime will convert timezones
            value = value.split(" ")[0] 
            # date time also has a back compat issue with dates with a "-" in them. 
            value = value.replace("-", "/")
            try:
                t_obj = DateTime( value )
            except DateError: # conversion fails for whatever reason
                return default
            t_tup = t_obj.parts()
        elif isinstance(value, date) or isinstance(value, datetime):
            t_tup = value.timetuple()
        else:
            return default

        yr = t_tup[0]
        mo = t_tup[1]
        dy = t_tup[2]
        
        t_val = ( ( ( ( yr * 12 + mo ) * 31 + dy ) * 24) * 60 )

        if t_val > MAX32:
            # t_val must be integer fitting in the 32bit range
            raise OverflowError(
                "%s is not within the range of indexable dates (index: %s)"
                % (value, self.id))

        return t_val


manage_addDateDateIndexForm = DTMLFile( 'dtml/addDateDateIndex', globals() )

def manage_addDateDateIndex( self, id, REQUEST=None, RESPONSE=None, URL3=None):
    """Add a DateDate index"""
    return self.manage_addIndex(id, 'DateDateIndex', extra=None, \
                    REQUEST=REQUEST, RESPONSE=RESPONSE, URL1=URL3)
