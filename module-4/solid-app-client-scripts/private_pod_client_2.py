# -*- coding: utf-8 -*-

from openidc_client import OpenIDCClient
from oic.oic import Client as OicClient
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
import httpx


USERNAME = "kamir"
PASSWORD = "12345PodTest#"
IDP = 'https://solidcommunity.net'
POD_ENDPOINT = "https://kamir.solidcommunity.net"

# Before this register the client to get an id and secret
# oidc-register --debug http://localhost:3000 http://localhost:12345/ http://localhost:23456/
issuer = POD_ENDPOINT # "http://localhost:3000/"
provider_info = httpx.get(issuer + ".well-known/openid-configuration").json()
print( provider_info )

# one will most likely have to pass their own endpoint in place of 'http://localhost:12345/' below
# it might not work with the below endpoint 'http://localhost:12345/' in all flows since the "magic" is handled by
# OpenIDCClient and involves interacting with opening a browser on localhost (see OpenIDCClient._get_new_token() for how it works)
# this endpoint will receive a callback from OIDC and exchange an authorization code for DPoP access token by POSTing
# to provider_info['token_endpoint'] as done here:
# https://gitlab.com/arbetsformedlingen/individdata/oak/cms/-/blob/main/case_management/controllers/controllers.py#L264
registration_response = OicClient(
    client_authn_method=CLIENT_AUTHN_METHOD).register(provider_info.get('registration_endpoint'),
                                                      redirect_uris=[IDP])

client_id = registration_response['client_id']
client_secret = registration_response['client_secret']

client = OpenIDCClient("user", issuer,
                       {"Authorization": "idp/auth", "Token": "idp/token"},
                       client_id=client_id,
                       client_secret=client_secret,
                       use_pkce=True)

print( "Done." )