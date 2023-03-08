# -*- coding: utf-8 -*-

###########################################################
#
# This script is a Solid-Datapod-Client.
#
#   An personal preferences profile is used to illustrate
#   public data sharing, using the personal datapod.
#
#   References:
#   -----------
#   * https://kushaldas.in/posts/using-python-to-access-a-solid-pod.html
#   * https://github.com/twonote/solid-file-python
#
###########################################################

#
# Provide new facts and add those to the profile ....
#

from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS

from rdflib import Graph

import requests

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

#https://rdflib.readthedocs.io/en/stable/index.html

fileName = "data/exampleprofile.ttl"
with open(fileName, 'r') as file:
    data = file.read().rstrip()
g2 = Graph()
g2.parse(fileName, format="turtle")
for s, p, o in g2:
    print(s, p, o)

#
# Store the changed profile data in the datapod ....
#