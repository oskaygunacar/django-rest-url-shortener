from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate,login,logout

# Models
from shortener.models import Url, Profile

# Forms
from shortener.forms import UrlForm, PremiumUrlForm

#class based view
from django.views.generic import View, FormView

# Main View
class Redirecter(View):
    help = """Simply redirects the shortened_url to base_url (original source url)"""

    http_method_names = ['get']

    def get(self, request, shortened_slug):
        url_obj = get_object_or_404(Url, shortened_slug=shortened_slug)
        url_obj.view_count += 1
        url_obj.save()
        return redirect(url_obj.base_url)


# homepage url shortener
def url_shortener(request):
    form = UrlForm(request.POST or None)
    page_title = 'URL Shortener'
    if form.is_valid():
        url = form.save(commit=False)
        if request.user.is_authenticated:
            url.profile = request.user.profile
            url.save()
        context = dict(form=form, url=url, page_title=page_title)
        return render(request, 'shortener/homepage.html', context=context)
    context = dict(form=form, page_title=page_title)
    return render(request, 'shortener/homepage.html', context=context)

# Url shortener for Premium Users.
def premium_url_shortener(request):
    """
    By using this view premium users can create customized URL slugs as shortened_urls.
    """

    form = PremiumUrlForm(request.POST or None)
    if form.is_valid():
        url = form.save(commit=False)
        url.profile = request.user.profile
        url.save()
        context = dict(form=form, url=url, page_title='Premium URL Shortener')
        return render(request, 'shortener/homepage.html', context=context)
    context = dict(form=form, page_title='Premium URL Shortener')
    return render(request, 'shortener/homepage.html', context=context)