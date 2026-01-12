from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, FastingRecord, WeightRecord


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'})
    )
    fasting_goal_hours = forms.FloatField(
        initial=16.0,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Meta de jejum (horas)', 'step': '0.5'})
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'})
    )
    password2 = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar senha'})
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'fasting_goal_hours', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'})
    )


class FastingRecordForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_time = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = FastingRecord
        fields = ['start_time', 'end_time', 'fasting_type', 'energy_level', 'focus_level', 'mood_level', 'notes']
        widgets = {
            'fasting_type': forms.Select(attrs={'class': 'form-select'}),
            'energy_level': forms.Select(attrs={'class': 'form-select'}),
            'focus_level': forms.Select(attrs={'class': 'form-select'}),
            'mood_level': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 255}),
        }


class WeightRecordForm(forms.ModelForm):
    class Meta:
        model = WeightRecord
        fields = ['weight', 'reference_month']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Peso (kg)'}),
            'reference_month': forms.TextInput(attrs={'class': 'form-control', 'type': 'month', 'placeholder': 'YYYY-MM'}),
        }
