from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from Employer.serializers import EmployerCompanySerializer
from connectdata.models import Employer, Company
from Employer.serializers import *


################################# EMPLOYER #######################################

############################# EMPLOYER COMPANY ###################################

class IsUserCompany(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDCompany == request.user


class EmployerCompany(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = EmployerCompanySerializer
    permission_classes = (IsUserCompany,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Company.objects.filter(UserIDCompany=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        employer = Employer.objects.get(UserIDEmployer=user)
        serializer.save(UserIDCompany=self.request.user, EmployerIDCompany=employer)


############################# EMPLOYER COMPANY ###################################

############################### EMPLOYER JOB #####################################

class IsJobs(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDJob == request.user


class JobViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = EmployerJobsSerializer
    permission_classes = (IsJobs,)

    # Ensure a user sees only own Note objectsu.
    def get_queryset(self):
        user = self.request.user
        employer = Employer.objects.get(UserIDEmployer=user)
        if user.is_authenticated:
            return Jobs.objects.filter(UserIDJob=user).filter(EmployerIDJob=employer)
        raise PermissionDenied()

    # Set user as owner of a Notes object.
    def perform_create(self, serializer):
        user = self.request.user
        employer = Employer.objects.get(UserIDEmployer=user)
        serializer.save(UserIDJob=user, EmployerIDJob=employer)


############################### EMPLOYER JOB #####################################

############################### Schedule JOB #####################################

class isScheduleJob(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDShedule == request.user


class ScheduleJob(viewsets.ModelViewSet):
    serializer_class = ScheduleJobSerializer
    permission_classes = (isScheduleJob,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # company = Company.objects.get()
            return Schedule.objects.filter(UserIDShedule=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        employer = Employer.objects.get(UserIDEmployer=user)
        serializer.save(UserIDShedule=self.request.user, EmlpoyerIDSchedule=employer)


############################### Schedule JOB #####################################

################################# JOB APPLY#######################################

class JobApplyCV(viewsets.ModelViewSet):
    serializer_class = EmployerJobApplySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # company = Company.objects.get()
            return JobApply.objects.filter(UserIDJobCreate=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        employer = Employer.objects.get(UserIDEmployer=user)
        serializer.save(UserIDJobCreate=self.request.user, EmployerIDJobApply=employer)

    def create(self, request):
        pass


################################# JOB APPLY#######################################

################################# JOB APPLY#######################################
class isJobApply(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDJobCreate == request.user


class EmployerJobApplyCV(APIView):
    permission_classes = (isJobApply,)
    queryset = JobApply.objects.all()
    serializer_class = EmployerJobApplyCVSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            t = JobApply.objects.filter(UserIDJobCreate=user).first()
            if t is not None:
                return t

        raise PermissionDenied()

    def get_object(self, idjob):
        try:
            # userlogin = self.request.user
            # print(userlogin)
            # userjob = JobApply.objects.filter(JobIDJobApply=idjob)
            # # usercreate = userjob.UserIDJobCreate
            # # print(usercreate)
            queryset = self.get_queryset()
            if queryset is None:
                # print((userlogin != usercreate))
                return Response({"error": "Not Authentications or Not Create Jobs."}, status=404)
            return JobApply.objects.filter(JobIDJobApply=idjob)
        except JobApply.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, idjob=None):
        user = self.request.user
        print(user)
        instance = self.get_object(idjob)
        serailizer = EmployerJobApplyCVSerializer(instance, many=True, )
        return Response(serailizer.data)


class EmployerJobApply(ListAPIView):
    permission_classes = (isJobApply,)
    queryset = JobApply.objects.all()
    serializer_class = EmployerJobApplySerializer

    def get_queryset(self):
        # user = self.request.user
        # if user.is_authenticated:
        #     return JobApply.objects.filter(UserIDJobCreate=user)
        # raise PermissionDenied()
        user = self.request.user
        if user.is_authenticated:
            t = JobApply.objects.filter(UserIDJobCreate=user).first()
            if t is not None:
                return t

        raise PermissionDenied()

    def get_object(self, id=None):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return JobApply.objects.get(id=id)
        except JobApply.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = EmployerJobApplySerializer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = EmployerJobApplySerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


################################# JOB APPLY#######################################

########################## SCHEDULE JOB DATE INOUT ###############################

class isScheduleDateInOut(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDShedule == request.user


class ScheduleDateInOut(viewsets.ModelViewSet):
    serializer_class = ScheduleDateInOutSerializer
    permission_classes = (isScheduleDateInOut,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Schedule.objects.filter(UserIDShedule=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        # company = Company.objects.get(UserIDCompany=user)
        employer = Employer.objects.get(UserIDEmployer=user)
        serializer.save(UserIDShedule=user,
                        EmployerIDSchedule=employer,
                        # CompanyIDSchedule=company
                        )


########################## SCHEDULE JOB DATE INOUT ###############################

############################ SCHEDULE DATE INOUT #################################

class ScheduleDateTime(viewsets.ModelViewSet):
    serializer_class = ScheduleDateTimeSerializer
    permission_classes = (isScheduleJob,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # company = Company.objects.get()
            return Schedule.objects.filter(UserIDShedule=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        # company = Company.objects.get(UserIDCompany=user)
        employer = Employer.objects.get(UserIDEmployer=user)
        serializer.save(UserIDShedule=self.request.user,
                        EmployerIDSchedule=employer,
                        # CompanyIDSchedule=company
                        )


############################ SCHEDULE DATE INOUT #################################

############################## DATEINOUT INOUT ###################################

class isInOut(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDInOut == request.user


class InOutShift(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = InoutDateInOutSerializer
    permission_classes = (isInOut,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return InOut.objects.filter(UserIDInOut=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        # company = Company.objects.get(UserIDCompany=user)
        employer = Employer.objects.get(UserIDEmployer=user)
        # schedule = Schedule.objects.get(UserIDShedule=user)
        serializer.save(UserIDInOut=user,
                        EmployerIDInOut=employer,
                        # CompanyIDInOut=company,
                        # ScheduleIDInOut=schedule
                        )


############################## DATEINOUT INOUT ###################################


######################## Schedule DateInOut InOut ################################

####################### UPDATE SCHEDULE JOB DATE INOUT ###########################


class isScheduleDateInOutNested(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDSchedule == request.user


class ScheduleDateInOutNested(viewsets.ModelViewSet):
    serializer_class = ScheduleDateInOutNested
    permission_classes = (isScheduleDateInOutNested,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Schedule.objects.filter(UserIDShedule=user)
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        employer = Employer.objects.get(UserIDEmployer=user)
        serializer.save(UserIDShedule=user,
                        EmployerIDSchedule=employer,
                        )


######################## Schedule DateInOut InOut ################################

##################### LIST Schedule DateInOut InOut ##############################

@api_view(['GET'])
def ScheduleDateInOutList(request, pk):
    try:
        schedule = get_object_or_404(Schedule, id=pk)
        inout = InOut.objects.filter(UserIDInOut=schedule.UserIDShedule)
        dateinout = DateInOut.objects.filter(UserIDDateInOut=schedule.UserIDShedule)

    except Schedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        scheduledateinout = ScheduleDateInOutNestedList(schedule)
        dateinoutschedule = DateInOutNested(dateinout, many=True)
        inoutschedule = InOutNested(inout, many=True)
        s = [scheduledateinout.data]
        d = dateinoutschedule.data
        l = inoutschedule.data
        schedulecheckinout = s + d + l
        return Response(schedulecheckinout)


##################### LIST Schedule DateInOut InOut ##############################


#
#
# # *********************************** Employer Bank User **************************************
# class IsUserBank(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.UserIDUserBank == request.user
#
#
# class EmployerUserBankFullViewSet(viewsets.ModelViewSet):
#     serializer_class = EmployerUserBankViewSetSerializer
#     permission_classes = (IsUserBank,)
#
#     # Ensure a user sees only own Note objectsu.
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return UserBank.objects.filter(UserIDUserBank=user)
#         raise PermissionDenied()
#
#     # Set user as owner of a Notes object.
#     def perform_create(self, serializer):
#         user = self.request.user
#         employer = Employer.objects.get(UserIDEmployer=user)
#         serializer.save(UserIDUserBank=self.request.user, EmployerIDUserBank=employer)
#
#
# # **************************************  User Company ****************************************
#
#
# # ############################################### Schedule ##########################################################
# class IsUserSchedule(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.UserIDSchedule == request.user
#
#
# class EmployerScheduleFullViewSet(viewsets.ModelViewSet):
#     parser_classes = [MultiPartParser, FormParser]
#     serializer_class = EmployerScheduleViewSetSerializer
#     permission_classes = (IsUserSchedule,)
#
#     # Ensure a user sees only own Note objectsu.
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Schedule.objects.filter(UserIDSchedule=user)
#         raise PermissionDenied()
#
#     # Set user as owner of a Notes object.
#     def perform_create(self, serializer):
#         user = self.request.user
#         employer = Employer.objects.get(UserIDEmployer=user)
#         serializer.save(UserIDSchedule=self.request.user, EmployerIDSchedule=employer)
#
#
# # ***************************************** Employer - Address **************************************
# # class IsUserAddress(permissions.BasePermission):
# #     def has_object_permission(self, request, view, obj):
# #         return obj.UserIDAddress == request.user
# #
# #
# # class EmployerAddressFullViewSet(viewsets.ModelViewSet):
# #     parser_classes = [MultiPartParser, FormParser]
# #     serializer_class = EmployerAdressViewSetSerializer
# #     permission_classes = (IsUserAddress,)
# #
# #     # Ensure a user sees only own Note objectsu.
# #     def get_queryset(self):
# #         user = self.request.user
# #         if user.is_authenticated:
# #             return Address.objects.filter(UserIDAddress=user)
# #         raise PermissionDenied()
# #
# #     # Set user as owner of a Notes object.
# #     def perform_create(self, serializer):
# #         user = self.request.user
# #         employer = Employer.objects.get(UserIDEmployer=user)
# #         serializer.save(UserIDAddress=self.request.user, EmployerIDAddress=employer)
#
#
# # ***************************************** Employer Jobs ************************************************

#
#
# # ############################################### InOut ##########################################################
# class IsUserInOut(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.UserIDInOut == request.user
#
#
# class EmployerInOutFullViewSet(viewsets.ModelViewSet):
#     parser_classes = [MultiPartParser, FormParser]
#     serializer_class = EmployerInOutViewSetSerializer
#     permission_classes = (IsUserInOut,)
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
#         serializer.save(UserIDInOut=self.request.user, EmployerIDInOut=employer)
#
#
# # ################################################ BANK ############################################################
# # ******************************** Get Employer - Bank **************************************
#
# class EmployerUserBankFullView(ListAPIView):
#     # permission_classes = (AllowAny,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Employer.objects.all()
#     serializer_class = EmployerUserBankDetailSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Employer.objects.filter(UserIDEmployer=user)
#         raise PermissionDenied()
#
#     def get(self, request):
#         queryset = self.get_queryset()
#         # qr = profile.objects.all()
#         serializer = EmployerUserBankDetailSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#
# # ********************************************** Detail Emplyee - Bank ************************************************
# class EmployerUserBankDetailView(APIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Employer.objects.all()
#     serializer_class = EmployerUserBankDetailSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Employer.objects.filter(UserIDEmployer=user)
#         raise PermissionDenied()
#
#     def get_object(self, id):
#         try:
#             queryset = self.get_queryset()
#             if queryset is None:
#                 return Response({"error": "Not Authentications."}, status=404)
#             return Employer.objects.get(id=id)
#         except Employer.DoesNotExist as e:
#             return Response({"error": "Given question object not found."}, status=404)
#
#     def get(self, request, id=None):
#         instance = self.get_object(id)
#         serailizer = EmployerUserBankDetailSerializer(instance)
#         return Response(serailizer.data)
#
#     def put(self, request, id=None):
#         data = request.data
#         instance = self.get_object(id)
#         serializer = EmployerUserBankDetailSerializer(instance, data=data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)
#
#     def delete(self, request, id=None):
#         instance = self.get_object(id)
#         instance.delete()
#         return HttpResponse(status=204)
#
#
# # ################################################ COMPANY ############################################################
#
# # ******************************** Get - Employer - Company *************************************
# class EmployerCompanyFullView(ListAPIView):
#     # permission_classes = (AllowAny,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Employer.objects.all()
#     serializer_class = EmployerCompanyDetailSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Employer.objects.filter(UserIDEmployer=user)
#         raise PermissionDenied()
#
#     def get(self, request):
#         queryset = self.get_queryset()
#         # qr = profile.objects.all()
#         serializer = EmployerCompanyDetailSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#
# # ******************************** Detail - Employer - Company *************************************
# class EmployerCompanyDetailView(APIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Employer.objects.all()
#     serializer_class = EmployerCompanyDetailSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Employer.objects.filter(UserIDEmployer=user)
#         raise PermissionDenied()
#
#     def get_object(self, id):
#         try:
#             queryset = self.get_queryset()
#             if queryset is None:
#                 return Response({"error": "Not Authentications."}, status=404)
#             return Employer.objects.get(id=id)
#         except Employer.DoesNotExist as e:
#             return Response({"error": "Given question object not found."}, status=404)
#
#     def get(self, request, id=None):
#         instance = self.get_object(id)
#         serailizer = EmployerCompanyDetailSerializer(instance)
#         return Response(serailizer.data)
#
#     def put(self, request, id=None):
#         data = request.data
#         instance = self.get_object(id)
#         serializer = EmployerCompanyDetailSerializer(instance, data=data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)
#
#     def delete(self, request, id=None):
#         instance = self.get_object(id)
#         instance.delete()
#         return HttpResponse(status=204)
#
#
# # ################################################ COMPANY ############################################################
#
#
# # *********************************** Employer - Address ****************************************
#
#
# class EmployerAddressFullView(ListAPIView):
#     # permission_classes = (AllowAny,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Employer.objects.all()
#     serializer_class = EmployerAddressDetailSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Employer.objects.filter(UserIDEmployer=user)
#         raise PermissionDenied()
#
#     def get(self, request):
#         queryset = self.get_queryset()
#         # qr = profile.objects.all()
#         serializer = EmployerAddressDetailSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#
# # ******************************** Detail - Employer - Address *************************************
# class EmployerAddressDetailView(APIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Employer.objects.all()
#     serializer_class = EmployerAddressDetailSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Employer.objects.filter(UserIDEmployer=user)
#         raise PermissionDenied()
#
#     def get_object(self, id):
#         try:
#             queryset = self.get_queryset()
#             if queryset is None:
#                 return Response({"error": "Not Authentications."}, status=404)
#             return Employer.objects.get(id=id)
#         except Employer.DoesNotExist as e:
#             return Response({"error": "Given question object not found."}, status=404)
#
#     def get(self, request, id=None):
#         instance = self.get_object(id)
#         serailizer = EmployerAddressDetailSerializer(instance)
#         return Response(serailizer.data)
#
#     def put(self, request, id=None):
#         data = request.data
#         instance = self.get_object(id)
#         serializer = EmployerAddressDetailSerializer(instance, data=data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)
#
#     def delete(self, request, id=None):
#         instance = self.get_object(id)
#         instance.delete()
#         return HttpResponse(status=204)
#
#
# # ################################################ JOBS ##############################################################
#
# # *********************************** Employer - JOBS ****************************************
#
#
# class EmployerJobsFullView(ListAPIView):
#     # permission_classes = (AllowAny,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Employer.objects.all()
#     serializer_class = EmployerJobDetailSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Employer.objects.filter(UserIDEmployer=user)
#         raise PermissionDenied()
#
#     def get(self, request):
#         queryset = self.get_queryset()
#         # qr = profile.objects.all()
#         serializer = EmployerJobDetailSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#
# # ******************************** Detail - Employer - JOBs *************************************
# class EmployerJobsDetailView(APIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Employer.objects.all()
#     serializer_class = EmployerJobDetailSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Employer.objects.filter(UserIDEmployer=user)
#         raise PermissionDenied()
#
#     def get_object(self, id):
#         try:
#             queryset = self.get_queryset()
#             if queryset is None:
#                 return Response({"error": "Not Authentications."}, status=404)
#             return Employer.objects.get(id=id)
#         except Employer.DoesNotExist as e:
#             return Response({"error": "Given question object not found."}, status=404)
#
#     def get(self, request, id=None):
#         instance = self.get_object(id)
#         serailizer = EmployerJobDetailSerializer(instance)
#         return Response(serailizer.data)
#
#     def put(self, request, id=None):
#         data = request.data
#         instance = self.get_object(id)
#         serializer = EmployerJobDetailSerializer(instance, data=data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)
#
#     def delete(self, request, id=None):
#         instance = self.get_object(id)
#         instance.delete()
#         return HttpResponse(status=204)
#
#
# # ################################################ INOUT ##############################################################
# class EmployerInOutFullView(ListAPIView):
#     # permission_classes = (AllowAny,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Employer.objects.all()
#     serializer_class = EmployerInOutDetailSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Employer.objects.filter(UserIDEmployer=user)
#         raise PermissionDenied()
#
#     def get(self, request):
#         queryset = self.get_queryset()
#         # qr = profile.objects.all()
#         serializer = EmployerInOutDetailSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#
# # ******************************** Detail - Employer - INOUT *************************************
# class EmployerInOutDetailView(APIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Employer.objects.all()
#     serializer_class = EmployerInOutDetailSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Employer.objects.filter(UserIDEmployer=user)
#         raise PermissionDenied()
#
#     def get_object(self, id):
#         try:
#             queryset = self.get_queryset()
#             if queryset is None:
#                 return Response({"error": "Not Authentications."}, status=404)
#             return Employer.objects.get(id=id)
#         except Employer.DoesNotExist as e:
#             return Response({"error": "Given question object not found."}, status=404)
#
#     def get(self, request, id=None):
#         instance = self.get_object(id)
#         serailizer = EmployerInOutDetailSerializer(instance)
#         return Response(serailizer.data)
#
#     def put(self, request, id=None):
#         data = request.data
#         instance = self.get_object(id)
#         serializer = EmployerInOutDetailSerializer(instance, data=data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)
#
#     def delete(self, request, id=None):
#         instance = self.get_object(id)
#         instance.delete()
#         return HttpResponse(status=204)
#
#
# # ################################################ Schedule ##############################################################
# class EmployerScheduleFullView(ListAPIView):
#     # permission_classes = (AllowAny,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Employer.objects.all()
#     serializer_class = EmployerScheduleDetailSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Employer.objects.filter(UserIDEmployer=user)
#         raise PermissionDenied()
#
#     def get(self, request):
#         queryset = self.get_queryset()
#         # qr = profile.objects.all()
#         serializer = EmployerInOutDetailSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#
# # ******************************** Detail - Employer - INOUT *************************************
# class EmployerScheduleDetailView(APIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Employer.objects.all()
#     serializer_class = EmployerScheduleDetailSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             return Employer.objects.filter(UserIDEmployer=user)
#         raise PermissionDenied()
#
#     def get_object(self, id):
#         try:
#             queryset = self.get_queryset()
#             if queryset is None:
#                 return Response({"error": "Not Authentications."}, status=404)
#             return Employer.objects.get(id=id)
#         except Employer.DoesNotExist as e:
#             return Response({"error": "Given question object not found."}, status=404)
#
#     def get(self, request, id=None):
#         instance = self.get_object(id)
#         serailizer = EmployerScheduleDetailSerializer(instance)
#         return Response(serailizer.data)
#
#     def put(self, request, id=None):
#         data = request.data
#         instance = self.get_object(id)
#         serializer = EmployerScheduleDetailSerializer(instance, data=data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)
#
#     def delete(self, request, id=None):
#         instance = self.get_object(id)
#         instance.delete()
#         return HttpResponse(status=204)


class ScheduleDatelist(ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ScheduleDatelistSerializer
    queryset = Schedule.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serilizer = ScheduleDatelistSerializer(queryset, many=True)
        return Response(serilizer.data, status=200)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ScheduleDate(ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ScheduleDateSerializer
    queryset = Schedule.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serilizer = ScheduleDateSerializer(queryset, many=True)
        return Response(serilizer.data, status=200)


class ScheduleDateDetailView(APIView):
    permission_classes = (AllowAny,)
    queryset = Schedule.objects.all()
    serializer_class = ScheduleDateSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Schedule.objects.filter(UserIDShedule=user)
        raise PermissionDenied()

    def get_object(self, id):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                return Response({"error": "Not Authentications."}, status=404)
            return Schedule.objects.get(id=id)
        except Schedule.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = ScheduleDateSerializer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = ScheduleDateSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)
