from django.views import generic
from django.conf import settings
from home.models import Menu
from .forms import LoginForm, PwResetForm, RegisterForm


def get_defaults():
    return {
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'menu_list': Menu.objects.filter(status=1).order_by('sort'),
        'title': 'User Control Panel'
    }


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seite'] = 'Home'
        context.update(get_defaults())
        return context


class LoginFormView(generic.FormView):
    template_name = 'cp/login.html'
    seite = 'Anmelden'
    form_class = LoginForm
    success_url = 'ergebniss'

    def __init__(self, *args, **kwargs):
        super(LoginFormView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_defaults())
        context['seite'] = self.seite
        context['loginpage'] = True
        return context


class PwResetFormView(generic.FormView):
    template_name = 'cp/login.html'
    seite = 'Passwort zurücksetzen'
    form_class = PwResetForm
    success_url = 'ergebniss'

    def __init__(self, *args, **kwargs):
        super(PwResetFormView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_defaults())
        context['seite'] = self.seite
        context['pwrestpage'] = True
        return context


class RegisterFormView(generic.FormView):
    template_name = 'cp/login.html'
    seite = 'Account registrieren'
    form_class = RegisterForm
    success_url = 'ergebniss'

    def __init__(self, *args, **kwargs):
        super(RegisterFormView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_defaults())
        context['seite'] = self.seite
        context['signuppage'] = True
        return context
