from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError
from shortener.models import Url, Profile

class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Please enter your password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']



class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Please enter your password'}))
    confirm_password= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Please write your password again for confirmation'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    
    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords are not identical. Please try again.')
        
        return self.cleaned_data
    

    
class UserChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Please write your current password'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Please write your new password'}))

    def clean(self):
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')

        if old_password and new_password and old_password == new_password:
            raise ValidationError('Please do not use the same password with your old password. Change the new password and try again.')
        elif len(new_password) < 5:
            raise ValidationError('Your password should be at least 5 character long.')
        
        return self.cleaned_data
    

class UserDeleteForm(forms.Form):
    delete_account_validation = forms.CharField()
    
