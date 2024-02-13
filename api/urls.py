
from django.urls import path
from api import views

from rest_framework.authtoken.views import obtain_auth_token


app_name = 'api'

urlpatterns = [
    path('token/',obtain_auth_token, name='api_get_or_create_token_view'),
    path('list/',views.urlListView.as_view(), name='list_all_urls_view'),
    path('create/', views.urlCreateView.as_view(), name='create_api_view'),
    path('detail/<int:id>/', views.APIDetailView.as_view(), name="detail_api_view"),
    path('delete/<int:id>/', views.APIDeleteView.as_view(), name='delete_api_view')
]