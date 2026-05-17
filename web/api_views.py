from rest_framework import generics
from .models import WebUser, Country
from .serializers import WebUserSerializer, CountrySerializer


class APIUserSearchList(generics.ListAPIView):
    serializer_class = WebUserSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return WebUser.objects.filter(username__icontains=query)[:5]
        return WebUser.objects.none()


class APICountrySearchList(generics.ListAPIView):
    serializer_class = CountrySerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return Country.objects.filter(country_name__icontains=query)[:10]
        return Country.objects.none()
