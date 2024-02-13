# class based views
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView

# permissions
from rest_framework import permissions
from .permissions import APIViewPermission, APICreatePermission

# Serializer
from .serializers import URLSerializer

# models
from shortener.models import Url

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status


# List Objects View
class urlListView(ListAPIView):
    serializer_class = URLSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, APIViewPermission]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user.profile.api_view -= 1
        user.profile.save()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return Url.objects.filter(profile=user.profile)
    
class urlCreateView(CreateAPIView):
    serializer_class = URLSerializer
    permission_classes = [permissions.IsAuthenticated, APICreatePermission]
    
    def perform_create(self, serializer):
        serializer.save(profile = self.request.user.profile)
        profile = self.request.user.profile
        profile.api_create -= 1
        profile.save()

# Detail View
class APIDetailView(RetrieveAPIView):
    serializer_class = URLSerializer
    queryset = Url.objects.all()
    lookup_field = 'id'

    permission_classes = [permissions.IsAuthenticated, APIViewPermission]

    
    def get_object(self):
        id = self.kwargs.get('id')
        url = Url.objects.filter(pk=id, profile=self.request.user.profile).first()
        if url is None:
            raise NotFound({'info':'Object does not exist.'})
        profile = self.request.user.profile
        profile.api_view -=1
        profile.save()
        return url

# Delete Object View
class APIDeleteView(DestroyAPIView):
    queryset = Url.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id, format=None):
        profile = request.user.profile
        url_to_delete = Url.objects.filter(pk=id, profile=profile).first()
        if not url_to_delete:
            return Response({'Info':'The URL that you are trying to delete is not found!'}, status=status.HTTP_404_NOT_FOUND)
        url_to_delete.delete()
        return Response({'message': 'Object Succesfully Deleted!'}, status=status.HTTP_200_OK)
    

# this is not getting used.
class APIUpdateView(UpdateAPIView):
    queryset = Url.objects.all()
    lookup_field = 'id'
    serializer_class = URLSerializer
    permission_classes = [permissions.IsAuthenticated, APICreatePermission]

    def update(self, request, *args, **kwargs):
        profile = request.user.profile
        id = kwargs.get('id')
        obj = Url.objects.filter(pk=id, profile=profile).first()
        if not obj:
            return Response({'Info':'The object that you are trying to update is not found!'}, status=status.HTTP_404_NOT_FOUND)
        profile.api_create -= 1
        profile.save()
        return super().update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        serializer.save()