import secrets
import os
import base64
import hashlib


def generate_token():
    return secrets.token_urlsafe(64)


def generate_salt(size=6):
    return base64.b64encode(os.urandom(size)).decode('utf-8')


def gen_unique(size=6):
    return sum([x*255**ind for ind, x in enumerate([x for x in reversed(os.urandom(6))])])


def make_secure(password, salt):
    h = hashlib.sha3_512()
    h.update((salt + password).encode())
    return h.hexdigest()
