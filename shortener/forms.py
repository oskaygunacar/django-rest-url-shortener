from django import forms
from shortener.models import Url
from django.forms import ValidationError

class UrlForm(forms.ModelForm):

    base_url = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter the link here'}))

    class Meta:
        model = Url
        fields = ['base_url',]

class PremiumUrlForm(forms.ModelForm):
    base_url = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Please write your URL to be shortened'}))
    shortened_slug = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Please write the url slug that you want to use as shortened URL'}))
    
    class Meta:
        model = Url
        fields = ['base_url', 'shortened_slug']

    
    def clean_shortened_slug(self):
        slug = self.cleaned_data.get("shortened_slug")

        if slug and len(slug) > 25:
            raise ValidationError('Shortened url can not be longer than 25 character.')
        
        return slug

