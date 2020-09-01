from django.urls import path, include
from django.contrib import admin
from django.urls import path, re_path
from connectdata import views
from connectdata.views import *
from .views import NoteViewSet, ConnectViewAll, CourseListViewSet, CompanyViewSet, ProfileUserViewSet, UserBankFullViewSet


from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register("connectdata", NoteViewSet, basename="connectdata")
router.register("CourseListViewSet", CourseListViewSet, basename="CourseListViewSet")
router.register("CourseCompanySerializerViewSet", CourseCompanySerializerViewSet, basename="CourseCompanySerializerViewSet")
router.register("CompanyViewSet", CompanyViewSet, basename="CompanyViewSet")
router.register("ScheduleCVViewSet", ScheduleCVViewSet, basename="ScheduleCVViewSet")

router.register("ProfileFullCheckViewSet", ProfileFullCheckViewSet, basename="ProfileFullCheckViewSet")

################################ Address ######################################

router.register("address", AddressViewSet, basename="AddressViewSet")

################################ Address ######################################

########################### Employee Education #################################

router.register("EmployeeEducationViewSet", EmployeeEducationViewSet, basename="EmployeeEducationViewSet")

################################ EmployeeEducation ######################################

################################ EmployeeEducation ######################################

router.register("EmployeeCareerViewSet", EmployeeCareerViewSet, basename="EmployeeCareerViewSet")

################################ EmployeeEducation ######################################

router.register("WorkLocationViewSet", WorkLocationViewSet, basename="WorkLocationViewSet")

################################ EmployeeEducation ######################################

################################ EmployeeEducation ####View##################################


##################################/////// Profile User\\\\\\\\\\\\#####################################
router.register("ProfileUserViewSet", ProfileUserViewSet, basename="ProfileUserViewSet")
router.register("ProfileUserViewSetToken", ProfileUserViewSetToken, basename="ProfileUserViewSetToken")
router.register("profilecmnd1", ProfileUserCMND1, basename="ProfileUserCMND1")
router.register("profilecmnd2", ProfileUserCMND2, basename="ProfileUserCMND2")



router.register("CreateProfileViewSet", CreateProfileViewSet, basename="CreateProfileViewSet")
##################################/////// Profile User\\\\\\\\\\\\#####################################

##################################/////// Bank User\\\\\\\\\\\\#####################################
router.register("UserBankFullViewSet", UserBankFullViewSet, basename="UserBankFullViewSet")
router.register("UserEducationViewSet", UserEducationViewSet, basename="UserEducationViewSet")

##################################/////// Bank User\\\\\\\\\\\\#####################################

##################################/////// Create Employee \\\\\\\\\\\\#####################################
router.register("CreateEmployeeViewSet", CreateEmployeeViewSet, basename="CreateEmployeeViewSet")
router.register("EmployeeAttPhotoViewSet", EmployeeAttPhotoViewSet, basename="EmployeeAttPhotoViewSet")
router.register("AttPhotoEmployeeFullViewSet", AttPhotoEmployeeFullViewSet, basename="AttPhotoEmployeeFullViewSet")

##################################/////// Create Employee \\\\\\\\\\\\#####################################

##################################/////// Create Employer \\\\\\\\\\\\#####################################
router.register("CreateEmployerViewSet", CreateEmployerViewSet, basename="CreateEmployerViewSet")
##################################/////// Create Employer \\\\\\\\\\\\#####################################

##################################/////// Create Employer \\\\\\\\\\\\#####################################
router.register("AttPhotoUserViewSet", AttPhotoUserViewSet, basename="AttPhotoUserViewSet")
##################################/////// Create Employer \\\\\\\\\\\\#####################################


##################################/////// Create CV \\\\\\\\\\\\#####################################
router.register("CurriculumVitaeEducationViewSet", CurriculumVitaeEducationViewSet, basename="CurriculumVitaeEducationViewSet")
router.register("CVEmployeeExperiencesViewSet", CVEmployeeExperiencesViewSet, basename="CVEmployeeExperiencesViewSet")

router.register("CVManyToMany", CVManyToMany, basename="CVManyToMany")

# router.register("CVEducationViewSet", CVEducationViewSet, basename="CVEducationViewSet")

router.register("CVViewSet", CVViewSet, basename="CVViewSet")


router.register("CVFinishViewSet", CVFinishViewSet, basename="CVFinishViewSet")
router.register("EmployeeCVViewSet", EmployeeCVViewSet, basename="EmployeeCVViewSet")



##################################/////// Create Employer \\\\\\\\\\\\#####################################

########################## Khong Phan Quyen ManyToMany CV - Edu ################################


router.register("EducationViewSet", EducationViewSet, basename="EducationViewSet")
router.register("CurriculumVitaeViewSet", CurriculumVitaeViewSet, basename="CurriculumVitaeViewSet")


########################## Khong Phan Quyen ManyToMany CV - Edu ################################

################################ Education - Employee ###########################################

########################## Create Update Full - EduEmployee ################################

# Use

router.register("EducationFullEmployeeViewSet", EducationFullEmployeeViewSet, basename="EducationFullEmployeeViewSet")

########################## Create Update Full Full - EduEmployee ################################

########################## Create Update Full - ExperienceEmployee ################################
# Use

router.register("ExperienceFullEmployeeViewSet", ExperienceFullEmployeeViewSet, basename="ExperienceFullEmployeeViewSet")

########################## Create Update Full Full - ExperienceEmployee ################################
########################## Create Update Full - ECareerViewSet ################################
# Use

router.register("CareerViewSet", CareerViewSet, basename="CareerViewSet")

########################## Create Update Full Full - ExperienceEmployee ################################

########################## Create Update Full - WorkLocationViewSet ################################
# Use

router.register("WorkLocationViewSet", WorkLocationViewSet, basename="WorkLocationViewSet")

########################## Create Update Full Full - WorkLocationViewSet ################################



# ########################################### EMPLOYER #######################################################
# # ************************************* Employer Bank User***********************************************
# router.register("EmployerUserBankFullViewSet", EmployerUserBankFullViewSet, basename="EmployerUserBankFullViewSet")
#
# # **************************************** Employer Company ****************************************************
# router.register("EmployerCompayFullViewSet", EmployerCompayFullViewSet, basename="EmployerCompayFullViewSet")
#
# # # **************************************** Employer Address ****************************************************
# # router.register("EmployerAddressFullViewSet", EmployerAddressFullViewSet, basename="EmployerAddressFullViewSet")
# # **************************************** Employer Jobs ****************************************************
# router.register("EmployerJobsFullViewSet", EmployerJobsFullViewSet, basename="EmployerJobsFullViewSet")
# # # **************************************** Employer Inout ****************************************************
# # router.register("EmployerInoutFullViewSet", EmployerInoutFullViewSet, basename="EmployerInoutFullViewSet")


# # **************************************** Employer Address ****************************************************
router.register("CheckInOutViewSet", CheckInOutViewSet, basename="CheckInOutViewSet")

# # **************************************** Employer Address ****************************************************

# # **************************************** Location Address ****************************************************
router.register("LocationViewSet", LocationViewSet, basename="LocationViewSet")
router.register("CompanyEmployerViewSet", CompanyEmployerViewSet, basename="CompanyEmployerViewSet")

# # **************************************** Location Address ****************************************************


#router.register("CouresViewSet/<int:id>/", CourseListViewSet, basename="CourseListViewSet/<int:id>/")

urlpatterns = [
    #path("dataNote/", NoteViewSet, name="dataNote"),
    path("CourseListAPIView/", CourseListAPIView.as_view(), name="CourseListAPIView"),
    path("CourseListAPIView/<int:id>/", CourseDetailAPIView.as_view(), name="CourseDetailAPIView"),
    path("ComAllSerializerView/", ComAllSerializerView.as_view(), name="ComAllSerializerView"),
    path("CourseAllSerializerView/", CourseAllSerializerView.as_view(), name="CourseAllSerializerView"),
    path("ProfileUserViewAll/", ProfileUserViewAll.as_view(), name="ProfileUserViewAll"),
    path("ProfileUserViewNolog/", ProfileUserViewNolog.as_view(), name="ProfileUserViewNolog"),

################################ Update Edu of Employee for CV ##################################
    path("CVEducationViewSet/<int:pk>/", CVEducationViewSet.as_view(), name="CVEducationViewSet"),
    path("CVEducationList/", CVEducationList.as_view(), name="CVEducationList"),

    path("FinishCVAPIView/", FinishCVAPIView.as_view(), name="FinishCVAPIView"),

################################ Update Edu of Employee for CV ##################################

################################ Update Experience of Employee for CV ##################################
    path("CVExperienceAPIView/<int:pk>/", CVExperienceAPIView.as_view(), name="CVExperienceAPIView"),
################################ Update Experience of Employee for CV ##################################


    path("", include(router.urls)),
    path('ConnectViewAll/', ConnectViewAll.as_view(), name='ConnectViewAll'),
    # path('rest_courses/',  views.list_courses),
    re_path('rest_courses/(?P<code>\w+)/$', views.course_details),
    path('rest_client/', views.client),
    # test post long

    # path('api/DetailCourseCom/', DetailCourseComView.as_view(), name='DetailCourseComView'),
    path('api/getlong/', views.GetInnerCourseComView.as_view(), name="GetInnerCourseComView"),
    path('api/getlong/<int:pk>/', views.DetailCourseComView.as_view(), name="DetailCourseComView"),
    path('api/postlong/', views.PostCourseComView.as_view(), name="PostCourseComView"),
    path('rest_client_ajax/', views.client_ajax),
    # chay link api cua sep

    path('CourseSerializerAPIView/', views.CourseSerializerAPIView.as_view()),
    path('CourseSerializerLibAPIView/', views.CourseSerializerLibAPIView.as_view()),
    path('CompanySerializerAPIView/', views.CompanySerializerLibAPIView.as_view()),
    path('CourseCompanySerializerLibView/', views.CourseCompanySerializerLibView.as_view()),
    path('CourseCompanySerializerLibView/<int:id>/', views.CourseCompanySerializerLibDetail.as_view()),
    # api list title
    path('api/list/user/', views.ListUserAPIView.as_view()),
    path('manegecourse/', views.ajaxclient),
    path('xoa/', views.xoa),
    path('AjaxCourseCompnay/', views.AjaxCourseCompnay),
    path('getip/', views.getip),

    path('multigetip/', views.multigetip),


################################ Bank User#####################################
    path('UserBankFullViewAll/', views.UserBankFullViewAll.as_view()),
################################ Bank User#####################################

################################ Bank User#####################################
    path("ProfileImageAPIView/", ProfileImageAPIView.as_view(), name="ProfileImageAPIView"),
################################ Bank User#####################################


########################## Search CV: Address################################

path('SearchCV/', SearchCV.as_view(), name="SearchCV"),
########################## Search CV: Address################################

# ########################## Address ################################
# path('CountryView/', CountryView.as_view(), name="CountryView"),
# path('CountryView/<int:id>', CountryDetail.as_view(), name="CountryDetail"),
########################## Address################################

path('CountryFilter/', CountryFilter.as_view(), name="CountryFilter"),
path('ProvinceCityFilter/', ProvinceCityFilter.as_view(), name="ProvinceCityFilter"),
path('DistrictFilter/', DistrictFilter.as_view(), name="DistrictFilter"),
path('WardFilter/', WardFilter.as_view(), name="WardFilter"),


]