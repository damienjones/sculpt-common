# ParameterProxy
#
# Django's template language is deliberately hobbled
# to make it extremely simple, but one of its limitations
# is that it's not possible to invoke methods on an object
# unless they require no parameters or they are properties.
# This makes certain kinds of functions cumbersome and is
# why Django creates get_<field>_display methods. To work
# around this, we create a "parameter proxy" method which
# returns a new object, which Django will then pass the
# next token to as a field lookup, which we catch and give
# to the original requested method as a parameter.
#
# To use this, you must define your method first and then
# your proxy method:
#
# class Foo(object):
#     def bar(self, param):
#         ...
#     bar_proxy = property(parameter_proxy('bar', enumeration = MY_ENUM))
#
# This is because we want bar to exist as a named method
# on the object, and if we simply wrap bar in a decorator,
# the only way to access it will be through the proxy,
# which we don't want to do if we don't have to.
#
# You could also apply ParameterProxy to an existing
# function directly and place a reference to the proxy in
# a context passed into a template, to give a template
# access to a function. That would be unusual.
#
# If an enumeration is passed in as well, then the parameter
# to the proxy method will be translated to its value from
# the enumeration, rather than requiring the method to do
# that.
#
class ParameterProxy(object):

    # construction requires a reference to the proxied method
    # and whether it is an enumeration
    def __init__(self, proxy_method, enumeration = None):
        self.proxy_method = proxy_method
        self.enumeration = enumeration

    # any time we get a request for a particular attribute
    # on the object, call the method with the attribute
    # as the first parameter; if the parameter is meant
    # to be an enumeration, look up the enumeration first
    # and validate it
    def __getattr__(self, attr):
        if self.enumeration:
            attr = self.enumeration.get_value(attr)  # raises KeyError if it's invalid
        return self.proxy_method(attr)

# the property generator, required since we need
# access to self; this allows the proxy to be
# generated just once (for the class) but still
# invoked properly per object
def parameter_proxy(proxy_method_name, enumeration = None):
    
    def inner(self):
        cachename = proxy_method_name + '_proxy'
        if not hasattr(self, cachename):
            proxy_method = getattr(self, proxy_method_name)
            setattr(self, cachename, ParameterProxy(proxy_method, enumeration))
        return getattr(self, cachename)

    return inner

