from django import forms
from auth_app.models import MesUser

class SignInForm(forms.ModelForm):

    password_confirm = forms.CharField(min_length=4, max_length=20, required=True,
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))

    class Meta:

        model = MesUser

        fields = ('username', 'first_name', 'second_name', 'email', 'birth_place', 'birth_date',
                  'avatar', 'password', 'password_confirm')
        
        widgets = {
            'username': forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
            'first_name': forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'second_name': forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': forms.widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Эллектронный адрес'}),
            'birth_place': forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Место рождения'}),
            'birth_date': forms.widgets.DateInput(attrs={'class': 'form-control', 'placeholder': 'Дата рождения'}),
            'avatar': forms.widgets.FileInput(attrs={'class': 'form-control', 'placeholder': 'Аватар'}),
            'password': forms.widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
        }

    def clean_password_confirm(self):

        print('-------------\n{}\n-------------'.format(self.cleaned_data))

        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError('{}, {}'.format(password, password_confirm))

        return self.cleaned_data

    def save(self):

        user = super(SignInForm, self).save(commit=False)
        user.save()

        return user

class LogInForm(forms.Form):

    username = forms.CharField(widget=forms.widgets.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Пароль'}))
