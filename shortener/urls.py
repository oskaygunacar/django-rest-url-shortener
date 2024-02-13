from django.urls import path, include
from shortener import views
from django.views.generic import RedirectView

app_name = 'shortener'

urlpatterns = [
    path("", views.url_shortener, name="homepage"),
    path('premium-url-shortener/', views.premium_url_shortener, name="premium_url_shortener"),
    path('<slug:shortened_slug>/', views.Redirecter.as_view(), name="redirecter_view"),
]