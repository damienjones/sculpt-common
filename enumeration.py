from sculpt.common.parameter_proxy import parameter_proxy
import collections

# Enumeration
#
# Django's support for enumerated types is... quirky. As in,
# you define a list of (value, label) pairs and pass it to an
# integer/char field, and in the admin it restricts the set.
# It does NOT create an actual ENUM field type, nor does it
# create a foreign-key type, nor does it enforce the choices
# on direct assignment. And referencing the values by label
# in your code isn't possible.
#
# What we would LIKE is to be able to reference
# classname.ENUM_LABEL directly AND have that automatically
# used for the choices on the field. We'd really like it to
# be enforced, but we'll settle for not.
#
# Use this way:
#
# class MyModel(model.Model):
#
#     MY_ENUMS = Enumeration(
#             (0, 'FOO'),
#             (1, 'BAR'),
#         )
#     enum_field = models.IntegerField(choices = MY_ENUMS.choices)
#
# print MyModel.MY_ENUMS.FOO
# >>> 0
#
# NOTE: if your list of enumerated values is longer than 254,
# you won't be able to pass it directly as parameters because
# Python function parameters are actually tuples and tuples are
# capped at 254 entries. Instead, pass choices = [ <tuples> ]
#
# You can create additional fields with each enumeration,
# essentially turning it into a miniature record set that has
# its values defined by code, rather than a database. This
# will let you do useful things like associate helper classes
# or functions with specific enumerated values.
#
# To accommodate this, internally all enumeration values are
# actually labeled; the defaults for 2-tuples are "value" and
# "id". If you pass labels = <tuple> then you can provide
# any number of columns. You can access the data as
#
#     MY_ENUMS.data.FOO['<column_name>']
#
#**** and if you know the value of a particular column you can
#**** use that to look up the row:
#****
#****     MY_ENUMS.columns.<column_name1>.<column_value>['<column_name2>']
#
# You can generate a tuple of 2-tuples from any two columns:
#
#     MY_ENUMS.tuples('<column_name1>','<column_name2>')
#
# and in fact the choices field is populated exactly this way.
# Also available is the notion of "display" labels, which can
# be used to create drop-downs without sacrificing code
# readability. Define a "label" column, and you can use this:
#
#     MY_ENUMS.labels
#
# which is a tuple of value,label tuples instead of the 
# value,id tuples returned by MY_ENUMS.choices
#
# If you pass a list of column labels, you can use the value
# and id columns at any position, but their presence is
# required.
#
# The Enumeration class uses tuples because this stuff is
# supposed to be static. If you find yourself wanting to muck
# with the internal representation of an enumeration to modify
# its values at run-time, don't. Call it something else.
#
class Enumeration(object):

    _columns = None
    _columns_idx = None
    _data = None
    _data_dicts = None
    _idxs = None

    _choices = None
    _labels = None
    
    def __init__(self, *args, **kwargs):
        # pluck data from parameters
        self._columns = kwargs.get('labels', ( 'value', 'id' ))
        self._data = kwargs.get('choices', args)
        
        # create column-label to column-index lookup
        self._columns_idx = dict([ (self._columns[i],i) for i in range(len(self._columns)) ])

        # create indices for each column heading; any entries
        # which do not hold values in that column are ignored
        # (we also ignore entries that are not hashable)
        self._idxs = {}
        for i in range(len(self._columns)):
            column = self._columns[i]
            idx = {}
            self._idxs[column] = idx

            for j in range(len(self._data)):
                row = self._data[j]
                if i < len(row) and isinstance(row[i], collections.Hashable):
                    idx[row[i]] = j

        # go ahead and prep the data dicts for each row, so
        # that we don't constantly create new throw-away dicts
        # for this data; any fields missing from the list
        # (because the tuple is too short) are filled in as
        # None
        self._data_dicts = []
        for row in self._data:
            data_dict = {}
            self._data_dicts.append(data_dict)
            
            for i in range(len(self._columns)):
                column = self._columns[i]
                if i < len(row):
                    data_dict[column] = row[i]
                else:
                    data_dict[column] = None

        # fun bit: we want .data to be a parameter proxy to
        # the get_data() method, but we need a reference to
        # ourselves to pass in as the enumeration, so we have
        # to do this at creation time
        #self.data = parameter_proxy('get_data', enumeration = self)

    # generate a tuple of 2-tuples given a pair of column names
    def tuples(self, column1, column2):
        return tuple( (d['value'],d['id']) for d in self._data_dicts )

    #
    # cached access to common tuples-of-tuples extractions
    #

    @property
    def choices(self):
        if self._choices == None:
            # choices must be a list of 2-tuples to keep South happy
            self._choices = self.tuples('value', 'id')
        return self._choices
            
    @property
    def labels(self):
        if self._labels == None:
            self._labels = self.tuples('value', 'label')
        return self._labels
            
    # given a particular column name and value, return the row
    #
    # NOTE: this is more efficient than using the .data
    # property, and is the preferred implementation for code
    # rather than templates
    #
    def get_data(self, column, value):
        # if column is not in self._idxs, KeyError raised
        if value not in self._idxs[column]:
            # pretend we're a real attribute, and throw a similar exception,
            # instead of KeyError from a dict lookup
            raise AttributeError()
        row_number = self._idxs[column][value]
        return self._data_dicts[row_number]

    # given a particular ID, return the row
    # (a thin wrapper around get_data())
    #
    # NOTE: this is called _by_id because the
    # "value" that is passed is actually
    # checked to see if it's an ID value first
    #
    def get_data_by_id(self, value):
        return self.get_data('value', self.get_value(value))
        
    # look up an attribute, if it is not found
    # elsewhere (we look up the name in our set
    # of enumerations)
    def __getattr__(self, attr):
        return self.get_data('id', attr)['value']

    # and a parameter proxy to make this super-easy
    # for templates; since we're creating the proxy
    # at class definition time, we don't have an
    # enumeration for parameter_proxy to work with,
    # so we handle that ourselves in the wrapper
    data = property(parameter_proxy('get_data_by_id'))

    # look up an attribute, but get the whole row,
    # not just the value column
    #
    # NOTE: this is a function generator

    # columns
    #
    # Django automatically creates a get_<field>_display
    # function for each IntegerField using enumerated
    # choices. The problem is that it uses element 1 from
    # the tuple, which is the programmatic label (shame on
    # the Django dev team for not using better enumerations).
    # We want to return the nicer label at element 2, but
    # also make it possible to access the rest of the
    # enumeration's data in case it has been provided.
    #
    # To accommodate this, we create a wrapper that makes
    # a property that returns the tuple from the enumerated
    # type. It requires the field name.
    #
    # NOTE: this is a function generator
    #
    def columns(self, column):

        # this is the one-off function we need
        def _inner(inner_self):
            return self.get_tuple(getattr(inner_self, field_name))

        # return that function
        return _inner

    # sometimes (e.g. JSON parsing) we want to accept either
    # a numerical value directly or its label; this method
    # accepts either and always returns the value
    #
    # NOTE: does NOT validate the data; numbers not part
    # of the enumeration will not be rejected and names
    # not part of the enumeration will raise KeyError
    #
    def get_value(self, value):
        if isinstance(value, basestring):
            # a string; assume it's an ID, convert to value
            return self.get_data('id', value)['value']
        else:
            # already a value, return as-is
            return value

    # methods to make the class iterable
    def __len__(self):
        return len(self._data)
        
    def __iter__(self):
        return self._data.__iter__()
        
    def __getitem__(self, key):
        return self._data[key]
        
    def __setitem__(self, key, value):
        raise TypeError("'Enumeration' object does not support item assignment")
        
    def __delitem__(self, key):
        raise TypeError("'Enumeration' object does not support item assignment")

    # without this, 'in' tests by iterating, which isn't useful;
    # we want to test if an id is in the enumeration
    def __contains__(self, key):
        return key in self._idxs['id']

