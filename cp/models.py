from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


# Create your models here.
class UserModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()
    socialclub = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField()


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
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()
    content = MarkdownxField()
    private = models.BooleanField()
    admin = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def get_content(self):
        return markdownify(self.content)
