from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Teacher, Student


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].label = ''
        self.fields['username'].label = ''
        self.fields['moderate'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Номер телефона (+996)'
        self.fields['username'].widget.attrs['placeholder'] = 'Имя пользователя'
        self.fields['moderate'].widget.attrs['placeholder'] = 'Класс'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторно введите пароль'

    password1 = forms.CharField(label='Введите паорль',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль',
                                widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = ("phone_number", "username", "moderate", "item_name", "password1", "password2")


class UserAuthenticationForm(forms.Form):
    phone_number = forms.CharField(label='Введите номер телефона',
                                   widget=forms.TextInput(attrs={'placeholder': '+996'}))

    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = ("phone_number", "password")


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('full_name', 'mail', 'date_of_birth', 'classroom', 'address', 'gender', 'image')





