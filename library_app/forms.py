from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), css_class='form-control')
    password = forms.CharField(widget=forms.PasswordInput(), css_class='form-control')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-loginform'
        self.helper.form_show_labels = False
        self.helper.form_method = 'post'
        self.helper.form_action = 'account_login'
        self.helper.layout = Layout(
            'username',
            'password',
            StrictButton('Sign in', css_class='btn btn-lg btn-primary btn-block'),
        )


class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), css_class='form-control',
                               required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}), css_class='form-control',
                             required=True)
    password = forms.CharField(widget=forms.PasswordInput(), css_class='form-control', required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), css_class='form-control', required=True)

    class Meta:
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "passwords do not match"
            )

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-signupform'
        self.helper.form_show_labels = False
        self.helper.form_method = 'post'
        self.helper.form_action = 'account_signup'
        self.helper.layout = Layout(
            'username',
            'email',
            'password',
            'confirm_password',
            StrictButton('Sign up', css_class='btn btn-lg btn-primary btn-block'),
        )
