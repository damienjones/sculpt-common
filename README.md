sculpt-common
=============

Django is a great framework, but there are a few things that are missing or just cumbersome to use. This is a collection of small additions that make life easier. Many of the other sculpt-* projects I've written rely on some or all of this code.

Features
--------

* An Enumeration class
    * Designed to support Django's tuple-of-tuples used to enumerate choices for model fields.
    * Allows semantic code, like MyEnum.SOME_VALUE, instead of directly using the magic value.
    * Supports additional fields per enumerated value, especially a "display" field that is suitable for users when the programmatic label is not.
* A ParameterProxy class
    * Allows a class to designate a single-parameter function as callable from a Django template, where normally it would not be.
* Conversion edge case functions:
    * empty_if_none (converts None to '', leaves others unchanged)
    * parse_datetime (requires ISO format)
    * sculpt_slugify (convert / to - in slugs rather than stripping them)
* compare_strings - a function to sensibly compare version strings, e.g. 1.2a < 1.2q
* merge_dicts - overlay an arbitrary number of dicts and return the response.
* Easy method of importing all submodules within a module and catching exceptions (useful for batch processing).
* Verified HTTPS connector (validates server certificates instead of swallowing certificate errors; doing SSL/TLS without this leaves you open to man-in-the-middle attacks).
