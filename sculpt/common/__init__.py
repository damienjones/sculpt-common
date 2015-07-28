from sculpt.common.enumeration import Enumeration   # more convenient to import from here than .enumeration
from sculpt.common.parameter_proxy import parameter_proxy   # and here too
import datetime
import os
import re
import string

# shared code

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


