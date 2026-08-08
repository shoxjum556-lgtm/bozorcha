from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from users.models import User, Profile
from .serializers import UserRegisterSerializer, ProfileDetailSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

class ProfileDetailView(RetrieveUpdateAPIView):
    serializer_class = ProfileDetailSerializer
    http_method_names = ["get", "patch"]

    def get_object(self):
        return Profile.objects.filter(user=self.request.user).last()
