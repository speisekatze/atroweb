from django.views import generic
from django.conf import settings
from home.models import Menu


def get_defaults():
    return {
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'menu_list': Menu.objects.filter(status=1).order_by('sort')
    }


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seite'] = 'Home'
        context.update(get_defaults())
        return context
