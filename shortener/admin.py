from django.contrib import admin
from shortener.models import Url


@admin.register(Url)
class UrlModelAdmin(admin.ModelAdmin):
    list_display = ["base_url", 'shortened_slug', 'profile']