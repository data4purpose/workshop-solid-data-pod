# solid-flask

This is a simple Flask app that can authenticate against a Solid pod and read
private data from it.

It should become simpler when [Demonstration of
Proof-of-Possession](https://tools.ietf.org/html/draft-fett-oauth-dpop-04) gets
implemented in some Python OAuth library. Unfortunately, as of time of writing,
I can't find a Python library that implements DPoP, and Solid seems to require
it.

## Running

* Install [Bazel](https://bazel.build).
* Run the app with: `bazel run :flask_solid_main`.
  If you want to use a issuer other than https://solidcommunity.net/, pass:
  `bazel run :flask_solid_main -- --issuer=https://...`
