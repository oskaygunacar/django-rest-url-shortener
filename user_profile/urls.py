
from django.urls import path
from user_profile import views

app_name = 'user_profile'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name="dashboard_view"),
    path('update-profile/', views.ProfileInfoUpdateView.as_view(), name="profile_update_view"),
    path('<slug:profile_slug>/', views.ProfileDetailView.as_view(), name="profile_detail_view"),
]