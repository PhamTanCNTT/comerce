from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from connectdata.views import ProfileFullCheckViewSet
from .views import registration, registrationsocial, loginsocial, loginallauth, signallauth, ProfileFullViewAll, \
    UserUpdateSerializerDetail, xoa, registeruser, checkfunc, GJC_Login
from rest_framework.routers import SimpleRouter
from django.urls import path, re_path, include

from .views import ProfileFullViewSet

router = SimpleRouter()
router.register("ProfileFullViewSet", ProfileFullViewSet, basename="ProfileFullViewSet")
# router.register("ProfileFullCheckViewSet", ProfileFullCheckViewSet, basename="ProfileFullCheckViewSet")



urlpatterns = [
    path("", include(router.urls)),
    path("register/", registration, name="register"),
    path('UserUpdateSerializerDetail/<int:id>',  UserUpdateSerializerDetail.as_view(),
         name='UserUpdateSerializerDetail'),
    path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Account
    path('registersocial/', registrationsocial, name='registersocial'),
    path('loginsocial', loginsocial, name="loginsocial"),
    path('', loginallauth, name="loginallauth"),
    path('signallauth/', signallauth, name="signallauth"),
    path('ProfileFullViewAll/', ProfileFullViewAll, name="ProfileFullViewAll"),
    path('Index/', TemplateView.as_view(template_name="index.html")),
    path('xoa/', xoa, name="xoa"),
    path('registeruser/', registeruser, name="registeruser"),
    path('checkfunc/', checkfunc, name="checkfunc"),

    path('GJC_Login/', GJC_Login, name="GJC_Login"),

]
