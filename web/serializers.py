from rest_framework import serializers
from .models import WebUser, Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_id', 'country_name', 'country_iso', 'flag_image']


class WebUserSerializer(serializers.ModelSerializer):
    user_country = CountrySerializer(read_only=True)

    class Meta:
        model = WebUser
        fields = ['username', 'user_image', 'user_country']