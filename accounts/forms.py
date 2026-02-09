from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from accounts.models import UserProfile


class CustomSignupForm(SignupForm):
    """Custom signup form with additional fields."""
    first_name = forms.CharField(
        label='First Name',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile."""
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'preferred_currency']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'preferred_currency': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3'}),
        }


class UserEditForm(forms.ModelForm):
    """Form for editing user information."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
