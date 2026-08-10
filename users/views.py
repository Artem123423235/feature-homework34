from rest_framework import generics

from users.models import User
from users.serializers import UserProfileSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
