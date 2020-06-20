from .models import User
from .token import make_secure


def username_already_used(username):
    user = User.objects.all().filter(name__iexact=username)
    print(user)
    if len(user) > 0:
        return True
    return False


def email_already_used(email):
    user = User.objects.all().filter(email__iexact=email)
    if len(user) > 0:
        return True
    return False


def is_verified(username):
    user = User.objects.all().filter(name__iexact=username, verified=True)
    if len(user) > 0:
        return True
    return False


def check_password(username, password):
    user = User.objects.all().filter(name__iexact=username)
    if len(user) < 1:
        return False
    pw = make_secure(password, user[0].salt)
    if pw == user[0].password:
        return True
    return False


def find_by_token(token):
    user = User.objects.all().filter(verify_token__iexact=token)
    if len(user) < 1:
        return False
    return user


def find_by_mail(email):
    user = User.objects.all().filter(email__iexact=email)
    if len(user) < 1:
        return False
    return user
