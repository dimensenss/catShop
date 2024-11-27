from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator

from users.validators import validate_email


class RegisterUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']

        if commit:
            user.save()
        return user

    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zА-Яа-я]+$',
                message="Ім'я повинно містити тільки літери."
            )
        ]
    )
    last_name = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zА-Яа-я]+$',
                message="Прізвище повинно містити тільки літери."
            )
        ]
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[
            MinLengthValidator(8, message="Пароль повинен містити не менше 8 символів."),
        ],
        help_text="Ваш пароль повинен містити щонайменше 8 символів."
    )
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        validate_email(email, self)
        if User.objects.filter(email=email).exists():
            raise ValidationError("Користувач з такою електронною адресою вже існує.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Користувач з таким ім'ям вже існує.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Паролі не співпадають.")

        return password2

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("Ім'я повинно містити тільки літери.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError("Прізвище повинно містити тільки літери.")
        return last_name

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(error_messages={'required': 'Це поле обов\'язкове.'})
    password = forms.CharField(error_messages={'required': 'Це поле обов\'язкове.'})

    class Meta:
        model = User
        fields = ('username', 'password')
