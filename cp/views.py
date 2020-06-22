from datetime import timedelta
from django.utils import timezone
from django.views import generic
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, render
from home.models import Menu
from .models import User
from .forms import LoginForm, PwResetForm, RegisterForm, NewPasswordForm
from .token import generate_token, generate_salt, make_secure, gen_unique
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
    success_url = 'profile'

    def __init__(self, *args, **kwargs):
        super(LoginFormView, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        if self.request.session.get('uid') and self.request.session.get('token'):
            user_set = User.objects.filter(id=self.request.session.get('uid'))
            if user_set is not None:
                user = user_set[0]
                if (timezone.now() - user.updated_on) > timedelta(seconds=3600*8):
                    user.session_token = ''
                    user.updated_on = timezone.now()
                    user.save()
                else:
                    if user.session_token == self.request.session.get('token'):
                        user.updated_on = timezone.now()
                        user.save()
                        return redirect('cp:profile')
        return super().get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_defaults())
        context['seite'] = self.seite
        context['loginpage'] = True
        return context

    def form_valid(self, form):
        user = form.cleaned_data['user']
        user.session_token = generate_token()
        user.updated_on = timezone.now()
        user.save()
        self.request.session['uid'] = user.id
        self.request.session['token'] = user.session_token
        return super(LoginFormView, self).form_valid(form)


class PwResetFormView(generic.FormView):
    template_name = 'cp/login.html'
    seite = 'Passwort zurücksetzen'
    form_class = PwResetForm
    success_url = 'pwsent'

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
            user.password_reset = timezone.now()
            user.password_reset_token = token
            user.save()
            send_mail('Password reset Notification', 'The Link to reset your password: http://79.200.226.103/cp/reset/'+token+'/', 'register@atropity.de', [email])
        return super(PwResetFormView, self).form_valid(form)


class PwSentView(generic.TemplateView):
    template_name = 'cp/verify.html'
    seite = 'Mail versendet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_defaults())
        context['seite'] = self.seite
        context['successmail'] = True
        return context


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
        user.id = gen_unique()
        user.verified = False
        user.verify_token = token
        user.verify_sent = timezone.now()
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

        user_set = find_by_token(kwargs['token'], 0)
        if user_set is not False:
            user = user_set[0]
            user.verified = True
            user.verified_date = timezone.now()
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
    success_url = '/cp/signin'
    token = None

    def __init__(self, *args, **kwargs):
        super(NewPasswdView, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        self.token = kwargs['token']
        user_set = find_by_token(self.token, 1)
        print(self.token)
        if user_set is False:
            c = self.get_context_data(**kwargs)
            return render(self.request, 'cp/verify.html', c)
        return super().get(self, *args, **kwargs)

    def get_initial(self):
        initial = super(NewPasswdView, self).get_initial()
        user_set = find_by_token(self.token, 1)
        if user_set is not False:
            initial.update({'uid': user_set[0].id})
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_defaults())
        context['seite'] = self.seite
        context['signuppage'] = True
        return context

    def form_valid(self, form):
        password = form.cleaned_data['password']
        uid = form.cleaned_data['uid']
        user_set = User.objects.all().filter(id=uid)
        if user_set is None:
            return redirect('login')
        user = user_set[0]
        user.salt = generate_salt(6)
        user.password = make_secure(password, user.salt)
        user.password_reset_token = ''
        user.save()
        return super(NewPasswdView, self).form_valid(form)


class ProfileView(generic.TemplateView):
    template_name = 'cp/profile.html'
    seite = 'Profil'
    user = None

    def get(self, *args, **kwargs):
        user_set = User.objects.all().filter(id=self.request.session.get('uid'))
        if len(user_set) < 1:
            return redirect('cp:signin')
        self.user = user_set[0]
        if self.user.session_token != self.request.session.get('token'):
            return redirect('cp:signin')
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_defaults())
        context['seite'] = self.seite
        context['user'] = self.user
        return context
