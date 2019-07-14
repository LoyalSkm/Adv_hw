import homework04

f = open("[rutor.is]the_messenger.torrent", "rb")
d = homework04.decode(f.read())
del d[b"info"][b"pieces"]
from pprint import pprint
pprint(d)