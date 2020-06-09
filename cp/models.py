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
    verified = models.BooleanField()
    verify_sent = models.DateTimeField()
    verify_token = models.CharField(max_length=100)
    password_reset = models.DateTimeField()
    password_reset_token = models.CharField(max_length=100)


class RolesModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()


class UserRolesModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    role = models.ForeignKey(RolesModel, on_delete=models.CASCADE)
    unique_together = (
        'user',
        'role',
    )


class RightsModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()


class RoleRightsModel(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(RolesModel, on_delete=models.CASCADE)
    right = models.ForeignKey(RightsModel, on_delete=models.CASCADE)
    unique_together = (
        'role',
        'right',
    )


class UserNotesModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()
    content = MarkdownxField()
    private = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserModel, default=0, on_delete=models.SET_DEFAULT,
                                   related_name='creator')
    updated_by = models.ForeignKey(UserModel, default=0, on_delete=models.SET_DEFAULT,
                                   related_name='updater')

    def get_content(self):
        return markdownify(self.content)


class CharacterModel(models.Model):
    id = models.AutoField(primary_key=True)
    ingame_id = models.IntegerField()


class UserCharacterModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    char = models.ForeignKey(CharacterModel, on_delete=models.CASCADE)
    unique_together = (
        'user',
        'char',
    )


class UserBanModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='banned_user')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserModel, default=0, on_delete=models.SET_DEFAULT,
                                   related_name='banning_user')
    reason = models.TextField()
    until = models.DateTimeField()
    parole = models.BooleanField(default=False)
    parole_requested = models.BooleanField(default=False)
    parole_granted = models.BooleanField(default=False)
    parole_granted_by = models.ForeignKey(UserModel, default=0, on_delete=models.SET_DEFAULT,
                                          related_name='paroler')
    parole_until = models.DateTimeField()


class FragebogenModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user')
    created_on = models.DateTimeField(auto_now_add=True)
    answered_on = models.DateTimeField()
    application_text = models.TextField()
    processed_by = models.ForeignKey(UserModel, default=0, on_delete=models.SET_DEFAULT,
                                     related_name='processing_user')


class FragenModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()
    text = MarkdownxField()


class AntwortenModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()
    frage = models.ForeignKey(FragenModel, on_delete=models.CASCADE)
    text = MarkdownxField()
    richtig = models.BooleanField(default=0)


class FragebogenFragenModel(models.Model):
    id = models.AutoField(primary_key=True)
    bogen = models.ForeignKey(FragebogenModel, on_delete=models.CASCADE)
    frage = models.ForeignKey(FragenModel, on_delete=models.PROTECT)
    antwort = models.ForeignKey(AntwortenModel, on_delete=models.PROTECT)
    richtig = models.BooleanField(default=False)
