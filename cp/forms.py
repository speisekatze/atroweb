from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms


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
