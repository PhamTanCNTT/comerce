from rest_framework import viewsets, generics, mixins
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework.response import Response

from addressgojoco.models import *
from addressgojoco.serializers import *
from django.contrib.auth import get_user_model

User = get_user_model()


################################ Address ######################################

################################ Country ######################################

class IsCountry(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserIDCountry == request.user


class CountryViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CountrySerializer
    permission_classes = (IsCountry, IsAdminUser,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Country.objects.filter(UserIDCountry=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(UserIDCountry=self.request.user)


class CountryList(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serilizer = CountrySerializer(queryset, many=True)
        return Response(serilizer.data, status=200)


class CountryDetail(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return Country.objects.get(id=id)
        except Country.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = CountrySerializer(instance)
        return Response(serailizer.data)


################################ Country ######################################

############################# ProvinceCity ####################################

class IsProvinceCity(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserIDProvinceCity == request.user


class ProvinceCityViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProvinceCitySerializer
    permission_classes = (IsProvinceCity, IsAdminUser,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ProvinceCity.objects.filter(UserIDProvinceCity=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(UserIDProvinceCity=self.request.user)


class ProvinceCityList(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProvinceCitySerializer
    queryset = ProvinceCity.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serilizer = ProvinceCitySerializer(queryset, many=True)
        return Response(serilizer.data, status=200)


class ProvinceCityDetail(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ProvinceCity.objects.all()
    serializer_class = ProvinceCitySerializer

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return ProvinceCity.objects.get(id=id)
        except ProvinceCity.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = ProvinceCitySerializer(instance)
        return Response(serailizer.data)


############################# ProvinceCity ####################################

############################### District ######################################

class IsDistrict(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserIDDistrict == request.user


class DistrictViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = DistrictSerializer
    permission_classes = (IsDistrict, IsAdminUser,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return District.objects.filter(UserIDDistrict=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(UserIDDistrict=self.request.user)


class DistrictList(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = DistrictSerializer
    queryset = District.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serilizer = DistrictSerializer(queryset, many=True)
        return Response(serilizer.data, status=200)


class DistrictDetail(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return District.objects.get(id=id)
        except ProvinceCity.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = DistrictSerializer(instance)
        return Response(serailizer.data)


############################### District ######################################

################################# Ward ########################################

class IsWard(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserIDWard == request.user


class WardViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = WardSerializer
    permission_classes = (IsWard, IsAdminUser,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Ward.objects.filter(UserIDWard=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(UserIDWard=self.request.user)


class WardList(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = WardSerializer
    queryset = Ward.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serilizer = WardSerializer(queryset, many=True)
        return Response(serilizer.data, status=200)


class WardDetail(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Ward.objects.all()
    serializer_class = WardSerializer

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return Ward.objects.get(id=id)
        except Ward.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = WardSerializer(instance)
        return Response(serailizer.data)


################################# Ward ########################################

############################## End Address ####################################

############################## LanguageUser ####################################

class IsLanguageUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserIDLanguage == request.user


class LanguageUserViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = LanguageUserSerializer
    permission_classes = (IsLanguageUser, IsAdminUser,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return LanguageUser.objects.filter(UserIDLanguage=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(UserIDLanguage=self.request.user)


# ############################# LanguageUser ####################################

# ############################### MainCareer ######################################

class IsMainCareer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserIDMainCareer == request.user


class MainCareerViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = MainCareerSerializer
    permission_classes = (IsMainCareer, IsAdminUser,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return MainCareer.objects.filter(UserIDMainCareer=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(UserIDMainCareer=self.request.user)


# ############################### Level1Career ######################################

class IsLevel1Career(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserIDLevel1Career == request.user


class Level1CareerViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = Level1CareerSerializer
    permission_classes = (IsLevel1Career, IsAdminUser,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Level1Career.objects.filter(UserIDLevel1Career=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(UserIDLevel1Career=self.request.user)


# ############################### Level2Career ######################################

class IsLevel2Career(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserIDLevel2Career == request.user


class Level2CareerViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = Level2CareerSerializer
    permission_classes = (IsLevel2Career, IsAdminUser,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Level2Career.objects.filter(UserIDLevel2Career=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(UserIDLevel2Career=self.request.user)


# ############################### Level3Career ######################################

class IsLevel3Career(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserIDLevel3Career == request.user


class Level3CareerViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = Level3CareerSerializer
    permission_classes = (IsLevel3Career, IsAdminUser,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Level3Career.objects.filter(UserIDLevel3Career=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(UserIDLevel3Career=self.request.user)
