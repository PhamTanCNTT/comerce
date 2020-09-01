from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, generics, mixins
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from Employer.serializers import *
from addressgojoco.serializers import CountrySerializer, ProvinceCitySerializer, DistrictSerializer, WardSerializer
from .FilterBackend import AddressFilterBackend, AddressSearchFilter
from .models import *
from .serializers import *
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import filters

###########################Nested 07/07/2020#######################

from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Course
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from jwtauth.serializers import *


###########################Nested 07/07/2020#######################

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = (IsOwner,)

    # Ensure a user sees only own Note o34bjects.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Note.objects.filter(owner=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ConnectViewAll(ListAPIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = NoteSerializer(queryset, many=True)
        return Response(serializer.data)


###########################Nested 07/07/2020#######################

class AccountEditView(UpdateView):
    template_name = 'account.html'
    model = User
    fields = ('first_name', 'last_name', 'middle_name', 'year_birth', 'about', 'date_updated', 'UserIDC')
    success_url = reverse_lazy('account')

    def get_object(self, queryset=None):
        return self.request.user


def client(request):
    return render(request, "connectdata/rest_client.html")


def client_ajax(request):
    return render(request, "connectdata/test_ajax.html")


@api_view(['GET', 'DELETE', 'PUT'])
def course_details(request, pk):
    try:
        course = Course.objects.get(IDC=pk)
    except:
        return Response(status=404)
    if request.method == 'GET':
        serializer = CourseComSerializer(course)
        return Response(serializer.data)
    elif request.method == 'PUT':  # Update
        serializer = CourseComSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Update table in DB
            return Response(serializer.data)

        return Response(serializer.errors, status=400)  # Bad request
    elif request.method == 'DELETE':
        course.delete()
        return Response(status=204)


# Get lồng
class GetInnerCourseComView(APIView):
    def get(self, request):
        course = Course.objects.all()
        datacourse = CourseComSerializer(course, many=True)
        return Response(datacourse.data)


# post long test
class PostCourseComView(CreateAPIView):
    serializer_class = CompanyPostSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# view detail long
class DetailCourseComView(APIView):

    def get_object(self, id):
        try:
            return Course.objects.get(id=id)
        except Course.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, pk):
        try:
            course = Course.objects.get(IDC=pk)
        except:
            return Response(status=404)
        serializers = CourseComSerializer(course)
        return Response(serializers.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = CourseCompanySerializerLib(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.erros, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


# view chay api cua sep

# List title
class ListUserAPIView(APIView):
    def get(self, request):
        course = Course.objects.all()
        serilizer = ListTitleSerializer(course, many=True)
        context = ({"serilizer": serilizer});
        # return Response(serilizer.data, status=200)
        return render(request, "connectdata/test_ajax.html", context)


# List CourseSerializerLib #Authenications to view

class isCourseList(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserID == request.user


class CourseListViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializerLib
    permission_classes = (isCourseList,)

    # Ensure a user sees only own Note objects.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Course.objects.filter(UserID=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)


class CourseListAPIView(generics.ListCreateAPIView):
    serializer_class = CourseSerializerLib
    permission_classes = (isCourseList,)

    # Ensure a user sees only own Note objects.

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Course.objects.filter(UserID=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)


class CourseDetailAPIView(APIView):
    serializer_class = CourseSerializerLib
    permission_classes = (isCourseList,)


class CourseSerializerAPIView(ListAPIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)


# List CourseSerializerLib #Authenications to view


class CourseSerializerLibAPIView(ListAPIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)


# List CompanySerializerLib ++++ Authentications get + post

class CompanySerializerLibAPIView(APIView):
    def get(self, request):
        company = Company.objects.all()
        serilizer = CompanySerializerLib(company, many=True)
        return Response(serilizer.data, status=200)


class ComAllSerializerView(APIView):
    def get(self, request):
        company = Company.objects.all()
        serilizer = ComAllSerializer(company, many=True)
        return Response(serilizer.data, status=200)


class CourseAllSerializerView(APIView):
    def get(self, request):
        company = Course.objects.all()
        serilizer = CourseAllSerializer(company, many=True)
        return Response(serilizer.data, status=200)


# List CompanySerializerLib ++++ Authentications get + post

class IsUserIDCompany(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserID == request.user


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializerLib
    permission_classes = (IsUserIDCompany,)

    # Ensure a user sees only own Note objects.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Company.objects.filter(UserID=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)


# List CompanySerializerLib ++++ Authentications get + post


class IsOwnerCouresList(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserID == request.user


class CouresComListViewSet(viewsets.ModelViewSet):
    serializer_class = CourseCompanySerializerLib
    permission_classes = (IsOwnerCouresList,)

    # Ensure a user sees only own Note objects.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Course.objects.filter(UserID=user)
        raise PermissionDenied()

    # Set user as owner of a CourseCom object.
    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)


class CourseCompanySerializerLibView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseCompanySerializerLib

    def get(self, request):
        queryset = self.get_queryset()
        serializer = CourseCompanySerializerLib(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = CourseCompanySerializerLib(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.erros, status=400)


# List CompanySerializerLib ++++ Authentications get + post


# List CourseCompanySerializerLibDetail #Authenications to view
class IsUserIDCoures(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserID == request.user


class CouresViewSet(viewsets.ModelViewSet):
    serializer_class = CourseCompanySerializerLib
    permission_classes = (IsUserIDCoures,)

    # Ensure a user sees only own Note objects.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Course.objects.filter(UserID=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)


# CourseCompany Nested
###########Nested Get - Post Course - Compnany ViewSet ##########

class isCourseCompanyList(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserID == request.user


class CourseCompanySerializerViewSet(viewsets.ModelViewSet):
    serializer_class = CourseCompanySerializerLib
    permission_classes = (isCourseCompanyList,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Course.objects.filter(UserID=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserID=self.request.user)


class CourseCompanySerializerLibDetail(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseCompanySerializerLib

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return Course.objects.get(id=id)
        except Course.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = CourseCompanySerializerLib(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = CourseCompanySerializerLib(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


###########Nested Get - Post Course - Compnany ViewSet ##########

# List CourseCompanySerializerLibDetail #Authenications to view


def ajaxclient(request):
    return render(request, "connectdata/test_ajax.html")


def xoa(request):
    return render(request, "connectdata/xoa.html")


def AjaxCourseCompnay(request):
    return render(request, "connectdata/Ajax_Course_Company.html")


def getip(request):
    return render(request, "connectdata/getip.html")


def multigetip(request):
    return render(request, "connectdata/multilocation.html")


###########################Nested 07/07/2020#######################


########################### Update Profile#######################


class IsProfileUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserProfile == request.user


class ProfileUserViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileUserFullSerializer
    permission_classes = (IsProfileUser,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Profile.objects.filter(UserProfile=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def create(self, request):
        pass

    def destroy(self, request, pk=None):
        pass

    def perform_create(self, serializer):
        serializer.save(UserProfile=self.request.user)


class ProfileUserViewAll(APIView):
    # permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_classes = (IsAuthenticated,)

    # queryset = profile.objects.all()
    # serializer_class = ProfileUserFullSerializer
    def get(self, request):
        # queryset = self.get_queryset()
        qr = Profile.objects.all()
        serializer = ProfileUserFullSerializer(qr, many=True)
        return Response(serializer.data)


class ProfileUserViewNolog(APIView):
    permission_classes = (AllowAny,)

    # permission_classes = (IsAuthenticated,)
    # queryset = profile.objects.all()
    # serializer_class = ProfileUserFullSerializer
    def get(self, request):
        # queryset = self.get_queryset()
        qr = Profile.objects.all()
        serializer = ProfileUserFullSerializer(qr, many=True)
        return Response(serializer.data)


########################### Update Profile#######################


################################ Bank User########################

class IsUserBank(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDBank == request.user


class UserBankFullViewSet(viewsets.ModelViewSet):
    serializer_class = UserBankFullSerializer
    permission_classes = (IsUserBank,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return UserBank.objects.filter(UserIDBank=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDBank=self.request.user, EmployeeID=employee)


class UserBankFullViewAll(ListAPIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = UserBankFullSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = ProfileUserFullSerializer(queryset, many=True)
        return Response(serializer.data)


################################ Bank User#####################################

################################ ProfileImageSerializer #######################


class ProfileImageAPIView(ListAPIView):
    # parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileImageSerializer
    queryset = Profile.objects.all()

    # permission_classes = [AllowAny,]

    def get(self, request):
        queryset = self.get_queryset()
        serilizer = ProfileImageSerializer(queryset, many=True)
        return Response(serilizer.data, status=200)


################################ ProfileImageSerializer Token #######################

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
    def create(self, request):
        pass

    def destroy(self, request, pk=None):
        pass

    def perform_create(self, serializer):
        serializer.save(UserProfile=self.request.user)


class ProfileUserCMND1(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CMND1ImageSerializer
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

    def create(self, request):
        pass

    def destroy(self, request, pk=None):
        pass


class ProfileUserCMND2(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CMND2ImageSerializer
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

    def create(self, request):
        pass

    def destroy(self, request, pk=None):
        pass


########################### ProfileImageSerializer Token#######################

###################### Create User's Profile Employer Employee  ####################


################################ Create User's Profile Employer Employee  #####################################

################################ Create User's Profile Employer Employee  #####################################

### Create for Employee

class IsCreateEmployee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDEmployee == request.user


class CreateEmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = CreateEmployeeSerializer
    permission_classes = (IsCreateEmployee,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserIDEmployee=self.request.user)


### Create for Employer

class IsCreateEmployer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDEmployer == request.user


class CreateEmployerViewSet(viewsets.ModelViewSet):
    serializer_class = CreateEmployerSerializer
    permission_classes = (IsCreateEmployer,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employer.objects.filter(UserIDEmployer=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserIDEmployer=self.request.user)


## Create for Profile

class IsCreateProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserProfile == request.user


class CreateProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CreateProfileSerializer
    permission_classes = (IsCreateProfile,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Profile.objects.filter(UserProfile=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserProfile=self.request.user)


############################# Create User's Profile Employer Employee  ##############################

################################ User's Image AttPhoto #####################################
class IsAttPhotoImage(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserIDAttPhoto == request.user


class AttPhotoUserViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = AttPhotoImageSerializer
    permission_classes = (IsAttPhotoImage,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return AttPhoto.objects.filter(UserIDAttPhoto=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserIDAttPhoto=self.request.user)


################################ User's Image AttPhoto #####################################

################################ Employee AttPhoto #####################################

class isEmployeeAttPhoto(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDEmployee == request.user


class EmployeeAttPhotoViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = EmployeeAttPhotoSerializer
    permission_classes = (isEmployeeAttPhoto,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserIDEmployee=self.request.user)


################################ Employee AttPhoto #####################################

################################ Bank User#####################################

################################ Employee Image User#####################################

class IsAttPhotoEmployee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDAttPhoto == request.user


class AttPhotoEmployeeFullViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = AttPhotoEmployeeSerializer
    permission_classes = (IsAttPhotoEmployee,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return AttPhoto.objects.filter(UserIDAttPhoto=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDAttPhoto=self.request.user, EmployeeIDAttPhoto=employee)


################################ Employee Image User#####################################

################################ User Eduaction #####################################

class IsUserEducation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDEducation == request.user


class UserEducationViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UserEducationSerializer
    permission_classes = (IsUserEducation,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Education.objects.filter(UserIDEducation=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDEducation=self.request.user, EmployeeIDEducation=employee)


################################  User Eduaction #####################################

################################  CurriculumVitae Education #####################################


class IsCurriculumVitaeEducation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDCurriculumVitae == request.user


class CurriculumVitaeEducationViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CurriculumVitaeEducationSerializer
    permission_classes = (IsCurriculumVitaeEducation,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CurriculumVitae.objects.filter(UserIDCurriculumVitae=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        # user = self.request.user
        # curriculumvitae = CurriculumVitae.objects.get(UserIDCurriculumVitae=user)
        # #employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDCurriculumVitae=self.request.user)


#########################  Employee Education ##############################

class IsEmployeeEducation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDEducation == request.user


class EmployeeEducationViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CVEmployeeEducationSerializer
    permission_classes = (IsEmployeeEducation,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Education.objects.filter(UserIDEducation=user, )
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDEducation=self.request.user, EmployeeIDEducation=employee)


#########################  Employee Education ##############################

#########################  Employee Career ##############################

class IsEmployeeCareer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDCareer == request.user


class EmployeeCareerViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = EmployeeCareerSerializer
    permission_classes = (IsEmployeeCareer,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Career.objects.filter(UserIDCareer=user, )
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDCareer=self.request.user, EmployeeIDCareer=employee)


#########################  Employee Career ##############################

################################  User Eduaction #####################################

################################  CurriculumVitae Experiences #####################################

class IsCVEmployeeExperiences(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDExperiences == request.user


class CVEmployeeExperiencesViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CVEmployeeExperiencesSerializer
    permission_classes = (IsCVEmployeeExperiences,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # employee = Employee.objects.get(UserIDEmployee=user)
            return Experiences.objects.filter(UserIDExperiences=user, )
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        # user = self.request.user
        # employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDExperiences=self.request.user)


################################  User CV #####################################


class IsCV(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDCurriculumVitae == request.user


class CVViewSet(viewsets.ModelViewSet):
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = CVSerializer
    permission_classes = (IsCV,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # curriculumvitae = get_object_or_404(CurriculumVitae, isFinishCV=False)
            # if curriculumvitae is not None:
            #     curriculumvitae.delete()
            # employee = Employee.objects.get(UserIDEmployee=user)
            return CurriculumVitae.objects.filter(UserIDCurriculumVitae=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        user = self.request.user
        profileidcurriculumVitae = Profile.objects.get(UserProfile=user)
        serializer.save(UserIDCurriculumVitae=self.request.user,
                        ProfileIDCurriculumVitae=profileidcurriculumVitae,
                        isFinishCV=False,
                        )
        # return CurriculumVitae.id


# CVFinishSerializer

class CVFinishViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CVFinishSerializer
    permission_classes = (IsCV,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # employee = Employee.objects.get(UserIDEmployee=user)
            return CurriculumVitae.objects.filter(UserIDCurriculumVitae=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        user = self.request.user
        profileidcurriculumVitae = Profile.objects.get(UserProfile=user)
        serializer.save(UserIDCurriculumVitae=self.request.user,
                        ProfileIDCurriculumVitae=profileidcurriculumVitae,
                        isFinishCV=True,
                        )


################################  CurriculumVitae Education #####################################

class IsCVEducation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDEducation == request.user


class CVEducationViewSet(APIView):
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = EducationIDCurriculumVitaeSerializer
    permission_classes = (IsCVEducation,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            employee = Employee.objects.get(UserIDEmployee=user)
            # cvemedu = CurriculumVitae.objects.get(UserIDEmployee=user)
            return Education.objects.filter(UserIDEducation=user, EmployeeIDEducation=employee)
        raise PermissionDenied()

    ############# Thinh
    def get_object(self, pk):
        try:
            return Education.objects.get(id=pk)
        except Education.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        education = self.get_object(pk)
        serializer = EducationIDCurriculumVitaeSerializer(education)
        return Response(serializer.data)

    def put(self, request, pk, format=None):

        id_CVEdu_list = []

        education = self.get_object(pk)
        for cvedu in education.CurriculumVitaeIDEducation.all():
            id_CVEdu_list.append(cvedu.id)

        for cvedu in request.data["CurriculumVitaeIDEducation"]:
            if cvedu not in id_CVEdu_list:
                id_CVEdu_list.append(cvedu)
            else:
                id_CVEdu_list.pop(id_CVEdu_list.index(cvedu))

        request.data["CurriculumVitaeIDEducation"] = id_CVEdu_list
        serializer = EducationIDCurriculumVitaeSerializer(education, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        education = self.get_object(pk)
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    ############# Thinh


class CVEducationList(APIView):
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = EducationIDCurriculumVitaeSerializer
    permission_classes = (IsCVEducation,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            employee = Employee.objects.get(UserIDEmployee=user)
            # cvemedu = CurriculumVitae.objects.get(UserIDEmployee=user)
            return Education.objects.filter(UserIDEducation=user, EmployeeIDEducation=employee)
        raise PermissionDenied()

    def get(self, request):
        education = Education.objects.all()
        serailizer = EducationIDCurriculumVitaeSerializer(education, many=True)
        return Response(serailizer.data, status=200)

    def get_object(self, pk):
        try:
            return Education.objects.get(id=pk)
        except Education.DoesNotExist:
            raise Http404

    def getdetail(self, request, pk, format=None):
        education = self.get_object(pk)
        serializer = EducationIDCurriculumVitaeSerializer(education)
        return Response(serializer.data)
    # Set user as owner of a Notes object.
    # def perform_create(self, serializer):
    #     user = self.request.user
    #     curriculumvitae = CurriculumVitae.objects.get(UserIDCurriculumVitae=user)
    #     employee = Employee.objects.get(UserIDEmployee=user)
    #     education = Education.objects.get(UserIDEducation=user)
    #     serializer.save(UserIDEducation=self.request.user,
    #                     CurriculumVitaeIDEducation=education.curriculumvitae.objects.add(id=curriculumvitae.id),
    #                     EmployeeIDEducation=employee,
    #                     )


################################  User Eduaction #####################################

########################## CV Education ManyToMany ################################


class IsCVManyToMany(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDCurriculumVitae == request.user


class CVManyToMany(viewsets.ModelViewSet):
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = CVManyToManySerializer
    permission_classes = (IsCVManyToMany,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # employee = Employee.objects.get(UserIDEmployee=user)
            return CurriculumVitae.objects.filter(UserIDCurriculumVitae=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        # user = self.request.user
        # eduacation = Education.objects.get(UserIDEducation=user)
        serializer.save(UserIDCurriculumVitae=self.request.user)


########################## CV Education ManyToMany ################################

########################## Khong Phan Quyen ManyToMany CV - Edu ################################

class IsEducationManyToMany(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDEducation == request.user


class EducationViewSet(viewsets.ModelViewSet):
    """
    List all workers, or create a new worker.
    """
    # parser_classes = [MultiPartParser, FormParser]

    queryset = Education.objects.all()
    serializer_class = EduManyToManySerializer
    permission_classes = (IsEducationManyToMany,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # employee = Employee.objects.get(UserIDEmployee=user)
            return Education.objects.filter(UserIDEducation=user)
        raise PermissionDenied()
        # Set user as owner of a Notes object.

    def perform_create(self, serializer):
        # user = self.request.user
        # eduacation = Education.objects.get(UserIDEducation=user)
        serializer.save(UserIDEducation=self.request.user)


class CurriculumVitaeViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    """
    List all workkers, or create a new worker.
    """
    queryset = CurriculumVitae.objects.all()
    serializer_class = CVEduManyToManySerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['Degree']


########################## Khong Phan Quyen ManyToMany CV - Edu ################################

########################## Update Create Full Full - Edu ################################

# EducationFullSerializer


class IsEmployeeEducationFull(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDEducation == request.user


class EducationFullEmployeeViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = EducationFullSerializer
    permission_classes = (IsEmployeeEducationFull,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Education.objects.filter(UserIDEducation=user, )
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDEducation=self.request.user, EmployeeIDEducation=employee)


########################## Update Create Full - Edu ################################

########################## Update Create Full - Experience ################################


# ExperienceFullSerializer

class IsEmployeeExperienceFull(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDExperiences == request.user


class ExperienceFullEmployeeViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ExperienceFullSerializer
    permission_classes = (IsEmployeeExperienceFull,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Experiences.objects.filter(UserIDExperiences=user, )
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDExperiences=self.request.user, EmployeeIDExperiences=employee)


# Update Experience for CV CVEmployeeExperiencesSerializer

################################  CurriculumVitae Education #####################################

class IsCVExperience(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDExperiences == request.user


class CVExperienceAPIView(APIView):
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = CVEmployeeExperiencesSerializer
    permission_classes = (IsCVExperience,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            employee = Employee.objects.get(UserIDEmployee=user)
            # cvemedu = CurriculumVitae.objects.get(UserIDEmployee=user)
            return Experiences.objects.filter(UserIDExperiences=user, EmployeeIDExperiences=employee)
        raise PermissionDenied()

    ############# Thinh
    def get_object(self, pk):
        try:
            return Experiences.objects.get(id=pk)
        except Experiences.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cv = self.get_object(pk)
        serializer = CVEmployeeExperiencesSerializer(cv)
        return Response(serializer.data)

    def put(self, request, pk, format=None):

        id_CVExp_list = []

        cv = self.get_object(pk)
        for cvep in cv.CurriculumVitaeIDExperiences.all():
            id_CVExp_list.append(cvep.id)

        for cvep in request.data["CurriculumVitaeIDExperiences"]:
            if cvep not in id_CVExp_list:
                id_CVExp_list.append(cvep)
            else:
                id_CVExp_list.pop(id_CVExp_list.index(cvep))

        request.data["CurriculumVitaeIDExperiences"] = id_CVExp_list
        serializer = CVEmployeeExperiencesSerializer(cv, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cv = self.get_object(pk)
        cv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


########################## Update Create Full - Experience ################################


# isFinishCVSerializer

class FinishCVAPIView(APIView):

    # def get(self, request):
    #     idCurriculumVitae = CurriculumVitae.objects.get(isFinishCV=True)
    #     curriculumvitae = CurriculumVitae.objects.get(id=idCurriculumVitae.id)
    #     datacurriculumvitae = isFinishCVSerializer(curriculumvitae)
    #     return Response(datacurriculumvitae.data)

    def get_object(self):
        try:
            return CurriculumVitae.objects.get(isFinishCV=False)
        except CurriculumVitae.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request):
        idCurriculumVitae = CurriculumVitae.objects.get(isFinishCV=False)
        pk = idCurriculumVitae.id
        try:
            curriculumvitae = CurriculumVitae.objects.get(id=pk)
        except:
            return Response(status=404)
        serializers = isFinishCVSerializer(curriculumvitae)
        return Response(serializers.data)
    #
    # def put(self, request, pk=None):
    #     data = request.data
    #     idCurriculumVitae = CurriculumVitae.objects.first(isFinishCV=True)
    #     pk = idCurriculumVitae.id
    #     instance = self.get_object(pk)
    #     serializer = isFinishCVSerializer(instance, data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=200)
    #     return Response(serializer.errors, status=400)
    #
    # def delete(self, request, pk=None):
    #     idCurriculumVitae = CurriculumVitae.objects.first(isFinishCV=True)
    #     pk = idCurriculumVitae.id
    #     instance = self.get_object(pk)
    #     instance.delete()
    #     return HttpResponse(status=204)


########################## Search CV: Address################################

class SearchCV(mixins.ListModelMixin, GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = CurriculumVitae.objects.all()
    serializer_class = SearchCVSerializer
    filter_backends = [AddressFilterBackend, AddressSearchFilter]
    filterset_fields = [
        'AddressIDCurriculumVitae__WardIDAddress__NameWard',
        'AddressIDCurriculumVitae__DistrictIDAddress__NameDistrict',
        'AddressIDCurriculumVitae__ProvinceCityIDAddress__NameProvinceCity',
        'AddressIDCurriculumVitae__CountryIDAddress__NameCountry',
    ]
    search_fields = ['DesiredPositionIDCurriculumVitae']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


########################## Search CV: Address################################

# ############################################### EMPLOYER ####################################################

# *********************************** Employer Bank User **************************************
#
# class EmployerUserBankFullViewSet(viewsets.ModelViewSet):
#     serializer_class = EmployerBankViewSetSerializer
#     permission_classes = (IsUserBank,)
#
#     # Ensure a user sees only own Note objectsu.
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return UserBank.objects.filter(UserIDBank=user)
#         raise PermissionDenied()
#
#     # Set user as owner of a Notes object.
#     def perform_create(self, serializer):
#         user = self.request.user
#         employer = Employer.objects.get(UserIDEmployer=user)
#         serializer.save(UserIDBank=self.request.user, EmployerIDBank=employer)
#

# **************************************  User Company ****************************************

# class IsUserCompany(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.UserIDCompany == request.user
#
#
# class EmployerCompayFullViewSet(viewsets.ModelViewSet):
#     serializer_class = EmployerCompanyViewSetSerializer
#     permission_classes = (IsUserCompany,)
#
#     # Ensure a user sees only own Note objectsu.
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Company.objects.filter(UserIDCompany=user)
#         raise PermissionDenied()
#
#     # Set user as owner of a Notes object.
#     def perform_create(self, serializer):
#         user = self.request.user
#         employer = Employer.objects.get(UserIDEmployer=user)
#         serializer.save(UserIDCompany=self.request.user, EmployerIDCompany=employer)


# ***************************************** Employer - Address **************************************

#
# class EmployerAddressFullViewSet(viewsets.ModelViewSet):
#     serializer_class = EmployerAdressViewSetSerializer
#     permission_classes = (IsUserAddress,)
#
#     # Ensure a user sees only own Note objectsu.
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Address.objects.filter(UserIDAddress=user)
#         raise PermissionDenied()
#
#     # Set user as owner of a Notes object.
#     def perform_create(self, serializer):
#         user = self.request.user
#         employer = Employer.objects.get(UserIDEmployer=user)
#         serializer.save(UserIDAddress=self.request.user, EmployerIDAddress=employer)


# ***************************************** Employer Jobs ************************************************
# class IsUserJobs(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.UserIDJobs == request.user
#
#
# class EmployerJobsFullViewSet(viewsets.ModelViewSet):
#     serializer_class = EmployerJobsViewSetSerializer
#     permission_classes = (IsUserJobs,)
#
#     # Ensure a user sees only own Note objectsu.
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Jobs.objects.filter(UserIDJobs=user)
#         raise PermissionDenied()
#
#     # Set user as owner of a Notes object.
#     def perform_create(self, serializer):
#         user = self.request.user
#         employer = Employer.objects.get(UserIDEmployer=user)
#         serializer.save(UserIDJobs=self.request.user, EmployerIDJobs=employer)


# # ************************************************ Employer Inout *********************************************
# class IsUserInout(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.UserIDInOut == request.user
#
#
# class EmployerInoutFullViewSet(viewsets.ModelViewSet):
#     serializer_class = EmployerInoutViewSetSerializer
#     permission_classes = (IsUserInout,)
#
#     # Ensure a user sees only own Note objectsu.
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return InOut.objects.filter(UserIDInOut=user)
#         raise PermissionDenied()
#
#     # Set user as owner of a Notes object.
#     def perform_create(self, serializer):
#         user = self.request.user
#         employer = Employer.objects.get(UserIDEmployer=user)
#         serializer.save(UserIDInOut=self.request.user, EmployerIDAddress=employer)


# # ############################################ GET ALL JOB #########################################################
# class JobsViewAll(APIView):
#     permission_classes = (AllowAny,)
#     # permission_classes = (IsAuthenticatedOrReadOnly,)
#     # permission_classes = (IsAuthenticated,)
#
#     # queryset = profile.objects.all()
#     # serializer_class = ProfileUserFullSerializer
#     def get(self, request):
#         # queryset = self.get_queryset()
#         qr = Jobs.objects.all()
#         serializer = ViewJobSerializer(qr, many=True)
#         return Response(serializer.data)


########### Nested Get - Post Schedule - Inout ViewSet ##########

class isScheduleCV(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDShedule == request.user


class ScheduleCVViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleCVSerializer
    permission_classes = (isScheduleCV,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Schedule.objects.filter(UserIDShedule=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDShedule=self.request.user, EmlpoyeeIDSchedule=employee)


### Filter Thành Phố Theo Quốc Gia
class CountryFilter(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = Country.objects.all()
        serilizer = CountrySerializer(queryset, many=True)
        return Response(serilizer.data, status=200)


class ProvinceCityFilter(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = ProvinceCity.objects.filter(CountryIDProvinceCity=request.data['CountryIDProvinceCity'])
        serilizer = ProvinceCitySerializer(queryset, many=True)
        return Response(serilizer.data, status=200)


class DistrictFilter(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = District.objects.filter(ProvinceCityIDDistrict=request.data['ProvinceCityIDDistrict'])
        serilizer = DistrictSerializer(queryset, many=True)
        return Response(serilizer.data, status=200)


class WardFilter(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = Ward.objects.filter(DistrictIDWard=request.data['DistrictIDWard'])
        serilizer = WardSerializer(queryset, many=True)
        return Response(serilizer.data, status=200)


class isAddress(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDAddress == request.user


class AddressViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = AddressSerializer
    permission_classes = (isAddress,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Address.objects.filter(UserIDAddress=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserIDAddress=self.request.user)


class isCheckInOut(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDCheckInOut == request.user


class CheckInOutViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]

    serializer_class = CheckInOutSerializer
    permission_classes = (isCheckInOut,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CheckInOut.objects.filter(UserIDCheckInOut=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        user = self.request.user
        scheduleidcheckinout = Schedule.objects.get(UserIDShedule=user)
        companyidcheckinout = Company.objects.get(UserIDCompany=user)
        jobidcheckinout = Jobs.objects.get(UserIDJobs=user)
        curriculumvitaeidcheckinout = CurriculumVitae.objects.get(UserIDCurriculumVitae=user)
        serializer.save(
            UserIDCheckInOut=self.request.user,
            ScheduleIDCheckInOut=scheduleidcheckinout,
            CompanyIDCheckInOut=companyidcheckinout,
            JobIDCheckInOut=jobidcheckinout,
            CurriculumVitaeIDCheckInOut=curriculumvitaeidcheckinout
        )


### Location Thành Phố Theo Quốc Gia


class isLocation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDLocation == request.user


class LocationViewSet(viewsets.ModelViewSet):
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = LocationSerializer
    permission_classes = (isLocation,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Location.objects.filter(UserIDLocation=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(
            UserIDLocation=self.request.user,
        )


class isCompanyEmployer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDCompany == request.user


class CompanyEmployerViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CompanyEmployerSerializer
    permission_classes = (isCompanyEmployer,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Company.objects.filter(UserIDCompany=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(
            UserIDCompany=self.request.user,
        )


# create CV test
# ****************************************** Employee CV ***********************************************
class IsEmployeeCV(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDCurriculumVitae == request.user


class EmployeeCVViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = EmployeeCurriculumVitaeViewSetSerializer
    permission_classes = (IsEmployeeCV,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CV.objects.filter(UserIDCurriculumVitae=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(
            UserIDCurriculumVitae=self.request.user,
            EmployeeIDCurriculumVitae=employee,
        )


class IsCareer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDCareer == request.user


class CareerViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CareerViewSetSerializer
    permission_classes = (IsCareer,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Career.objects.filter(UserIDCareer=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(
            UserIDCareer=self.request.user,
            EmployeeIDCareer=employee,
        )


class IsProfile(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserProfile == request.user


class ProfileFullCheckViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializerCheck
    permission_classes = (IsProfile,)

    # Ensure a user sees only own Note objects.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Profile.objects.filter(UserProfile=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserProfile=self.request.user)


class IsWorkLocation(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserIDWorkLocation == request.user


class WorkLocationViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = WorkLocationSerializer
    permission_classes = (IsWorkLocation,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return WorkLocation.objects.filter(UserIDWorkLocation=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(UserIDWorkLocation=self.request.user)
