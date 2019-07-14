# bencoding
# http://www.bittorrent.org/beps/bep_0003.html

"""
Strings are length-prefixed base ten followed by a colon and the string.
For example 4:spam corresponds to 'spam'.

>>> encode(b'spam')
b'4:spam'

Integers are represented by an 'i' followed by the number in base 10 followed by an 'e'.
For example i3e corresponds to 3 and i-3e corresponds to -3.
Integers have no size limitation. i-0e is invalid.
All encodings with a leading zero, such as i03e, are invalid,
other than i0e, which of course corresponds to 0.

>>> decode(b'i3e')
3
>>> decode(b'i-3e')
-3
>>> decode(b'i0e')
0
>>> decode(b'i03e')
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 0: '03'


Lists are encoded as an 'l' followed by their elements (also bencoded) followed by an 'e'.
For example l4:spam4:eggse corresponds to ['spam', 'eggs'].

>>> decode(b'l4:spam4:eggse')
[b'spam', b'eggs']

Dictionaries are encoded as a 'd' followed by a list of alternating keys
and their corresponding values followed by an 'e'.
For example, d3:cow3:moo4:spam4:eggse corresponds to {'cow': 'moo', 'spam': 'eggs'}
Keys must be strings and appear in sorted order (sorted as raw strings, not alphanumerics).

>>> decode(b'd3:cow3:moo4:spam4:eggse')
OrderedDict([(b'cow', b'moo'), (b'spam', b'eggs')])

"""

import re
import string
import itertools as it
from collections import OrderedDict

def encode(val):
    if isinstance(val, int):
        return b"i" + str(val).encode() + b"e"
    elif isinstance(val, bytes):
        return str(len(val)).encode() + b":" + val
    elif isinstance(val, str):
        return encode(val.encode("ascii"))
    elif isinstance(val, list):
        return b"l" + b"".join(map(encode, val)) + b"e"
    elif isinstance(val, dict):
        if all(isinstance(i, bytes) for i in val.keys()):
            items = list(val.items())
            items.sort()
            return b"d" + b"".join(map(encode, it.chain(*items))) + b"e"
        else:
            raise ValueError("dict keys should be bytes")
    raise ValueError("Allowed types: int, bytes, list, dict; not %s", type(val))


def decode(val):

    if val.startswith(b"i"):
        match = re.match(b"i(-?\\d+)e", val)
        list_val = match.group(1).decode("utf-8")
        col = [str(x) for x in list_val]
        try:
            if col[0] == "0" and len(col) != 1:
                print('''Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 0: \'{}\''''.format(list_val))
            else:
                return int(match.group(1))
        except ValueError as error:
            print(error)
    elif val.startswith(b"l") or val.startswith(b"d"):
        l = []
        rest = val[1:]
        while not rest.startswith(b"e"):
            elem, rest = decode(rest)
            l.append(elem)
        rest = rest[1:]
        if val.startswith(b"l"):
            return l
        else:
            a = {i: j for i, j in zip(l[::2], l[1::2])}
            return OrderedDict(a)

    elif any(val.startswith(i.encode()) for i in string.digits):
        m = re.match(b"(\\d+):", val)
        length = int(m.group(1))
        rest_i = m.span()[1]
        start = rest_i
        end = rest_i + length
        return val[start:end], val[end:]
    else:
        raise ValueError("Malformed input.")

print(decode(b'i03e'))
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
