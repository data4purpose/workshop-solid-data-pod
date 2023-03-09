# TODO(agentydragon): add logout

import base64
import datetime
import hashlib
import json
import os
import re
import urllib

import flask
import jwcrypto
import jwcrypto.jwk
import jwcrypto.jws
import jwcrypto.jwt
import requests
from absl import app, flags, logging
from oic.oic import Client as OicClient
from oic.utils.authn.client import CLIENT_AUTHN_METHOD

_PORT = flags.DEFINE_integer('port', 3333, 'HTTP port to listen on')
_ISSUER = flags.DEFINE_string('issuer', 'https://solidcommunity.net/', 'Issuer')

_OID_CALLBACK_PATH = "/oauth/callback"


def get_redirect_url():
    return f"http://localhost:{_PORT.value}{_OID_CALLBACK_PATH}"


def make_random_string():
    x = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    x = re.sub('[^a-zA-Z0-9]+', '', x)
    return x


def make_verifier_challenge():
    code_verifier = make_random_string()

    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
    code_challenge = code_challenge.replace('=', '')

    return code_verifier, code_challenge


def register_client(provider_info):
    # Client registration.
    # https://pyoidc.readthedocs.io/en/latest/examples/rp.html#client-registration
    registration_response = OicClient(
        client_authn_method=CLIENT_AUTHN_METHOD).register(
            provider_info['registration_endpoint'],
            redirect_uris=[get_redirect_url()])
    logging.info("Registration response: %s", registration_response)
    return registration_response['client_id']


def make_token_for(keypair, uri, method):
    jwt = jwcrypto.jwt.JWT(header={
        "typ":
        "dpop+jwt",
        "alg":
        "ES256",
        "jwk":
        keypair.export(private_key=False, as_dict=True)
    },
                           claims={
                               "jti": make_random_string(),
                               "htm": method,
                               "htu": uri,
                               "iat": int(datetime.datetime.now().timestamp())
                           })
    jwt.make_signed_token(keypair)
    return jwt.serialize()


_TEMPLATE = """
<h2>Login status</h2>
{% if web_id %}
  You are logged in as {{ web_id }}.
{% else %}
  You are not logged in.
{% endif %}

<h2>Resource content</h2>
{% if resource %}
  <pre>{{ resource_content }}</pre>
{% else %}
  Use the form below to read a resource.
{% endif %}

<form action=/ method=GET>
  <input
      value="{{ resource }}"
      placeholder='https://you.solidcommunity.net/private/...'
      name='resource'>
  <input type=submit value=Read>
</form>
"""


def main(_):
    # Provider info discovery.
    # https://pyoidc.readthedocs.io/en/latest/examples/rp.html#provider-info-discovery
    provider_info = requests.get(_ISSUER.value +
                                 ".well-known/openid-configuration").json()
    logging.info("Provider info: %s", provider_info)
    client_id = register_client(provider_info)

    flask_app = flask.Flask(__name__)
    flask_app.secret_key = 'notreallyverysecret123'

    # keyed by state, contains {'key': {...}, 'code_verifier': ...}
    STATE_STORAGE = {}

    @flask_app.route('/')
    def index():
        tested_url = flask.request.args.get('resource', '')

        if ('access_token' in flask.session) and ('key' in flask.session):
            logging.info("loading access token and key from session")
            keypair = jwcrypto.jwk.JWK.from_json(flask.session['key'])
            access_token = flask.session['access_token']
            headers = {
                'Authorization': ('DPoP ' + access_token),
                'DPoP': make_token_for(keypair, tested_url, 'GET')
            }
            decoded_access_token = jwcrypto.jwt.JWT(jwt=access_token)
            # TODO(agentydragon): should we also verify the payload against
            # the signature it has?
            web_id = json.loads(
                decoded_access_token.token.objects['payload'])['sub']
            # TODO(agentydragon): if we pull the webid from here, it needs
            # further validation.
        else:
            headers = {}
            web_id = None

        if tested_url:
            # Read file from Solid.
            # TODO(agentydragon): handle token expiration, refreshes, etc.
            resp = requests.get(url=tested_url, headers=headers)
            if resp.status_code == 401:
                logging.info("Got 401 trying to access %s.", tested_url)
                code_verifier, code_challenge = make_verifier_challenge()

                state = make_random_string()
                assert state not in STATE_STORAGE
                STATE_STORAGE[state] = {
                    'code_verifier': code_verifier,
                    'redirect_url': flask.request.url
                }

                query = urllib.parse.urlencode({
                    "code_challenge":
                    code_challenge,
                    "state":
                    state,
                    "response_type":
                    "code",
                    "redirect_uri":
                    get_redirect_url(),
                    "code_challenge_method":
                    "S256",
                    "client_id":
                    client_id,
                    # offline_access: also asks for refresh token
                    "scope":
                    "openid offline_access",
                })
                url = provider_info['authorization_endpoint'] + '?' + query
                return flask.redirect(url)
            elif resp.status_code != 200:
                raise Exception(
                    f"Unexpected status code: {resp.status_code} {resp}")

            resource_content = resp.text
        else:
            resource_content = None

        return flask.Response(flask.render_template_string(
            _TEMPLATE,
            web_id=web_id,
            resource_content=resource_content,
            resource=tested_url),
                              mimetype='text/html')

    @flask_app.route(_OID_CALLBACK_PATH)
    def oauth_callback():
        auth_code = flask.request.args['code']
        state = flask.request.args['state']
        assert state in STATE_STORAGE, f"state {state} not in STATE_STORAGE?"

        # Generate a key-pair.
        keypair = jwcrypto.jwk.JWK.generate(kty='EC', crv='P-256')

        code_verifier = STATE_STORAGE[state].pop('code_verifier')

        # Exchange auth code for access token
        resp = requests.post(url=provider_info['token_endpoint'],
                             data={
                                 "grant_type": "authorization_code",
                                 "client_id": client_id,
                                 "redirect_uri": get_redirect_url(),
                                 "code": auth_code,
                                 "code_verifier": code_verifier,
                             },
                             headers={
                                 'DPoP':
                                 make_token_for(
                                     keypair, provider_info['token_endpoint'],
                                     'POST')
                             },
                             allow_redirects=False)
        result = resp.json()
        logging.info("%s", result)

        flask.session['key'] = keypair.export()
        flask.session['access_token'] = result['access_token']

        decoded_access_token = jwcrypto.jwt.JWT()
        decoded_access_token.deserialize(result['access_token'])
        decoded_id_token = jwcrypto.jwt.JWT()
        decoded_id_token.deserialize(result['id_token'])
        logging.info("access token: %s", decoded_access_token)
        logging.info("id token: %s", decoded_id_token)

        # TODO(agentydragon): at this point can probably drop STATE_STORAGE[state]
        return flask.redirect(STATE_STORAGE[state].pop('redirect_url'))

    flask_app.run(port=_PORT.value)


if __name__ == '__main__':
    app.run(main)
