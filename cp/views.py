from datetime import datetime
from django.views import generic
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from home.models import Menu
from .models import User
from .forms import LoginForm, PwResetForm, RegisterForm, NewPasswordForm
from .token import generate_token, generate_salt, make_secure
from .helper import find_by_mail, find_by_token


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
    success_url = 'login'

    def __init__(self, *args, **kwargs):
        super(LoginFormView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_defaults())
        context['seite'] = self.seite
        context['loginpage'] = True
        return context

    def form_valid(self, form):
        return super(LoginFormView, self).form_valid(form)


class PwResetFormView(generic.FormView):
    template_name = 'cp/login.html'
    seite = 'Passwort zurücksetzen'
    form_class = PwResetForm
    success_url = 'reset'

    def __init__(self, *args, **kwargs):
        super(PwResetFormView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_defaults())
        context['seite'] = self.seite
        context['pwrestpage'] = True
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        token = generate_token()
        user_set = find_by_mail(email)
        if user_set is not False:
            user = user_set[0]
            user.password_reset = datetime.now()
            user.password_reset_token = token
            user.save()
            send_mail('Password reset Notification', 'The Link to reset your password: http://79.200.226.103/cp/reset/'+token+'/', 'register@atropity.de', [email])
        return super(RegisterFormView, self).form_valid(form)


class RegisterFormView(generic.FormView):
    template_name = 'cp/login.html'
    seite = 'Account registrieren'
    form_class = RegisterForm
    success_url = 'register'

    def __init__(self, *args, **kwargs):
        super(RegisterFormView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_defaults())
        context['seite'] = self.seite
        context['signuppage'] = True
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        token = generate_token()
        user = User(name=username, email=email)
        user.verified = False
        user.verify_token = token
        user.verify_sent = datetime.now()
        user.salt = generate_salt(6)
        user.password = make_secure(password, user.salt)
        user.save()
        send_mail('Email Verification', 'The Link to verify your email address: http://79.200.226.103/cp/verify/'+token+'/', 'register@atropity.de', [email])
        return super(RegisterFormView, self).form_valid(form)


class RegisterResultView(generic.TemplateView):
    template_name = 'cp/register_result.html'
    seite = 'Erfolg'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_defaults())
        context['seite'] = self.seite
        return context


class VerifyView(generic.TemplateView):
    template_name = 'cp/verify.html'
    seite = 'Erfolg'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_defaults())

        user_set = find_by_token(kwargs['token'])
        if user_set is not False:
            user = user_set[0]
            user.verified = True
            user.verified_date = datetime.now()
            user.verify_token = 'already_used'
            user.save()
            context['success'] = True
            context['seite'] = 'Erfolg'
        else:
            context['seite'] = 'Fehler'
        return context


class NewPasswdView(generic.FormView):
    template_name = 'cp/login.html'
    seite = 'Neues Passwort'
    form_class = NewPasswordForm
    success_url = 'register'

    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_defaults())
        context['seite'] = self.seite
        context['signuppage'] = True
        user_set = find_by_token(kwargs['token'])
        if user_set is not False:
            context['success'] = True
        else:
            context['success'] = False
            context['seite'] = 'Fehler'
        return context

    def form_valid(self, form):
        password = form.cleaned_data['password']
        
        user.password = make_secure(password, user.salt)
        user.save()
        return redirect('profile')
