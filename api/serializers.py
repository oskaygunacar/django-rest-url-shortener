from rest_framework import serializers
from shortener.models import Url

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = '__all__'
        read_only_fields = ('profile','view_count')