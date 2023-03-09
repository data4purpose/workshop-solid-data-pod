# -*- coding: utf-8 -*-

import requests

###########################################################
#
# This script is a Solid-Data Pod-Client.
#
#   An personal preferences profile is used to illustrate
#   public data sharing, using a personal datapod.
#
#   References:
#   -----------
#   * https://kushaldas.in/posts/using-python-to-access-a-solid-pod.html
#   * https://github.com/twonote/solid-file-python
#
###########################################################
# https://rdflib.readthedocs.io/en/stable/index.html
#
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS

from rdflib import Graph

url = "http://www.w3.org/People/Berners-Lee/card"
f = requests.get(url)
print("---------")
print(f.text)
print("---------")
print()
g1 = Graph()
g1.parse(url, format="turtle")
for s, p, o in g1:
    print(s, p, o)


fileName = "data/exampleprofile.ttl"
with open(fileName, 'r') as file:
    data = file.read().rstrip()
g2 = Graph()
g2.parse(fileName, format="turtle")
for s, p, o in g2:
    print(s, p, o)
