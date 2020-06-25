import secrets
import os
import bcrypt


def generate_token():
    return secrets.token_urlsafe(64)


def generate_salt(size=6):
    return bcrypt.gensalt().decode('utf-8')


def gen_unique(size=6):
    return sum([x*255**ind for ind, x in enumerate([x for x in reversed(os.urandom(6))])])


def make_secure(password, salt):
    return bcrypt.hashpw(password.encode(), salt.encode()).decode('utf-8')


def check_pw(pw, hash):
    return bcrypt.checkpw(pw.encode(), hash)
