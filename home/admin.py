from django.db import models
from django.contrib import admin
from markdownx.widgets import AdminMarkdownxWidget
from .models import Page, Faq, Menu


# Register your models here.
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'version', 'status', 'created_on')
    list_filter = ("status",)
    search_fields = ['name', 'content']
    prepopulated_fields = {'slug': ('name',)}
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


class FaqAdmin(admin.ModelAdmin):
    list_display = ('slug', 'question', 'status')
    list_filter = ('status', )
    search_fields = ['name', 'question']
    prepopulated_fields = {'slug': ('name',)}
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


class MenuAdmin(admin.ModelAdmin):
    list_display = ('slug', 'url', 'status', 'sort')
    list_filter = ('status', )
    search_fields = ['name',]
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Menu, MenuAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Faq, FaqAdmin)
