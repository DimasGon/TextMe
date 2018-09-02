from django import forms
from auth_app.models import MesUser

class AccountUpdateForm(forms.ModelForm):

    class Meta:

        model = MesUser

        fields = ('first_name', 'second_name', 'email', 'birth_place', 'birth_date', 'avatar')
        
        widgets = {
            'first_name': forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'second_name': forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': forms.widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Эллектронный адрес'}),
            'birth_place': forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Место рождения'}),
            'birth_date': forms.widgets.DateInput(attrs={'class': 'form-control', 'placeholder': 'Дата рождения'}),
            'avatar': forms.widgets.FileInput(attrs={'class': 'form-control', 'placeholder': 'Аватар'}),
        }