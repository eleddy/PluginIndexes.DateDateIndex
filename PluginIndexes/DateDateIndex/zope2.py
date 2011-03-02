
def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    
    from PluginIndexes.DateDateIndex.DateDateIndex import DateDateIndex
    from PluginIndexes.DateDateIndex.DateDateIndex import manage_addDateDateIndex
    from PluginIndexes.DateDateIndex.DateDateIndex import manage_addDateDateIndexForm
    
    context.registerClass(DateDateIndex,
                          permission='Add Pluggable Index',
                          constructors=(manage_addDateDateIndexForm,
                                        manage_addDateDateIndex),
                          icon='www/index.gif',
                          visibility=None,
                         )
