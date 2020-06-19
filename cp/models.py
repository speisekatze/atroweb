from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()
    socialclub_id = models.CharField(max_length=50, null=True, blank=False)
    email = models.EmailField()
    password = models.CharField(max_length=140, null=False, blank=False)
    discord_name = models.CharField(max_length=100, null=True, blank=False)
    account_id = models.IntegerField(null=True, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    verified_date = models.DateTimeField(null=True)
    verified = models.BooleanField()
    verify_sent = models.DateTimeField(null=True)
    verify_token = models.CharField(max_length=100, null=True)
    password_reset = models.DateTimeField(null=True)
    password_reset_token = models.CharField(max_length=100, null=True)
    salt = models.CharField(max_length=10)


class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()


class UserRoles(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    unique_together = (
        'user',
        'role',
    )


class Rights(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()


class RoleRights(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    right = models.ForeignKey(Rights, on_delete=models.CASCADE)
    unique_together = (
        'role',
        'right',
    )


class UserNotes(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()
    content = MarkdownxField()
    private = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, default=0, on_delete=models.SET_DEFAULT,
                                   related_name='creator')
    updated_by = models.ForeignKey(User, default=0, on_delete=models.SET_DEFAULT,
                                   related_name='updater')

    def get_content(self):
        return markdownify(self.content)


class Character(models.Model):
    id = models.AutoField(primary_key=True)
    ingame_id = models.IntegerField()


class UserCharacter(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    char = models.ForeignKey(Character, on_delete=models.CASCADE)
    unique_together = (
        'user',
        'char',
    )


class UserBan(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='banned_user')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, default=0, on_delete=models.SET_DEFAULT,
                                   related_name='banning_user')
    reason = models.TextField()
    until = models.DateTimeField()
    parole = models.BooleanField(default=False)
    parole_requested = models.BooleanField(default=False)
    parole_granted = models.BooleanField(default=False)
    parole_granted_by = models.ForeignKey(User, default=0, on_delete=models.SET_DEFAULT,
                                          related_name='paroler')
    parole_until = models.DateTimeField()


class Fragebogen(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    created_on = models.DateTimeField(auto_now_add=True)
    answered_on = models.DateTimeField()
    application_text = models.TextField()
    processed_by = models.ForeignKey(User, default=0, on_delete=models.SET_DEFAULT,
                                     related_name='processing_user')


class Fragen(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()
    text = MarkdownxField()
    time_to_answer = models.IntegerField(default=30)


class Antworten(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()
    frage = models.ForeignKey(Fragen, on_delete=models.CASCADE)
    text = MarkdownxField()
    richtig = models.BooleanField(default=0)


class FragebogenFragen(models.Model):
    id = models.AutoField(primary_key=True)
    bogen = models.ForeignKey(Fragebogen, on_delete=models.CASCADE)
    frage = models.ForeignKey(Fragen, on_delete=models.PROTECT)
    antwort = models.ForeignKey(Antworten, on_delete=models.PROTECT)
    richtig = models.BooleanField(default=False)
