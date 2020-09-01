from django.urls import path, include
from employee.views import *
# EmployeeSimpleListView, EmployeeSimpleDetail, EmployeeBankVSView, EmployeeBankVSViewDetail, \
# cv, createcv, login_views, CVViewSet, JobApply, EmployeeJobApply, ScheduleCheckInOut, ScheduleLocation, \
# ScheduleCheckInOutDetail, mydash_views, employeeprofile

from .views import EmployeeBankFullViewSetABC, EmployeeBankVSViewSet
from . import views

from rest_framework.routers import SimpleRouter, DefaultRouter

router = SimpleRouter()
################################ CV ######################################

router.register("CVViewSet", CVViewSet, basename="CVViewSet")

################################ CV ######################################

############################# APPLY JOB ##################################

router.register("EmployeeJobApply", EmployeeJobApply, basename="EmployeeJobApply")

############################# APPLY JOB ##################################
# router.register("EmployeeBankViewSet", EmployeeBankViewSet, basename="EmployeeBankViewSet")
router.register("EmployeeBankFullViewSetABC", EmployeeBankFullViewSetABC, basename="EmployeeBankFullViewSetABC")
router.register("EmployeeBankVSViewSet", EmployeeBankVSViewSet, basename="EmployeeBankVSViewSet")


# ****************************************************************************************************************
# ############################################# EDUCATION ########################################################
router.register("EmployeeEducateFullViewSet", EmployeeEducateFullViewSet, basename="EmployeeEducateFullViewSet")
# ############################################# Experiences ######################################################
router.register("EmployeeExperiencesFullViewSet", EmployeeExperiencesFullViewSet,
                basename="EmployeeExperiencesFullViewSet")
# ############################################# EmployeeCVFullViewSet ############################################
router.register("EmployeeCVFullViewSet", EmployeeCVFullViewSet, basename="EmployeeCVFullViewSet")

# ############################################# Career ###########################################################
router.register("CareerViewSet", CareerViewSet, basename="CareerViewSet")


urlpatterns = [

    path("", include(router.urls)),  # Use for ViewSet
    path('EmployeeSimpleListView/', EmployeeSimpleListView.as_view(), name='EmployeeSimpleListView'),
    path('EmployeeSimpleListView/<int:id>/', EmployeeSimpleDetail.as_view(), name='EmployeeSimpleDetail'),

    ###########Nested Get - Post Employee - Bank ##########

    # path('EmployeeBankListView/', EmployeeBankListView.as_view(), name = 'EmployeeBankListView'),
    # path('EmployeeBankListView/<int:id>/', EmployBankDetail.as_view(), name = 'EmployBankDetail'),
    # path('EmployeeBankViewSetAll/', EmployeeBankViewSetAll.as_view(), name = 'EmployeeBankViewSetAll'),
    path('EmployeeBankVSView/', EmployeeBankVSView.as_view(), name='EmployeeBankVSView'),
    path('EmployeeBankVSView/<int:id>/', EmployeeBankVSViewDetail.as_view(), name='EmployeeBankVSViewDetail'),

    ###########Nested Get - Post Bank - Employee  ##########

    ###########Nested Get - Post Employee - Bank ##########

    # path('BankEmployListView/', BankEmployListView.as_view(), name = 'BankEmployListView'),

    ###########Nested Get - Post Bank - Employee ##########

    # ########## web CV ##########
    path('cv/', cv, name="cv"),
    path('createcv/', createcv, name="createcv"),
    path('login_views/', login_views, name="login_views"),

    # ###################### Profile Employee ##############################

    path('employeeprofile/', employeeprofile, name="employeeprofile"),
    path('listprofile/', listprofile, name="listprofile"),

    # ###################### Profile Employee ##############################

    path('basetest/', basetest, name="basetest"),
    path('employeebase/', employeebase, name="employeebase"),
    path('calender2/', calender2, name="calender2"),

    # ###################### Schedule CheckInOut ##############################

    path('ScheduleCheckInOut/', ScheduleCheckInOut, name="ScheduleCheckInOut"),
    path('ScheduleLocation/', ScheduleLocation, name="ScheduleLocation"),
    path('ScheduleCheckInOutDetail/<int:pk>/', ScheduleCheckInOutDetail, name="ScheduleCheckInOutDetail"),

    # ###################### Schedule CheckInOut ##############################

]
