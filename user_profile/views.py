from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.contrib.auth.models import User

from shortener.models import Profile, Url

from rest_framework.authtoken.models import Token

#Class Based Views
from django.views.generic import DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin


# Forms

from user_profile.forms import UserInfoUpdateForm

## Profile Views

# Profile detail
class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = Profile
    login_url = reverse_lazy('account:login_view')
    template_name = 'user_profile/profile-detail.html'
    context_object_name = 'profile'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urls'] = Url.objects.filter(profile=self.request.user.profile)
        context['token'] = Token.objects.get(user=self.request.user)
        return context

    def get_object(self):
        return get_object_or_404(Profile,slug=self.kwargs.get('profile_slug'), user=self.request.user)
    

# Profile Info Update
class ProfileInfoUpdateView(LoginRequiredMixin,FormView):
    login_url = reverse_lazy('account:login_view')
    template_name = 'registration/form.html'
    form_class = UserInfoUpdateForm
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Update {self.request.user.username} Profile Info'
        context['button_info'] = 'Update'
        return context

    def get_form(self):
        if self.request.method == 'GET':
            form = UserInfoUpdateForm(instance=Profile.objects.get(user=self.request.user))
        else:
            form = UserInfoUpdateForm(self.request.POST, self.request.FILES or None, instance=Profile.objects.get(user=self.request.user))
        return form
    
    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy('user_profile:profile_detail_view', kwargs={'profile_slug':self.request.user.profile.slug}))


# Dashboard
@login_required(login_url=reverse_lazy('account:login_view'))
def dashboard_view(request):
    """
    Creates dashboard with Urls that created by authenticated user.
    """
    if request.GET.get('page') and request.GET.get('page') == '1':
        return redirect('user_profile:dashboard_view',permanent=True)
    profile = get_object_or_404(Profile, user=request.user)
    urls = Url.objects.filter(profile=profile) #queryset
    paginator = Paginator(urls, 20)
    page_number = request.GET.get('page')
    paginated_urls = paginator.get_page(page_number) 
    context = dict(urls=paginated_urls, profile=profile)
    return render(request, 'user_profile/dashboard.html', context=context)