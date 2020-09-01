from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter

from addressgojoco.views import *
    # CountryViewSet, ProvinceCityViewSet, DistrictViewSet, WardViewSet, LanguageUserViewSet, \
    # CountryList

router = SimpleRouter()

router.register("CountryViewSet", CountryViewSet, basename="CountryViewSet")
router.register("ProvinceCityViewSet", ProvinceCityViewSet, basename="ProvinceCityViewSet")
router.register("DistrictViewSet", DistrictViewSet, basename="DistrictViewSet")
router.register("WardViewSet", WardViewSet, basename="WardViewSet")
router.register("LanguageUserViewSet", LanguageUserViewSet, basename="LanguageUserViewSet")

# ############################################## Career #############################################
# ############################################## MainCareer #############################################
router.register("MainCareerViewSet", MainCareerViewSet, basename="MainCareerViewSet")
# ############################################## Level1Career #############################################
router.register("Level1CareerViewSet", Level1CareerViewSet, basename="Level1CareerViewSet")
# ############################################## Level2Career #############################################
router.register("Level2CareerViewSet", Level2CareerViewSet, basename="Level2CareerViewSet")
# ############################################## Level3Career #############################################
router.register("Level3CareerViewSet", Level3CareerViewSet, basename="Level3CareerViewSet")

urlpatterns = [
    path("", include(router.urls)),
    path('country/', CountryList.as_view(), name='CountryList'),
    path('country/<int:id>/', CountryDetail.as_view(), name='CountryDetail'),
    path('provincecity/', ProvinceCityList.as_view(), name='ProvinceCityList'),
    path('provincecity/<int:id>/', ProvinceCityDetail.as_view(), name='ProvinceCityDetail'),
    path('district/', DistrictList.as_view(), name='DistrictList'),
    path('district/<int:id>/', DistrictDetail.as_view(), name='DistrictDetail'),
    path('ward/', WardList.as_view(), name='WardList'),
    path('ward/<int:id>/', WardDetail.as_view(), name='WardDetail'),

]