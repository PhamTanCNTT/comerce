from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from pymongo.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

from Employer.serializers import ScheduleDateInOutSerializer, ScheduleViewSerializer, LocationViewSerializer, \
    DateInOutSingleSerialzier, DateInOutSerialzier
from connectdata.models import *
from connectdata.serializers import LocationSerializer
from employee.serializers import EmployeeBankSerializer, EmployeeSimpleSerializer, \
    EmployeeBankABCSerializer, EmployeeBankViewSerializer, EmployeeBankVSSerializer, EmployeeUserBankViewSetSerializer, \
    EmployeeEducateViewSetSerializer, EmployeeExperiencesViewSetSerializer, EmployeeUserBankDetailSerializer, \
    EmployeeEducateDetailSerializer, EmployeeCurriculumVitaeDetailSerializer, EmployeeAddressDetailSerializer, \
    EmployeeExperiencesDetailSerializer, isFinishCVSerializer, EducationIDCurriculumVitaeSerializer, \
    EmployeeCurriculumVitaeViewSetSerializer, CVSerializer, JobApplySerializer, CareerSerializer
from rest_framework import permissions
from rest_framework.generics import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()


############################### Employee User #####################################

###########Nested Get - Post Simple ##########

class EmployeeSimpleListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSimpleSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = EmployeeSimpleSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = EmployeeSimpleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


###########Nested Get - Post Simple ##########

###########Nested GetDetail - Put - Delete ##########

class EmployeeSimpleDetail(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSimpleSerializer

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = EmployeeSimpleSerializer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = EmployeeSimpleSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


###########Nested Get - Post Employee - Bank ViewSet ##########

class IsEmployeeBank(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
                obj.UserIDEmployee == request.user and
                obj.UserIDBank == request.user
        )


class EmployeeBankViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeBankSerializer
    permission_classes = (IsEmployeeBank,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return (
                    Employee.objects.filter(UserIDEmployee=user) and
                    UserBank.objects.filter(UserIDBank=user)
            )
        raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(UserIDEmployee=self.request.user, UserIDBank=self.request.user)


class EmployeeBankViewSetAll(ListAPIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeBankSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = EmployeeBankSerializer(queryset, many=True)
        return Response(serializer.data)


###########Nested Get - Post Employee - Bank ViewSet ##########

########### Nested Get - Post Simple ##################


###########Nested Get - Post Employee - Bank ##########

class EmployeeBankListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeBankSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = EmployeeBankSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = EmployeeBankSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


########### Nested Get - Post Simple ##################

###########Nested Get - Post - Delete - Employee - Bank  Details##########

class EmployBankDetail(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeBankSerializer

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = EmployeeBankSerializer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = EmployeeBankSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


###########Nested Get - Post - Delete - Employee - Bank  Details##########


###########Nested Get - Post Bank - Employ ##########

########### Nested Get - Post Bank - Employ ##########


################################ Employee User###############################

###########Nested Get - Post Employee - Bank ViewSet ##########

class IsEmployeeBankABC(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.UserIDEmployee == request.user


class EmployeeBankViewSetABC(viewsets.ModelViewSet):
    serializer_class = EmployeeBankABCSerializer
    permission_classes = (IsEmployeeBankABC,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        serializer.save(UserIDEmployee=self.request.user)


class EmployeeBankViewSetAllABC(ListAPIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeBankABCSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = EmployeeBankABCSerializer(queryset, many=True)
        return Response(serializer.data)


###########Nested Get - Post Employee - Bank ViewSet ##########


class IsEmployeeBankView(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                obj.UserIDEmployee == request.user and
                obj.UserIDBank == request.user
        )


class EmployeeBankFullViewSetABC(viewsets.ModelViewSet):
    serializer_class = EmployeeBankViewSerializer
    permission_classes = (IsEmployeeBankView,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return (
                    Employee.objects.filter(UserIDEmployee=user) and
                    UserBank.objects.filter(UserIDBank=user)
            )
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserIDEmployee=self.request.user, UserIDBank=self.request.user)


########### Get - Post Employee - Bank ViewSet EmployeeBankVSSerializer ##########

class isEmployeeBankVS(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDEmployee == request.user


class EmployeeBankVSViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeBankVSSerializer
    permission_classes = (isEmployeeBankVS,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        serializer.save(UserIDEmployee=self.request.user)


############# Get - Post Employee - Bank ViewSet EmployeeBankVSSerializer ##########

class IsEmployeeBankView(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                obj.UserIDEmployee == request.user and
                obj.UserIDBank == request.user
        )


class EmployeeBankVSView(ListAPIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeBankVSSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    def get(self, request):
        queryset = self.get_queryset()
        # qr = profile.objects.all()
        serializer = EmployeeBankVSSerializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeBankVSViewDetail(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeBankVSSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = EmployeeBankVSSerializer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = EmployeeBankVSSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


# ################################################ EMPLOYEE #################################################


# ********************************* Employee Bank User ***************************************
class IsUserBank(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDUserBank == request.user


class EmployeeUserBankFullViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = EmployeeUserBankViewSetSerializer
    permission_classes = (IsUserBank,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return UserBank.objects.filter(UserIDUserBank=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDUserBank=self.request.user, EmployeeIDUserBank=employee)


# ########################################### Education ###########################################

class IsUserEducation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDEducation == request.user


class EmployeeEducateFullViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = EmployeeEducateViewSetSerializer
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


# ####################################### Experiences ############################################
class IsUserExperiences(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDExperiences == request.user


class EmployeeExperiencesFullViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = EmployeeExperiencesViewSetSerializer
    permission_classes = (IsUserExperiences,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Experiences.objects.filter(UserIDExperiences=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDExperiences=self.request.user, EmployeeIDExperiences=employee)


# ########################################### Employee CV #########################################
class IsUserCV(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDCurriculumVitae == request.user


class EmployeeCVFullViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = EmployeeCurriculumVitaeViewSetSerializer
    permission_classes = (IsUserCV,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CurriculumVitae.objects.filter(UserIDCurriculumVitae=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDCurriculumVitae=self.request.user, EmployeeIDCurriculumVitae=employee)


############################### Employee User #####################################

########### Get - Post Employee - Bank ViewSet EmployeeBankVSSerializer ##########


class EmployeeUserBankFullView(ListAPIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeUserBankDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    def get(self, request):
        queryset = self.get_queryset()
        # qr = profile.objects.all()
        serializer = EmployeeUserBankDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeUserBankDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeUserBankDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = EmployeeUserBankDetailSerializer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = EmployeeUserBankDetailSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


########### Get  Employee - Educate ViewSet ##########
class EmployeeEducateFullView(ListAPIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeEducateDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    def get(self, request):
        queryset = self.get_queryset()
        # qr = profile.objects.all()
        serializer = EmployeeEducateDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeEucateDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeEducateDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = EmployeeEducateDetailSerializer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = EmployeeEducateDetailSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


# ********************************************** GET Employee - CV ************************************************
class EmployeeCurriculumVitaeFullView(ListAPIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeCurriculumVitaeDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    def get(self, request):
        queryset = self.get_queryset()
        # qr = profile.objects.all()
        serializer = EmployeeCurriculumVitaeDetailSerializer(queryset, many=True)
        return Response(serializer.data)


# ********************************************** Detail Emplyee - CV ************************************************
class EmployeeCurriculumVitaeDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeCurriculumVitaeDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = EmployeeCurriculumVitaeDetailSerializer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = EmployeeCurriculumVitaeDetailSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


# *********************************************** Employee - Address ***********************************************
class EmployeeAddressFullView(ListAPIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeAddressDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    def get(self, request):
        queryset = self.get_queryset()
        # qr = profile.objects.all()
        serializer = EmployeeAddressDetailSerializer(queryset, many=True)
        return Response(serializer.data)


# ******************************** Detail - Employer - Address *************************************
class EmployerAddressDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeAddressDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = EmployeeAddressDetailSerializer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = EmployeeAddressDetailSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


# ****************************************** Experiences **********************************************

class EmployeeExperiencesFullView(ListAPIView):
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeExperiencesDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    def get(self, request):
        queryset = self.get_queryset()
        # qr = profile.objects.all()
        serializer = EmployeeExperiencesDetailSerializer(queryset, many=True)
        return Response(serializer.data)


# ******************************** Detail - Employee - Experiences *************************************
class EmployerExperiencesDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeExperiencesDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Employee.objects.filter(UserIDEmployee=user)
        raise PermissionDenied()

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = EmployeeExperiencesDetailSerializer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = EmployeeExperiencesDetailSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


# ******************************** get id CV *************************************
# check isFinishCVSerializer
class FinishCVAPIView(APIView):

    def get_object(self):
        try:
            return CurriculumVitae.objects.get(isFinishCV=False)
        except CurriculumVitae.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request):
        # idCurriculumVitae = CurriculumVitae.objects.filter(isFinishCV=True).last()
        idCurriculumVitae = CurriculumVitae.objects.get(isFinishCV=False)
        pk = idCurriculumVitae.id
        try:
            curriculumvitae = CurriculumVitae.objects.get(id=pk)
        except:
            return Response(status=404)
        serializers = isFinishCVSerializer(curriculumvitae)
        return Response(serializers.data)


# education - checkbox
class IsCVEducation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDEducation == request.user


# ************************************** Array education CV ***********************************
# education - checkbox
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


# Link to web

def cv(request):
    return render(request, "employee/cv.html")


def createcv(request):
    return render(request, "employee/createcv.html")


def employeeprofile(request):
    return render(request, "employee/employeedash.html")


def basetest(request):
    return render(request, "account/base.html")


def employeebase(request):
    return render(request, "employeebase.html")


def listprofile(request):
    return render(request, "employee/listprofile.html")


def login_views(request):
    return render(request, "login.html")


def calender2(request):
    return render(request, "calendar2.html")


################################ CV ######################################

class IsCV(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDCurriculumVitae == request.user


class CVViewSet(viewsets.ModelViewSet):
    # parser_classes = [MultiPartParser, FormParser]
    serializer_class = CVSerializer
    permission_classes = (IsCV,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CV.objects.filter(UserIDCurriculumVitae=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDCurriculumVitae=self.request.user, EmployeeIDCurriculumVitae=employee)


################################ CV ######################################


############################# APPLY JOB ##################################

class EmployeeJobApply(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = JobApplySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return JobApply.objects.filter(UserIDJobApply=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDJobApply=user, EmployeeIDJobApply=employee)


############################# APPLY JOB ##################################

####################### Schedule CheckInOut ##############################
# LocationSerializer
# ScheduleDateInOutSerializer

@api_view(['GET'])
def ScheduleCheckInOut(request):
    permission_classes = (AllowAny,)
    schedule = Schedule.objects.all()
    scheduledateinout = ScheduleViewSerializer(schedule, many=True)
    checkinout = Location.objects.all()
    location = LocationViewSerializer(checkinout, many=True)
    schedulecheckinout = scheduledateinout.data + location.data

    return Response(schedulecheckinout)


@api_view(['GET'])
def ScheduleCheckInOutDetail(request, pk):
    try:
        schedule = get_object_or_404(Schedule, id=pk)
        # jobapplyidinoutarr =
        dateinout = DateInOut.objects.filter(ScheduleIDDateInOut=schedule)
        checkinout = CheckInOut.objects.filter(ScheduleIDCheckInOut=schedule).first()
        if checkinout is None:
            return Response({"error": "Given question object not found."}, status=404)
        location = Location.objects.filter(JobApplyIDLocation=checkinout.JobApplyIDInOutArr)

    except Schedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        scheduledateinout = ScheduleViewSerializer(schedule)
        dateinoutschedule = DateInOutSerialzier(dateinout, many=True)
        locationserializer = LocationSerializer(location, many=True)
        s = [scheduledateinout.data]
        d = dateinoutschedule.data
        l = locationserializer.data
        # schedulecheckinout = s.update(d)
        schedulecheckinout = s + d + l
        return Response(schedulecheckinout)

    # elif request.method == 'PUT':
    #     pass
    #     # serializer = ScheduleViewSerializer(Schedule, data=request.data)
    #     # if serializer.is_valid():
    #     #     serializer.save()
    #     #     return Response(serializer.data)
    #     # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # elif request.method == 'DELETE':
    #     pass
    #     # schedule.delete()
    #     # return Response(status=status.HTTP_204_NO_CONTENT)


# ####################### Schedule CheckInOut ##############################

@api_view(['GET'])
def ScheduleLocation(request):
    permission_classes = (AllowAny,)
    schedule = Schedule.objects.all()
    scheduledateinout = ScheduleDateInOutSerializer(schedule, many=True)
    checkinout = Location.objects.all()
    location = LocationSerializer(checkinout, many=True)
    schedulecheckinout = scheduledateinout.data + location.data

    return Response(schedulecheckinout)


######################### Schedule CheckInOut ##############################


#
#
#
# class IsCV(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.UserIDCurriculumVitae == request.user
#
#
# class CVViewSet(viewsets.ModelViewSet):
#     parser_classes = [MultiPartParser, FormParser]
#     serializer_class = CVSerializer
#     permission_classes = (IsCV,)
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return CV.objects.filter(UserIDCurriculumVitae=user)
#         raise PermissionDenied()
#
#     def perform_create(self, serializer):
#         user = self.request.user
#         employee = Employee.objects.get(UserIDEmployee=user)
#         serializer.save(UserIDCurriculumVitae=self.request.user, EmployeeIDCurriculumVitae=employee)
#


# ########################################### Employee Career #########################################
class IsCareer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDCareer == request.user


class CareerViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CareerSerializer
    permission_classes = (IsCareer,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Career.objects.filter(UserIDCareer=user)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(UserIDEmployee=user)
        serializer.save(UserIDCareer=self.request.user, EmployeeIDCareer=employee)
