from rest_framework import generics
from .models import WebUser
from .serializers import WebUserSerializer

class APIUserSearchList(generics.ListAPIView):
    serializer_class = WebUserSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return WebUser.objects.filter(username__icontains=query)[:5]
        return WebUser.objects.none()