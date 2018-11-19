from django import forms
from django.forms import ModelForm
from .models import User, TeamMod

SEX_CHOICES = (
    ('Мужчина', u"Мужчина"),
    ('Женщина', u"Женщина"),
)

COUNTRIES = (
    ('Беларусь', 'Беларусь'),
    ('Россия', 'Россия'),
    ('Украина', 'Украина')
)


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': 'Логин',
            'password': 'Пароль'
        }

        widgets = {
            'password': forms.PasswordInput()
        }

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с данным логином уже есть в системе!')

        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль!')


class RegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password_check',
            'first_name',
            'last_name',
            'middle_name',
            'gender',
            'date_birth',
            'phone',
            'avatar',
            'bio',
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].help_text = 'Придумайте пароль'
        self.fields['password_check'].label = 'Повторите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['email'].label = 'Эл.почта'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']

        if User.objects.filter(username=username).exists():
            self.add_error(None, 'Пользователь с таким логином уже есть в системе!')

        if password != password_check:
            self.add_error(None, 'Пароли не совпадают!')

        if User.objects.filter(email=email).exists():
            self.add_error(None, 'Пользователь с таким email уже зарегистрирован!')


class CreateTeamForm(forms.Form):
    team_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = TeamMod
        fields = [
            'team_name',
        ]

    def __init__(self, *args, **kwargs):
        super(CreateTeamForm, self).__init__(*args, **kwargs)
        self.fields['team_name'].label = 'Введите название пространства'
        self.fields['team_name'].help_text = 'Должно быть уникально'

    def clean(self):
        team_name = self.cleaned_data['team_name']
        if TeamMod.objects.filter(team_name=team_name).exists():
            self.add_error(None, 'Команда с таким именем уже существует')


