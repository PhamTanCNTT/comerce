from rest_framework import serializers
from addressgojoco.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


################################ Address ######################################

################################ Country ######################################

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id',
                  'NameCountry',
                  'CodeCountry',
                  'UserIDCountry',
                  )
        read_only_fields = ('id', 'UserIDCountry',)


################################ Country ######################################

############################# ProvinceCity ####################################

class ProvinceCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvinceCity
        fields = ('id',
                  'NameProvinceCity',
                  'CodeProvinceCity',
                  'CountryIDProvinceCity',
                  'UserIDProvinceCity',
                  )
        read_only_fields = ('id', 'UserIDProvinceCity',)


############################# ProvinceCity ####################################

############################### District ######################################

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id',
                  'NameDistrict',
                  'ProvinceCityIDDistrict',
                  'UserIDDistrict',
                  )
        read_only_fields = ('id', 'UserIDDistrict',)


############################### District ######################################

################################# Ward ########################################

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ('id',
                  'NameWard',
                  'DistrictIDWard',
                  'UserIDWard',
                  )
        read_only_fields = ('id', 'UserIDWard',)


################################# Ward ########################################

############################## End Address ####################################

############################### Languages #####################################

class LanguageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageUser
        fields = ('id',
                  'NameLanguage',
                  'UserIDLanguage',
                  )
        read_only_fields = ('id', 'UserIDLanguage',)


############################### Languages #####################################

class MainCareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCareer
        fields = ('id', 'UserIDMainCareer', 'NameMainCareer', 'CodeMainCareer', 'CountMainCareer')
        read_only_fields = ('id', 'UserIDMainCareer',)


class Level1CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level1Career
        fields = ('id', 'UserIDLevel1Career', 'NameLevel1Career', 'MainCareerIDLevel1Career', 'CodeLevel1Career',
                  'CountLevel1Career')
        read_only_fields = ('id', 'UserIDLevel1Career',)


class Level2CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level2Career
        fields = ('id', 'UserIDLevel2Career', 'NameLevel2Career', 'Level1CareerIDLevel2Career', 'CodeLevel2Career',
                  'CountLevel2Career')
        read_only_fields = ('id', 'UserIDLevel2Career',)


class Level3CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level3Career
        fields = ('id', 'UserIDLevel3Career', 'NameLevel3Career', 'Level2CareerIDLevel3Career', 'CodeLevel3Career',
                  'CountLevel3Career')
        read_only_fields = ('id', 'UserIDLevel3Career',)
