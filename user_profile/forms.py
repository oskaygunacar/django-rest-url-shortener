from django import forms
from user_profile.models import Profile

class UserInfoUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'avatar', 'info',
        ]