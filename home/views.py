from django.views import generic
from django.conf import settings
from django.http import HttpResponse
from .models import Page, Menu, Faq


INDEX_TEMPLATE = 'home/index.html'


def go_fuck_yourself(request):
    return HttpResponse('GO FUCK YOURSELF!')


def get_defaults():
    return {
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'menu_list': Menu.objects.filter(status=1).order_by('sort')
    }


class IndexView(generic.TemplateView):
    template_name = INDEX_TEMPLATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seite'] = 'Home'
        context['content'] = Page.objects.filter(name='test')[0].get_content()
        context['title'] = Page.objects.filter(name='test')[0].title
        context.update(get_defaults())
        return context


class ImpressumView(generic.TemplateView):
    template_name = INDEX_TEMPLATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seite'] = 'Impressum'
        context['content'] = Page.objects.filter(name='impressum')[0].get_content()
        context['title'] = Page.objects.filter(name='impressum')[0].title
        context.update(get_defaults())
        return context


class DatenschutzView(generic.TemplateView):
    template_name = INDEX_TEMPLATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seite'] = 'Datenschutzerklärung'
        context['content'] = Page.objects.filter(name='datenschutz')[0].get_content()
        context['title'] = Page.objects.filter(name='datenschutz')[0].title
        context.update(get_defaults())
        return context


class FaqView(generic.TemplateView):
    template_name = 'home/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seite'] = 'FAQ'
        faq = []
        for f in Faq.objects.filter(status=1).order_by('sort'):
            faq.append({'question': f.get_question(), 'answer': f.get_answer()})
        context['faq_list'] = faq
        context['title'] = 'FAQ'
        context.update(get_defaults())
        return context
