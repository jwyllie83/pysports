## Overview

Library to manipulate data on sports-reference.com for custom analysis in
Python.

## General functionality:

 - Parses HTML for statistics tables and loads them into usable data structures

## Internal Details

The parsing methods aren't designed with maximum efficiency in mind, but rather
maximum usability.  This is largely because sports-reference.com doesn't let
you get large swaths of data at a time so efficiency isn't at a premium.

There are various [XML
Vulnerabilities](https://docs.python.org/2/library/xml.html#xml-vulnerabilities)
present in most XML parsers.  This code uses `BeautifulSoup` to do the legwork,
so keep that in mind if you're using untrusted sources of data.  The page
doesn't cite any known XML vulnerabilities.

## Installing / Using

`pysports` requires `BeautifulSoup4`.  Easy to get on basically any OS.  On
Ubuntu:

`sudo apt-get install python-bs4`

`pysports` requires a Python version equal to or above 2.6.

`pysports` is not Python3 compatible.

## Implementation Details

This should have been reasonably obvious to me at the time: I should have used
the soup tags to create tables, and then used OOO to parse out the fields.
Passing around the big soup value like that and picking / assembling pieces is
more brittle and confusing.  My excuse is that I haven't coded web parsing
stuff before (and never used `BeautifulSoup`) so I wasn't aware of the
decomposable nature of it.

Either way, if you look at the code and wonder why the heck someone designed it
like this instead of decomposing pieces (say, constructing tables and passing
those pieces around vs. the whole soup and re-parsing), that's why.  You get
what you pay for.

## Terms of Use

It's your responsibility to comply with any and all rules of
sports-reference.com.  Put another way, it's not my responsibility if you use
this tool as part of a system that breaks their rules.  Some links you might
find helpful to find out what the rules are:

- [Data Use](http://www.sports-reference.com/data_use.shtml)
- [Terms of Use](http://www.sports-reference.com/termsofuse.shtml)

You might want to consider the yearly ad-free fee if you have a large enough
need to necessitate processing like this.  It's not that much cash.

I purposefully don't include any functionality to spider the site in this, just
to parse the already-obtained text.  You have to find your own way to actually
get the tables to parse.

## License

`pysports` is implemented according to the BSD 3-Clause License.  You can find
a copy in the LICENSE file.
