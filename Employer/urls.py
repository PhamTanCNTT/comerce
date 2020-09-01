from django.urls import path, include
from employee.views import *

from rest_framework.routers import SimpleRouter, DefaultRouter

from Employer.views import *

router = SimpleRouter()

router = SimpleRouter()

############################# EMPLOYER COMPANY ###################################

router.register("EmployerCompany", EmployerCompany, basename="EmployerCompany")

############################ EMPLOYER COMPANY ###################################

############################## Schedule JOB #####################################

router.register("ScheduleJob", ScheduleJob, basename="ScheduleJob")

############################## Schedule JOB #####################################

############################## EMPLOYER JOB #####################################

router.register("JobViewSet", JobViewSet, basename="JobViewSet")

# router.register("EmployerJobApply", EmployerJobApply, basename="EmployerJobApply")

router.register("JobApplyCV", JobApplyCV, basename="JobApplyCV")

############################## EMPLOYER JOB #####################################

########################## SCHEDULE JOB DATE INOUT ##############################

router.register("ScheduleDateInOut", ScheduleDateInOut, basename="ScheduleDateInOut")

########################## SCHEDULE JOB DATE INOUT ##############################

############################ SCHEDULE DATE INOUT #################################

router.register("ScheduleDateTime", ScheduleDateTime, basename="ScheduleDateTime")

# router.register("ScheduleDate", ScheduleDate, basename="ScheduleDate")


############################ SCHEDULE DATE INOUT #################################

############################## DATEINOUT INOUT ###################################

router.register("InOutShift", InOutShift, basename="InOutShift")

############################## DATEINOUT INOUT ###################################

############################## DATEINOUT INOUT ###################################



router.register("ScheduleDateInOutNested", ScheduleDateInOutNested, basename="ScheduleDateInOutNested")

############################## DATEINOUT INOUT ###################################



#
# # ########################################### EMPLOYER #######################################################
# # ************************************* Employer Bank User***********************************************
# router.register("EmployerUserBankFullViewSet", EmployerUserBankFullViewSet, basename="EmployerUserBankFullViewSet")
#
# # # **************************************** Employer Address ****************************************************
# # router.register("EmployerAddressFullViewSet", EmployerAddressFullViewSet, basename="EmployerAddressFullViewSet")
#
# # **************************************** Employer Jobs ****************************************************
# router.register("EmployerJobsFullViewSet", EmployerJobsFullViewSet, basename="EmployerJobsFullViewSet")
#
# # **************************************** Employer Schedule ****************************************************
# router.register("EmployerScheduleFullViewSet", EmployerScheduleFullViewSet, basename="EmployerScheduleFullViewSet")
#
# # **************************************** Employer InOut ****************************************************
# router.register("EmployerInOutFullViewSet", EmployerInOutFullViewSet, basename="EmployerInOutFullViewSet")

urlpatterns = [
    path("", include(router.urls)),

############################## EMPLOYER JOB #####################################

    path('EmployerJobApply/<int:id>/', EmployerJobApply.as_view(), name='EmployerJobApply'),
    # Confirm CV selected
    path('EmployerJobApplyCV/<int:idjob>/', EmployerJobApplyCV.as_view(), name='EmployerJobApplyCV'),
    # Get All CV Applied for Job
    path('ScheduleDateInOutList/<int:pk>/', ScheduleDateInOutList, name="ScheduleDateInOutList"),

    path('ScheduleDatelist/', ScheduleDatelist.as_view(), name="ScheduleDatelist"),
    path('ScheduleDate/', ScheduleDate.as_view(), name="ScheduleDate"),
    path('ScheduleDate/<int:id>/', ScheduleDateDetailView.as_view(), name="ScheduleDateDetailView"),



############################## EMPLOYER JOB #####################################

    # # ******************************** BANK **********************************************
    # path('EmployerUserBankFullView/', EmployerUserBankFullView.as_view(), name='EmployerBankVSView'),
    # path('EmployerUserBankDetailView/', EmployerUserBankDetailView.as_view(), name='EmployerUserBankDetailView'),
    #
    # # ******************************** COMPANY *******************************************
    # path('EmployerCompanyFullView/', EmployerCompanyFullView.as_view(), name='EmployerCompanyFullView'),
    # path('EmployerCompanyDetailView/<int:id>/', EmployerCompanyDetailView.as_view(),
    #      name='EmployerCompanyDetailView'),
    #
    # # *********************************** Address ******************************************
    # path('EmployerAddressFullView/', EmployerAddressFullView.as_view(), name='EmployerAddressFullView'),
    # path('EmployerAddressDetailView/<int:id>/', EmployerAddressDetailView.as_view(),
    #      name='EmployerAddressDetailView'),
    #
    # # *********************************** JOBS ******************************************
    # path('EmployerJobsFullView/', EmployerJobsFullView.as_view(), name='EmployeeJobsVSView'),
    # path('EmployerJobsDetailView/<int:id>/', EmployerJobsDetailView.as_view(), name='EmployerJobsDetailView'),
    #
    # # *********************************** Schedule ******************************************
    # path('EmployerScheduleFullView/', EmployerScheduleFullView.as_view(), name='EmployerScheduleFullView'),
    # path('EmployerScheduleDetailView/<int:id>/', EmployerScheduleDetailView.as_view(), name='EmployerScheduleDetailView'),
    #
    # # *********************************** InOut ******************************************
    # path('EmployerInOutFullView/', EmployerInOutFullView.as_view(), name='EmployeeInOutVSView'),
    # path('EmployerInOutDetailView/<int:id>/', EmployerInOutDetailView.as_view(), name='EmployerInOutDetailView'),
    #

]
