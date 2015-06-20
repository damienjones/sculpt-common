sculpt-common
=============

Django is a great framework, but there are a few things that are missing or just cumbersome to use. This is a collection of small additions that make life easier. Many of the other sculpt.* Python projects I've written rely on some or all of this code.

Special Note
------------

This is not a complete project. Although now packaged as a Python project, there are no unit tests, and the only documentation is within the code itself. I don't really expect anyone else to use this code... yet. All of those things will be addressed at some point.

That said, the code _is_ being used. This started with work I did while at Caxiam (and I obtained a comprehensive license to continue with the code) so here and there are references to Caxiam that I am slowly replacing. I've done quite a bit of refactoring since then and expect to do more.

License
-------

At the moment this is LGPLv2; see LICENSE.txt for details.

Features
--------

* An Enumeration class
    * Designed to support Django's tuple-of-tuples used to enumerate choices for model fields.
    * Allows semantic code, like MyEnum.SOME_VALUE, instead of directly using the magic value.
    * Supports additional fields per enumerated value, especially a "label" field that is suitable for users when the programmatic label is not. (There are lots of use cases for this which I need to document.)
* A ParameterProxy class
    * Allows a class to designate a single-parameter function as callable from a Django template, where normally it would not be.
* Conversion edge case functions:
    * empty_if_none (converts None to '', leaves others unchanged)
    * parse_datetime (requires ISO format)
    * sculpt_slugify (convert / to - in slugs rather than stripping them)
* compare_strings - a function to sensibly compare version strings, e.g. 1.2a < 1.2q
* merge_dicts - overlay an arbitrary number of dicts and return the response.
* Easy method of importing all submodules within a module and catching exceptions (useful for batch processing).
* Verified HTTPS connector (validates server certificates instead of swallowing certificate errors; doing SSL/TLS without this leaves you open to man-in-the-middle attacks). **TODO**
