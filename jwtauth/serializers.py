from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import response
from rest_framework.response import Response
from rest_framework import response, decorators, permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from connectdata.models import Profile
from connectdata.models import Employee
from connectdata.models import Employer

from django.contrib.auth import get_user_model, authenticate
User = get_user_model()

############################ Create User Profile Employer Employee  #####################################

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['isEmployee', 'isEmployer', 'UserProfile',]
        read_only_fields = ('UserProfile',)

class EmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['isEmployee', 'UserIDEmployee',]
        read_only_fields = ('UserIDEmployee',)

class EmployerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = [ 'isEmployer', 'UserIDEmployer',]
        read_only_fields = ('UserIDEmployer',)

class ProfileFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['Salary', 'Designation', 'Picture', 'isEmployee', 'isEmployer',
                  'UserMiddleName', 'UserFullName', 'UserBirthDay', 'UserBirthPlace',
                  'UserSex', 'UserIDCard', 'IDCardPlaceOfIssue', 'UserApplyDate', ]


class UserCreateSerializer(serializers.ModelSerializer):

    profileserializer = ProfileSerializer(required=True)
    password = serializers.CharField(write_only=True, required=True, style={
                                     "input_type":   "password"})
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label="Confirm password")
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "profileserializer",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profileserializer_data = validated_data.pop('profileserializer')
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if (email and User.objects.filter(email=email).exclude(username=username).exists()):
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."})
        if password != password2:
            raise serializers.ValidationError(
                {"password": "The two passwords differ."})
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        # user = User.objects.create_user(**validated_data)
        # user.set_password(password)
        Profile.objects.create(
            UserProfile=user,
            isEmployee=profileserializer_data['isEmployee'],
            isEmployer=profileserializer_data['isEmployer'],
        )
        Employee.objects.create(
            UserIDEmployee=user,
            isEmployee = profileserializer_data['isEmployee'],
        )
        Employer.objects.create(
            UserIDEmployer=user,
            isEmployer=profileserializer_data['isEmployer'],
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    profileserializer = ProfileSerializer(required=True)
    class Meta:
        model = User
        fields = [ "id",
                   "username",
                   "email",
                   "profileserializer",
        ]
        read_only_fields = ('id','username', )

    # @decorators.permission_classes([permissions.IsAuthenticated])
    def update(self, instance, validated_data):
        profileSerializer_data = validated_data.pop('profileserializer')
        instance.email = validated_data["email"]
        if (instance.email and User.objects.filter(email=instance.email).exclude(email=instance.email).exists()):
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."})
        instance.save()
        # user = User.objects.create_user(**validated_data)
        # user.set_password(password)
        Profile.objects.create(
            UserProfile=instance,
            # self.initial_data,
            # UserFullName=profileSerializer_data['UserFullName'],
            isEmoloyee=profileSerializer_data['isEmployee'],
            isEmployer=profileSerializer_data['isEmployer'],
        )
        Employee.objects.create(
            UserIDEmployee=instance,
            isEmoloyee = profileSerializer_data['isEmoloyee'],
        )
        Employer.objects.create(
            UserIDEmployer=instance,
            isEmployer=profileSerializer_data['isEmployer'],
        )
        return instance


############################ Create User Profile Employer Employee  #####################################


class UserCreateSerializerSocial(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     "input_type":   "password"})
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label="Confirm password")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}


    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if (email and User.objects.filter(email=email).exclude(username=username).exists()):
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."})
        if password != password2:
            raise serializers.ValidationError(
                {"password": "The two passwords differ."})
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user


############################ user token - nut upload img ############################

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'UserImage')
        read_only_fields = ('id',)

    def save(self, *args, **kwargs):
        if self.instance.UserImage:
            self.instance.UserImage.delete()
        return super().save(*args, **kwargs)

class CMND1ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'CMND1')
        read_only_fields = ('id',)

    def save(self, *args, **kwargs):
        if self.instance.CMND1:
            self.instance.CMND1.delete()
        return super().save(*args, **kwargs)

class CMND2ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'CMND2')
        read_only_fields = ('id',)

    def save(self, *args, **kwargs):
        if self.instance.CMND2:
            self.instance.CMND2.delete()
        return super().save(*args, **kwargs)




# create address
class ProfileAddressFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id',
                  'UserProfile',
                  'AddressIDProfile',
                  'UserFirstName',
                  'UserMiddleName',
                  'UserLastName',
                  'UserFullName',
                  'UserBirthDay',
                  'UserSex',
                  'UserPhone',
                  'Email',)
        read_only_fields = ('id', 'UserFullName', 'UserProfile',)

############################ user token - nut upload img ############################

