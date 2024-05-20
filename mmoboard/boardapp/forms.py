from django import forms
from django.core.validators import FileExtensionValidator
from .models import *


class MultipleFileInput(forms.ClearableFileInput):  #взято с документации по джанго по добавлению нескольких файлов
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class AddForm(forms.ModelForm):
    files = MultipleFileField(required=False, validators=[FileExtensionValidator(allowed_extensions=['png', 'mp4'])], help_text='only png and mp4')

    class Meta:
        model = Post
        fields = ['title', 'category', 'text']


class AddReply(forms.ModelForm):
    class Meta:
        model = PostReply
        fields = ['text_reply']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class RegForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    def clean(self):
        if User.objects.filter(email=self.cleaned_data.get('email')):  #проверяем есть ли в базе такой email
            raise forms.ValidationError('This email already in use.')
        if User.objects.filter(username=self.cleaned_data.get('username')):  #проверяем есть ли в базе такой username
            raise forms.ValidationError('This username already in use.')
        pass1 = self.cleaned_data.get('password')  #проверка совпадения пароля
        pass2 = self.cleaned_data.get('password_confirm')
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('Password do not match')
        return pass2


class VerifyForm(forms.Form):
    confirm_code = forms.CharField(label='Code of verification', max_length=6)

