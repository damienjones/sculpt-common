from sculpt.common.enumeration import Enumeration   # more convenient to import from here than .enumeration
from sculpt.common.parameter_proxy import parameter_proxy   # and here too
import datetime
import os
import re
import string

# shared code

# compare version strings
#
# A version string is compared character-by-character,
# except that whenever digits are encountered, all consecutive
# digits are converted to an integer and compared. Therefore:
#   1.1 < 1.2
#   1.2 < 1.10
#   1.2a < 1.2q
#   1.1.15 < 1.2.9
#   1.103b < 1.1011c    !! 103 < 1011
#   1.1.b < 1.01.c      !! b < c
#   1.01 < 1.1          !! lexical compare if no difference
#
# NOTE: this does not deal with Unicode digits other than 0-9.
# Don't try to do cute things with version numbers.
#
digit_extractor = re.compile(r'[0-9]+')

def compare_versions(a, b):
    # null cases
    if a == None and b == None:
        return 0
    elif a == None:
        return -1
    elif b == None:
        return 1
        
    # non-null cases
    pos_a = 0
    pos_b = 0
    while pos_a < len(a) and pos_b < len(b):
        if a[pos_a] in string.digits and b[pos_b] in string.digits:
            # number-to-number comparison
            pa = digit_extractor.match(a, pos_a).group()
            pb = digit_extractor.match(b, pos_b).group()
            na = int(pa, 10)
            nb = int(pb, 10)
            r = cmp(na, nb)
            if r != 0:
                return r
                
            pos_a += len(pa)
            pos_b += len(pb)
            
        else:
            # simple character comparison
            r = cmp(a[pos_a], b[pos_b])
            if r != 0:
                return r
            pos_a += 1
            pos_b += 1

    # no differences using above algorithm; use regular
    # string comparison
    return cmp(a,b)

# useful conversion edge case handlers

# empty_if_none
# returns the original string, or '' if it's None
# (this is useful shorthand when s is a complicated expression)
def empty_if_none(s):
    return s if s != None else ''

# given a particular string, attempt to parse it as an
# ISO-format datetime and return that; return None if
# not valid
def parse_datetime(v):
    try:
        return datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return None

# for a particular module, find all the sub-modules and import them
# (first-level crawl only)
#
# pass in the parent module name (typically globals()['__name__']) and
# the file path list (typically globals()['__path__'])
#
# NOTE: __path__ will NOT be defined if you recursively import, so
# don't do that
#
# This is primarily useful for the cron modules, which need to invoke
# the sub-modules one by one, but do so in a predictable (alphabetical)
# order, with exception-catching for each one. A boolean is returned
# indicating whether any of the sub-modules failed to import properly.
# 
def import_all_submodules(mod, path, catch_errors = False):
    # imported here so module can be used even if this isn't available
    # (e.g. Jython)
    import importlib
    
    had_error = False
    path = path[0]
    files = os.listdir(path)
    files.sort()                                            # sort them to ensure a consistent order
    for f in files:
        if f != '__init__.py' and f.endswith('.py'):        # a Python script, not our __init__ module
            try:
                importlib.import_module(mod + '.' + f[:-3]) # go ahead and import it
            except Exception, e:
                had_error = True
                if not catch_errors:
                    # we actually didn't want to trap these, re-raise it
                    raise
                    
                # otherwise we need to record this exception; we assume
                # we're running in an environment where STDOUT is logged
                # NOTE: we do this whether we're in DEBUG mode or not

                # sys.exc_info() returns a tuple (type, exception object, stack trace)
                # traceback.format_exception() formats the result in plain text, as a list of strings
                import sys
                import traceback
                backtrace_text = ''.join(traceback.format_exception(*sys.exc_info()))
                print '!!!! exception detected while importing submodules'
                print backtrace_text
                
                # and now we swallow the exception and move on to the
                # next one

    return had_error

# Python doesn't have an easy way to recursively merge
# dicts. So we recursively crawl the damn things and do
# it ourselves.
#
# http://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge/24837438#24837438
#
# NOTE: modifies dict1 in place as well as returns it.
# If you need to preserve it, use copy.deepcopy() on it
# first.
#
def merge_dicts(dict1, dict2):
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return dict2
    for k in dict2:
        if k in dict1:
            dict1[k] = merge_dicts(dict1[k], dict2[k])
        else:
            dict1[k] = dict2[k]
    return dict1

# extract from JSON
#
# Often when working with JSON data fetched from outside
# sources, we need to quickly look for a deeply-nested
# element and extract it if it's available or return None
# if it's missing. We need to check at each level of the
# nested structure if the next step is available.
#
def extract(obj, *args):
    for a in args:
        if isinstance(obj, list):
            # should be a numeric index
            if a >= 0 and a < len(obj):
                obj = obj[a]
            else:
                return None

        elif isinstance(obj, dict):
            # could be any kind of key
            if a in obj:
                obj = obj[a]
            else:
                return None

        else:
            # some other type we can't look into;
            # fail (but quietly)
            # THIS IS A DESIGN CHOICE. We could raise
            # an exception instead.
            return None

    return obj

# slugify extension
#
# Django's slugify() is nice and robust, except that it
# demands unicode input on Python 2 and it drops / instead
# of replacing it with -
#
# Since this is a wrapper around Django's slugify, you need
# Django installed to use this. But you can import the rest
# of the module without Django.
#
# NOTE: we call it sculpt_slugify instead of just slugify
# so that wherever it appears in code, it's crystal clear
# that it's NOT Django's slugify; this helps prevent subtle
# bugs due to bad import directives.
#
def sculpt_slugify(value):
    from django.utils.text import slugify
    return slugify(unicode(value.replace('/','-')))


