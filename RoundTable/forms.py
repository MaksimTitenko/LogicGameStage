from django import forms
from django.forms import ModelForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': 'Логин',
            'password': 'Пароль'
        }

        widgets = {
            'password':forms.PasswordInput()
        }

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с данным логином уже есть в системе!')

        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль!')



# class RegistrationForm(forms.ModelForm):
#     # password = forms.CharField(widget=forms.PasswordInput)
#     # password_check = forms.CharField(widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'first_name',
#             'last_name',
#             'email',
#             'country',
#             'city',
#             'phone',
#             'password',
#             'password_check',
#         )
#         labels = {
#             'username':'Логин',
#             'first_name':'Имя',
#             'last_name':'Фамилия',
#             'email':'Электронная почта',
#             'country':'Страна',
#             'city':'Город',
#             'phone':'Телефон',
#             'password':'Пароль',
#             'password_check':'Повторите пароль',
#         }
#
#
#         help_texts = {
#             'password':'Придумайте пароль',
#             'email':''
#         }
#
#         widgets = {
#             'password':forms.PasswordInput(),
#             'password_check':forms.PasswordInput()
#         }
#
#     def clean(self):
#         username = self.cleaned_data['username']
#         password = self.cleaned_data['password']
#         password_check = self.cleaned_data['password_check']
#         email = self.cleaned_data['email']
#
#
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError({
#                 'username': 'Пожалуйста выберите другое имя пользователя, т.к. пользователь с таким логином уже зарегистрирован в системе!'},
#                 code='user exists')
#
#         if password != password_check:
#             raise forms.ValidationError({
#                 'password': '',
#                 'password_check': 'Вы ошиблись при вводе паролей, они не совпадают, введите повторно!'},
#                 code='passwords do not match', )
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError({'email': 'Пользователь с таким email уже зарегистрирован!'},
#                                         code='email exists')


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_check',
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].help_text = 'Придумайте пароль'
        self.fields['password_check'].label = 'Повторите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['email'].label = 'Ваш email'
        self.fields['email'].help_text = 'Пожалуйста, указывайте реальный адрес'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({
                'username': 'Пожалуйста выберите другое имя пользователя, т.к. пользователь с таким логином уже зарегистрирован в системе!'},
                code='user exists')

        if password != password_check:
            raise forms.ValidationError({
                'password': '',
                'password_check': 'Вы ошиблись при вводе паролей, они не совпадают, введите повторно!'},
                code='passwords do not match', )
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError({'email': 'Пользователь с таким email уже зарегистрирован!'},
                                        code='email exists')