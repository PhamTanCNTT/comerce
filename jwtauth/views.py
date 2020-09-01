from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework import response, decorators, permissions, status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserCreateSerializer, UserCreateSerializerSocial, ProfileFullSerializer, UserUpdateSerializer, \
    ProfileAddressFullSerializer, ProfileImageSerializer
from rest_framework.response import Response

from rest_framework.exceptions import PermissionDenied

from connectdata.models import Profile
User = get_user_model()

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    res = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return response.Response(res, status.HTTP_201_CREATED)

################ Update User #########################

class UserUpdateSerializerDetail(APIView):

    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return User.objects.get(id=id)
        except User.DoesNotExist as e:
            return Response( {"error": "Given question object not found."}, status=404)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return User.objects.filter(id=user.id)
        raise PermissionDenied()

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = UserUpdateSerializer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = UserUpdateSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


################ Update User #########################

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def registrationsocial(request):
    serializer = UserCreateSerializerSocial(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    res = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return response.Response(res)



######### User call Web ###############
from django.shortcuts import render

# Create your views here.

def loginsocial(request):
    return render(request, "jwtauth/loginsocial.html")

def loginallauth(request):
    return render(request, "account/login.html")
def signallauth(request):
    return render(request, "account/signup.html")

def xoa(request):
    return render(request, "jwtauth/xoa.html")
class IsProfilefull(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.userprofile == request.user

class ProfileFullViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileFullSerializer
    permission_classes = (IsProfilefull,)

    # Ensure a user sees only own Note objects.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Profile.objects.filter(UserProfile=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserProfile=self.request.user)

class ProfileFullViewAll(ListAPIView):
    #permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileFullSerializer
    def get(self, request):
        queryset = self.get_queryset()
        serializer = ProfileFullSerializer(queryset, many=True)
        return Response(serializer.data)

################################ Token User#####################################

# UserToken - nut upload img
class IsProfileUserToken(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserProfile == request.user


class ProfileUserViewSetToken(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProfileImageSerializer
    permission_classes = (IsProfileUserToken,)

    # Ensure a user sees only own Note objectsu.

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Profile.objects.filter(UserProfile=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.

    def perform_create(self, serializer):
        serializer.save(UserProfile=self.request.user)


# create address
class ProfileViewSet(viewsets.ModelViewSet):
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProfileAddressFullSerializer
    permission_classes = (IsProfilefull,)

    # Ensure a user sees only own Note objects.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Profile.objects.filter(UserProfile=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserProfile=self.request.user)

################################ Token User#####################################


def registeruser(request):
    return render(request, "jwtauth/registeruser.html")

def checkfunc(request):
    return render(request, "jwtauth/check_func.html")

def GJC_Login(request):
    return render(request, "jwtauth/GJC_Login.html")

