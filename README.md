## Overview

Library to manipulate data on sports-reference.com for custom analysis to pull
large(r) swaths of data.

## General functionality:

 - Parses HTML for statistics tables and loads them into usable data structures

## Internal Details

The parsing methods aren't designed with maximum efficiency in mind, but rather
maximum usability.  This is largely because sports-reference.com doesn't let
you get large swaths of data at a time so efficiency isn't at a premium.

There are various [XML
Vulnerabilities](https://docs.python.org/2/library/xml.html#xml-vulnerabilities)
present in most XML parsers.  This code uses `BeautifulSoup` to do the legwork,
so keep that in mind if you're using untrusted sources of data.

## Terms of Use

It's your responsibility to stay within the Terms of Use of
sports-reference.com (not mine).  Some links you might find helpful to find out
what the rules are:

[Data Use](http://www.sports-reference.com/data_use.shtml)
[Terms of Use](http://www.sports-reference.com/termsofuse.shtml)

You might want to consider the yearly ad-free fee if you have a large enough
need to necessitate processing like this.  It's not that much cash.  If you
need enough data to resort to this library, you probably are using their
services enough to warrant paying for it.
