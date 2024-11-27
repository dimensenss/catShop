import re

from django import forms
from django.contrib.auth.models import User


def validate_email(email, user=None):
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) and len(email) > 254:
        raise forms.ValidationError("Некоректний формат email адреси")
    if user:
        if User.objects.filter(email=email).exists() and user.instance.email != email:
            raise forms.ValidationError("Користувач з такою адресою електронної пошти вже існує")