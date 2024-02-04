from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Tweet


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Логин",
                "class": "input",
                "type": "text",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Пароль",
                "class": "input",
                "type": "password",
                "autocomplete": "off",
            }
        ),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Логин",
                "class": "input",
                "type": "text",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Пароль",
                "class": "input",
                "type": "password",
                "autocomplete": "off",
            }
        ),
    )


class TweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Твитните что-нибудь",
                "class": "textarea is-success is-medium",
            }
        ),
        label="",
    )

    class Meta:
        model = Tweet
        exclude = ("user",)
