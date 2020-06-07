from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


# Create your models here.
class Page(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()
    title = models.CharField(max_length=100, null=True, default="Title")
    content = MarkdownxField()
    status = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def get_content(self):
        return markdownify(self.content)


class Faq(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField()
    question = MarkdownxField()
    answer = MarkdownxField()
    status = models.IntegerField(default=1)
    sort = models.IntegerField(default=1)

    def get_question(self):
        return markdownify(self.question)

    def get_answer(self):
        return markdownify(self.answer)


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False, blank=False)
    slug = models.SlugField()
    url = models.CharField(max_length=100, null=False, blank=False)
    target = models.CharField(max_length=50, null=False, blank=False, default="_self")
    status = models.IntegerField(default=1)
    sort = models.IntegerField(default=1)
