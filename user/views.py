from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework.views import APIView

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class LogOutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = get_object_or_404(Token, user=request.user)
        token.delete()
        return Response({"detail": "Succesfully log out"}, status=status.HTTP_200_OK)
