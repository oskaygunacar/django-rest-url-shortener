from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path("signup/", views.signup_view, name="signup_view"),
    path('login/', views.LoginFormView.as_view(), name="login_view"),
    path('logout/', views.LogoutFormView.as_view(), name="logout"),
    path('delete-account/', views.DeleteAccountView.as_view(), name="delete_account_view"),
    path('change-password/', views.change_password_view, name="change_password"),
]