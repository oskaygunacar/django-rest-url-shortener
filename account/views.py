from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import authenticate,login,logout


from shortener.models import Url
from user_profile.models import Profile
from django.views.generic import View, FormView

from account.forms import UserSignupForm,UserLoginForm, UserChangePasswordForm, UserDeleteForm


## Authentication Views

#Signup
def signup_view(request):
    form = UserSignupForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data['password']
        email = form.cleaned_data.get('email')
        email_control = User.objects.filter(email=email) if email else None # Without overriding default User Model, i coded this extra control to have email uniqueness.
        if email_control:
            messages.warning(request, 'This email is already in use. Please use another mail')
            context = dict(form=form, page_title='Signup', button_info='Register')
            return render(request, 'registration/form.html', context=context)
        user = form.save(commit=False)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user)
        messages.success(request, 'Your account created succesfully.')
        return redirect('shortener:homepage')
    context = dict(form=form, page_title='Signup', button_info='Register')
    return render(request, 'registration/form.html', context=context)

# Login (Class Based)
class LoginFormView(FormView):
    template_name = 'registration/form.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('shortener:homepage')

    def get_context_data(self, **kwargs): # get_context_data override
        context = super(LoginFormView,self).get_context_data() # to get context dictionary
        context['page_title'] = 'Login'
        context['button_info'] = 'Login'
        return context

    def get(self, request):
        if self.request.user.is_authenticated: # if user somehow find and clicks login URL this code block works. Just an extra control.
            if self.request.META.get('HTTP_REFERER'):
                return redirect(self.request.META.get('HTTP_REFERER')) # Redirect users wherever they come
            messages.success('You are already logged in.')
            return redirect('shortener:homepage')
        else:
            context = self.get_context_data()
            return render(request, self.template_name, context)


    def form_valid(self, form): #POST
       username = form.cleaned_data.get('username')
       password =  form.cleaned_data['password']
       user = authenticate(self.request, username=username, password=password)
       if user is not None:
           login(self.request,user)
           messages.success(self.request, f'Succesfully logged in {username}')
           if self.request.GET.get('next'):
               return redirect(self.request.GET.get('next'))
           return super(LoginFormView, self).form_valid(form)
       messages.warning(self.request, 'User not found')
       return render(self.request, self.template_name, self.get_context_data())


# Logout
class LogoutFormView(LoginRequiredMixin, View):
    login_url = reverse_lazy('account:login_view')
    http_method_names = ['get']

    def get(self, request):
        if request.user.is_authenticated: #extra authentication control
            logout(request)
            messages.success(request, 'You are succesfully logged out.')
            return redirect('shortener:homepage')


# User Password Change
@login_required(login_url=reverse_lazy('account:login_view'))
def change_password_view(request):
    form = UserChangePasswordForm(request.POST or None)
    if form.is_valid():
        user = authenticate(username=request.user.username, password=form.cleaned_data.get('old_password'))
        if user:
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            messages.success(request,'Your password is succesfully changed.')
            return redirect('account:login_view')
        # We take username directly from request, if old password is not correct the below code block works, sends a message to user and renders same page with user's form data.
        messages.warning(request, f'Old password is not correct for user: {request.user.username}. Please check and try again.')
        context = dict(form=form, page_title='Change Password', button_info='Change Password')
        return render(request, 'registration/form.html', context=context)
    context = dict(form=form, page_title='Change Password', button_info='Change Password')
    return render(request, 'registration/form.html', context=context)

# Delete User - Account
class DeleteAccountView(LoginRequiredMixin,FormView):
    login_url = reverse_lazy('account:login_view')
    template_name = 'registration/delete-account.html'
    form_class = UserDeleteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Delete Account'
        context['validation_data'] = self.request.user.username
        context['button_info'] = 'Delete'
        self.request.session['validation_data'] = self.request.user.username
        return context

    def form_valid(self, form): # POST
         user = get_object_or_404(User, username=self.request.user.username)
         delete_validation_data = form.cleaned_data.get('delete_account_validation')
         if delete_validation_data == self.request.session.get('validation_data'):
             user.delete()
             messages.success(self.request,'Account Deleted!')
             return redirect('account:signup_view')