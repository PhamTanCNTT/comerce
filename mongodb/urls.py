from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from jwtauth.views import loginsocial
########### JWT ###############
# from rest_framework_jwt.settings import api_settings
#
# if api_settings.JWT_AUTH_COOKIE:
#     from rest_framework_jwt.authentication import JSONWebTokenAuthentication
#     from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer
#     from rest_framework_jwt.views import RefreshJSONWebToken
#
#     RefreshJSONWebTokenSerializer._declared_fields.pop('token')
#
#     class RefreshJSONWebTokenSerializerCookieBased(RefreshJSONWebTokenSerializer):
#         def validate(self, attrs):
#             if 'token' not in attrs:
#                 if api_settings.JWT_AUTH_COOKIE:
#                     attrs['token'] = JSONWebTokenAuthentication().get_jwt_value(self.context['request'])
#             return super(RefreshJSONWebTokenSerializerCookieBased, self).validate(attrs)
#
#     RefreshJSONWebToken.serializer_class = RefreshJSONWebTokenSerializerCookieBased

########### JWT ###############




urlpatterns = [
    path('', loginsocial, name="loginsocial"),
    path('admin/', admin.site.urls),
    path('jwtauth/', include('jwtauth.urls')),

    path('connectdata/', include('connectdata.urls')),

    #Django Rest Framework
    path('auth/', include('rest_framework.urls')),
    ########AllAuth###############
    path('account/', include('allauth.urls')),
    path('employee/', include('employee.urls')),
    path('employer/', include('Employer.urls')),
    path('address/', include('addressgojoco.urls')),

    path('Page/', include('Page.urls')),
    ######## Test API Ajax ###############



]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
