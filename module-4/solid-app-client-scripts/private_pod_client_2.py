# -*- coding: utf-8 -*-

from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
IDP = os.getenv("IDP")
WEB_ID = os.getenv("WEB_ID")
POD_ENDPOINT = os.getenv("POD_ENDPOINT")

APP_NAME=os.getenv("APP_NAME")
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")

print( "---------------------------------")
print( "USERNAME",USERNAME )
print( "PASSWORD",PASSWORD )
print( "IDP",IDP )
print( "WEB_ID",WEB_ID )
print( "POD_ENDPOINT",POD_ENDPOINT )
print( "APP_NAME",APP_NAME )
print( "CLIENT_ID",CLIENT_ID )
print( "CLIENT_SECRET", CLIENT_SECRET)
print( "---------------------------------")

#-------------------------------------------------
# This example represents a registered Solid-App.
#
# During registration in a Data Pod we create a
# CLIENT_ID and a CLIENT SECRET.
#-------------------------------------------------

import base64, requests

client_id = CLIENT_ID
client_secret = CLIENT_SECRET

# Encode the client ID and client secret
authorization = base64.b64encode(bytes(client_id + ":" + client_secret, "ISO-8859-1")).decode("ascii")

headers = {
    "Authorization": f"Basic {authorization}",
    "Content-Type": "application/x-www-form-urlencoded"
}
body = {
    "grant_type": "client_credentials"
}

response = requests.post( IDP+"/token", data=body, headers=headers)

print(response.text)

import json
values = json.loads(response.text)

access_token = values['access_token']
print("------ access token ------")
print( access_token )
print("--------------------------")








from solidclient.solid_client import SolidAPIWrapper
import jwcrypto

# keys used for DPoP verification
keypair = jwcrypto.jwk.JWK.generate(kty='EC', crv='P-256')

# wrapper around SolidAPI, injects give access_token to OpenIDCClient with _add_token()
api = SolidAPIWrapper(client_id=client_id,
                      client_secret=client_secret,
                      access_token=values,
                      keypair=keypair)

# works only on resources where ACL allows access for Everyone
url = POD_ENDPOINT+"bookmarks/"
a = api.item_exists(url)
print( "----- api.item_exists(", url, ")" )
print( a )
print( "---------------------------------------------" )




# works only on resources where ACL allows access for Everyone
url = POD_ENDPOINT+"new_folder_001/"
api.create_folder(url)



import io
url = POD_ENDPOINT + "bookmarks/second.txt"
data = io.BytesIO(b"Welcoome to Chemnitz!")
print(api.put_file(url, data, 'text/plain'))
resp = api.get(url)
print(f"*** {resp.text} ***")

print( "Done." )