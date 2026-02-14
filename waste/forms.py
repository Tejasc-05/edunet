from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import WasteReport, WasteCategory

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control'
        })
    )


class SignUpForm(UserCreationForm):
    name = forms.CharField(
        max_length=100,
        label='Full Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your full name',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['name'].split()[0]
        user.last_name = ' '.join(self.cleaned_data['name'].split()[1:])
        if commit:
            user.save()
        return user


class WasteReportForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=WasteCategory.objects.all(),
        empty_label='Select waste category',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = WasteReport
        fields = ('category', 'quantity', 'location', 'notes')
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'placeholder': 'Enter quantity in kg',
                'class': 'form-control',
                'step': '0.01'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Enter location',
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'placeholder': 'Add any additional notes',
                'class': 'form-control',
                'rows': 3
            })
        }
