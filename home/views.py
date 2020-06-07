from django.views import generic
from django.conf import settings
from .models import Page


def get_defaults():
    return {
        'LANGUAGE_CODE': settings.LANGUAGE_CODE
    }


class IndexView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seite'] = 'Home'
        context['content'] = Page.objects.filter(name='test')[0].get_content()
        context['title'] = Page.objects.filter(name='test')[0].title
        context.update(get_defaults())
        return context


class ImpressumView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seite'] = 'Impressum'
        context['content'] = Page.objects.filter(name='impressum')[0].get_content()
        context['title'] = Page.objects.filter(name='impressum')[0].title
        context.update(get_defaults())
        return context


class DatenschutzView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seite'] = 'Datenschutzerklärung'
        context['content'] = Page.objects.filter(name='datenschutz')[0].get_content()
        context['title'] = Page.objects.filter(name='datenschutz')[0].title
        context.update(get_defaults())
        return context
