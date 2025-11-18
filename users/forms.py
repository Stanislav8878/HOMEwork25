from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)

from .models import User


class UserRegisterForm(UserCreationForm):
    """
    Форма регистрации: email + пароль + доп. поля профиля.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'avatar',
            'phone',
            'country',
        )


class UserLoginForm(AuthenticationForm):
    """
    Форма логина по email и паролю.
    """

    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(forms.ModelForm):
    """
    Форма редактирования профиля пользователя.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'avatar',
            'phone',
            'country',
        )
