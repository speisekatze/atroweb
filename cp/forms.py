from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms
from .models import User
from .token import make_secure


class LoginForm(forms.Form):
    username = forms.CharField(label="Benutzername")
    password = forms.CharField(label="Passwort", widget=forms.PasswordInput, min_length=8)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.form_id = 'login'
        self.helper.form_style = 'inline'
        self.helper.label_class = 'label'
        self.helper.field_class = 'input'

        self.helper.layout = Layout(
            Fieldset(
                'Login',
                'username',
                'password',
                ButtonHolder(
                    Submit('submit', 'Senden')
                )
            )
        )

    def clean(self):
        form_data = self.cleaned_data
        pw = form_data['password']
        username = form_data['username']
        uname = User.objects.filter(email=username)
        mail = User.objects.filter(name=username)
        user = None
        if uname.exists():
            user = uname[0]
        if mail.exists():
            user = mail[0]
        if make_secure(pw, user.salt) != user.password:
            user = None
        if user is None:
            self._errors["username"] = ["Benutzername unbekannt oder "]
            self._errors["password"] = ["Passwort ist falsch."]
        return {'user': user}


class PwResetForm(forms.Form):
    email = forms.EmailField(label='Email Adresse')

    def __init__(self, *args, **kwargs):
        super(PwResetForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.form_style = 'inline'
        self.helper.form_id = 'reset'
        self.helper.label_class = 'label'
        self.helper.field_class = 'input'

        self.helper.layout = Layout(
            Fieldset(
                'Passwort zurücksetzen',
                'email',
                ButtonHolder(
                    Submit('submit', 'Senden')
                )
            )
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Die angegebene Adresse ist unbekannt.")
        return email


class RegisterForm(forms.Form):
    username = forms.CharField(label='Benutzername')
    email = forms.EmailField(label='Email Adresse')
    password_one = forms.CharField(label="Passwort", widget=forms.PasswordInput, min_length=8)
    password_two = forms.CharField(label="Passwort wiederholen", widget=forms.PasswordInput,
                                   min_length=8)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = 'register'
        self.helper.form_style = 'inline'
        self.helper.label_class = 'label'
        self.helper.field_class = 'input'

        self.helper.layout = Layout(
            Fieldset(
                'Registrieren',
                'email',
                'username',
                'password_one',
                'password_two',
                ButtonHolder(
                    Submit('submit', 'Senden')
                )
            )
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Die Email-Adresse wird bereits genutzt.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(name=username).exists():
            raise forms.ValidationError("Der Name ist bereits vergeben.")
        return username

    def clean(self):
        form_data = self.cleaned_data
        if form_data['password_one'] != form_data['password_two']:
            self._errors["password_one"] = ["Die Passwörter stimmen nicht überein."]
            self._errors["password_two"] = ["Die Passwörter stimmen nicht überein."]
            del form_data['password_one']
            del form_data['password_two']
        else:
            form_data['password'] = form_data['password_one']
            del form_data['password_one']
            del form_data['password_two']
        return form_data


class NewPasswordForm(forms.Form):
    password_one = forms.CharField(label="Passwort", widget=forms.PasswordInput, min_length=8)
    password_two = forms.CharField(label="Passwort wiederholen", widget=forms.PasswordInput,
                                   min_length=8)
    uid = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = 'register'
        self.helper.form_style = 'inline'
        self.helper.label_class = 'label'
        self.helper.field_class = 'input'

        self.helper.layout = Layout(
            Fieldset(
                'Neues Passwort',
                'password_one',
                'password_two',
                'uid',
                ButtonHolder(
                    Submit('submit', 'Senden')
                )
            )
        )

    def clean(self):
        form_data = self.cleaned_data
        if form_data['password_one'] != form_data['password_two']:
            self._errors["password_one"] = ["Die Passwörter stimmen nicht überein."]
            self._errors["password_two"] = ["Die Passwörter stimmen nicht überein."]
            del form_data['password_one']
            del form_data['password_two']
        else:
            form_data['password'] = form_data['password_one']
            del form_data['password_one']
            del form_data['password_two']
        return form_data
