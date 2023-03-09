# -*- coding: utf-8 -*-

from dotenv import load_dotenv

load_dotenv()

PASSWORD = "12345PodTest#"

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
# 1. We configer the client credentials to a local data pod
#
#USERNAME = "kamir1604"
#PASSWORD = ""
#
#IDP = 'https://localhost:8443'
#POD_ENDPOINT = "https://kamir1604.localhost:8443/profile"

#
# 2. Alternatively, we configure the client credentials to a public data pod,
#    hosted by the solidcommunity
#
USERNAME = "kamir"

IDP = 'https://solidcommunity.net'
POD_ENDPOINT = "https://kamir.solidcommunity.net"

#
# For self hosted data pods with self signed certificates we have to deactivate certificate validation
#
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
context = ssl.create_default_context()

#
# A custom Auth-Component allows overwrting of httpx properties, such as certificate validation
#
import httpx

class Auth2:

    def __init__(self):
        self.client = httpx.Client(verify=False)

    @property
    def is_login(self) -> bool:
        return self.client.cookies.get('nssidp.sid') is not None

    def login(self, idp, username, password):
        # NSS only
        if idp[-1] == '/':
            idp = idp[:-1]
        url = '/'.join((idp, 'login/password'))

        data = {
            'username': username,
            'password': password
        }

        r = self.client.post(url, data=data)
        r.raise_for_status()

        if not self.is_login:
            raise Exception('Cannot login.')

        print("* ", r)

#
# The solid-file package is needed for this example to work.
#
#     python3 -m pip install solid-file
#
from solid.auth import Auth
from solid.solid_api import SolidAPI

########################################################################################################################
#
#
#
print(f">>>--------------------------------------------<<<")
print(f">>> Linked-Open-Data Cloud - the cloud of PODs <<<")
print(f">>>--------------------------------------------<<<")
print(f">>>")
print(f">>>")
print(f">>> SOLID datapod [{POD_ENDPOINT}] is used with IDP: [{IDP}] for user: [{USERNAME}]")
print(f">>>")
print(f">>>")
print("* Login ...")
auth = Auth2()
#auth = Auth()
api = SolidAPI(auth)
auth.login(IDP, USERNAME, PASSWORD)
print( f"*       ... DONE")
print("*")

########################################################################################################################
#
# We define the public folder in the datapod as our "base folder".
#
folder_url = f"{POD_ENDPOINT}/public/"

#
# We check if the base folder is ready.
#
if not api.item_exists(folder_url):
    print( f"'* The basefolder {folder_url} is not available. " )
    # print(api.create_folder(folder_url))
    exit()
else:
    print( f"* Ready to use the basefolder {folder_url}. " )
print("*")

########################################################################################################################
# Some example files ...
#
import io
import datetime

print( f"* Create/overwrite a (new) a file in basefolder {folder_url}. " )
NOW = datetime.datetime.now()
data = io.BytesIO(f"I ❤️ 🌱 {NOW}".encode("utf-8"))
file_url = f"{folder_url}hello.txt"
print( api.put_file(file_url, data, 'text/plain') )
print( f"* Filename: {file_url}. " )
print("*")

print( f"* Create/overwrite a (new) a file in basefolder {folder_url}. " )
data = f"At: {NOW} the profile has been changed by the ecolytiq agent. You can stop this by <<<here>>>."
data = io.BytesIO( bytes( data, 'utf-8' ) )
msg_url = f"{folder_url}message.txt"
print(api.put_file(msg_url, data, 'text/plain'))
print( f"* Filename: {msg_url}. " )
print("*")

print( f"* Read a profile-file from basefolder {folder_url}. " )
folder_data = api.read_folder(folder_url)
files = "\n".join(list(map(lambda x: x.name, folder_data.files)))
print("*")

#
# Delete some resources ...
#
#file_url1 = f"{folder_url1}hello.txt"
#msg_url1 = f"{folder_url1}message.txt"
#
#resp = api.delete(file_url1)
#print(f"**{resp.text}**")
#
#resp = api.delete(msg_url1)
#print(f"**{resp.text}**")

#
# Show the persisted personal profile ...
#
print("****** personal profile from datapod ******")
print("")
profile_url = "https://kamir.solidcommunity.net/public/ecolytiq-sustainability-profile/"
resp = api.get(profile_url)
print(f"-----PROFILE DATA-----\n{resp.text}----------------------")

#
# Provide new facts and add those to the profile ....
#
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, OWL

from rdflib import Graph, Namespace, OWL

import requests
url = "http://www.w3.org/People/Berners-Lee/card"
f = requests.get(url)
print(f.text)


g = Graph()
g.parse(data=resp.text, format="turtle")

for s, p, o in g:
    print(s, p, o)

import random
from rdflib.namespace import RDFS, XSD, FOAF


layer = ['1', '2', '3','4', '5', '6','7', '8', '9','10']


# general relations
geolayer = Namespace('http://geoqb.com/layer/general#')
g.bind('geoqb',geolayer)

for l in layer :
    rel = URIRef('http://geoqb.com/layer/general#weight_for_layer_' + l)
    g.add((rel, RDF.value, Literal( str(random.random()) )))


for lId in range( 0, 10 ):
    print(lId)

#
# Store the changed profile data in the datapod ....
#

newData = g.serialize(format='n3')

print( newData )

profile_url = "https://kamir.solidcommunity.net/public/ecolytiq-sustainability-profile/profile1.ttl"
resp = api.put_file(profile_url, newData, 'text/plain')

layer_weights = {}

for s, p, o in g:
    # print(s, p, o)

    parts = s.split("weight_for_layer_")
    # print( parts )

    if parts[0] == "http://geoqb.com/layer/general#":
        layer_weights[parts[1]] = o
        print( str(parts[1]) + " => " + str( layer_weights[parts[1]] ) )





folder_url = f"{POD_ENDPOINT}/public/myList_CLT2023"
resp = api.get(folder_url)
print(f"-----PROFILE DATA-----\n{resp.text}----------------------")

print( "Done." )