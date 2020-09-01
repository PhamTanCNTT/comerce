from rest_framework import serializers, permissions
from connectdata.models import *

from rest_framework.exceptions import PermissionDenied

#######################Nested#################

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.utils.translation import gettext, gettext_lazy as _
from jwtauth.models import *
User = get_user_model()
from django.shortcuts import get_object_or_404


#
# class UserUploadPhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = profile
#         fields = ('id', 'UserImage')