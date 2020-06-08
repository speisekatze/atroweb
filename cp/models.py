from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.db import models


# Create your models here.
class UserModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()
    socialclub_id = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField()
    password = models.CharField(max_length=100, null=False, blank=False)
    discord_name = models.CharField(max_length=100, null=False, blank=False)
    account_id = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    verified_date = models.DateTimeField()
    verified = models.IntegerField()
    verify_sent = models.DateTimeField()
    verify_token = models.CharField()
    password_reset = models.DateTimeField()
    password_reset_token = models.CharField()


class RolesModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()


class UserRolesModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    role = models.ForeignKey(RolesModel, on_delete=models.CASCADE)


class RightsModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()


class RoleRightsModel(models.Model):
    role = models.ForeignKey(RolesModel, on_delete=models.CASCADE)
    right = models.ForeignKey(RightsModel, on_delete=models.CASCADE)


class UserNotesModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()
    content = MarkdownxField()
    private = models.BooleanField()
    admin = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def get_content(self):
        return markdownify(self.content)


class CharacterModel(models.Model):
    id = models.AutoField(primary_key=True)
    ingame_id = models.IntegerField()


class UserCharacterModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    char = models.ForeignKey(CharacterModel, on_delete=models.CASCADE)


class UserBanModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserModel)
    reason = models.TextField()
    until = models.DateTimeField()
    parole = models.IntegerField()
    parole_requested = models.CharField()
    parole_granted = models.CharField()
    parole_granted_by = models.ForeignKey(UserModel)
