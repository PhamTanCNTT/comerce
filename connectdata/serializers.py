from rest_framework import serializers, permissions
from .models import *

from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser

#######################Nested#################

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.utils.translation import gettext, gettext_lazy as _
from connectdata.models import *

User = get_user_model()
from django.shortcuts import get_object_or_404


#######################Nested#################


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "title", "content")
        model = Note


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("code", "title", "duration", "fee")
        model = Course


class ComAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CourseAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        depth = 1


#########################Nested#######################

class CourseListAllViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('ComName', 'ComAddress')


# post
class CompanyPostSerializer(serializers.ModelSerializer):
    company = CompanySerializer(required=False)

    class Meta:
        model = Course
        fields = ('IDC', 'code', 'title', 'duration', 'fee', 'company')
        extra_kwargs = {"title": {"error_messages": {"required": "Give yourself a title"}}}

    def create(self, validated_data):
        company_data = validated_data.pop('company')
        course = Course.objects.create(**validated_data)
        Company.objects.create(
            IDC=course,
            ComName=company_data["ComName"],
            ComAddress=company_data["ComAddress"]
        )
        return course

    def update(self, instance, validated_data):
        company_data = validated_data.pop('company')
        course = Course(
            code=self.validated_data["code"],
            title=self.validated_data["title"],
            duration=self.validated_data["duration"],
            fee=self.validated_data["fee"]
        )
        Company.objects.update(
            IDC=course,
            ComName=company_data["ComName"],
            ComAddress=company_data["ComAddress"]
        )
        course.save()
        return course


# Get
class getbinhthuongCourse(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('code', 'title', 'duration', 'fee', 'IDC')


# get detail
class CourseComSerializer(serializers.ModelSerializer):
    coursecompany = serializers.SerializerMethodField(method_name='CouresCom')

    class Meta:
        model = Course
        fields = ('id', 'code', 'title', 'duration', 'fee', 'IDC', 'coursecompany')

    def CouresCom(self, obj):
        company = Company.objects.get(IDC=obj.IDC)
        if not company:
            return {}
        data = CompanySerializer(company).data
        return data


# update ajax long

######################### Course Company ViewSet ###########################

class CompanySerializerLib(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    # UserID = User.id
    # user = self.request.user
    class Meta:
        model = Company
        fields = ('id', 'ComName', 'ComAddress', 'IDC', 'UserID')
        read_only_fields = ('IDC', 'UserID',)


class CourseCompanySerializerLib(serializers.ModelSerializer):
    company = CompanySerializerLib(many=True)

    class Meta:
        model = Course
        fields = ('id', 'code', 'title', 'duration',
                  'fee', 'IDC', 'company')

    def create(self, validated_data):
        company = validated_data.pop('company')
        course = Course.objects.create(**validated_data)
        for com in company:
            Company.objects.create(**com, IDC=course, UserID=course.UserID)
        return course

    def update(self, instance, validated_data):
        # course = Course.objects.get(instance)
        company = validated_data.pop('company')
        instance.code = validated_data.get('code', instance.code)
        instance.title = validated_data.get('title', instance.title)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.fee = validated_data.get('fee', instance.fee)
        instance.IDC = validated_data.get('IDC', instance.IDC)
        # instance.UserID = validated_data.get('UserID', instance.UserID)

        instance.save()
        keep_company = []
        existing_ids = [c.id for c in instance.company]
        for com in company:
            if 'id' in com.keys():
                if Company.objects.filter(id=com['id']).exists():
                    c = Company.objects.get(id=com['id'])
                    c.ComName = com.get('ComName', c.ComName)
                    c.ComAddress = com.get('ComAddress', c.ComAddress)

                    c.save()
                    keep_company.append(c.id)
                else:
                    continue
            else:
                c = Company.objects.create(**com, IDC=instance, UserID=c.UserID)
                keep_company.append(c.id)
        for com in instance.company:
            if com.id not in keep_company:
                com.delete()
        return instance


######################### Course Company ViewSet ###########################

# serializer cua sep
class CourseSerializerLib(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'code', 'title', 'duration', 'fee', 'IDC')


class ListTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title")


######################### Nested #######################

######################### Nested Profile #######################

class ProfileUserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id',
                  'UserImage',
                  'UserProfile',
                  'UserFirstName',
                  'UserMiddleName',
                  'UserLastName',
                  'UserFullName',
                  'UserBirthDay',
                  'UserSex',
                  'UserPhone',
                  'Email',
                  'UserIDCard',
                  'IDCardPlaceOfIssue',
                  'UserApplyDate',
                  'UserNationality',
                  'MaritalStatus',
                  'AddressIDProfile',

                  ]
        read_only_fields = ('id',
                            'UserProfile',
                            'UserFullName',
                            )


################################ Bank User#####################################

######################### Nested Profile #######################

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'UserImage']
        read_only_fields = ('id',)

    def save(self, *args, **kwargs):
        if self.instance.UserImage:
            self.instance.UserImage.delete()
        return super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if self.instance.UserImage:
    #         self.instance.UserImage.delete()
    #     return super().save(**kwargs)


################################ Bank User#####################################


class UserBankFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBank
        fields = ['id', 'idTK', 'ownTK', 'BankName', 'BranchName', 'EmployeeIDBank', 'UserIDBank']
        read_only_fields = ['id', 'UserIDBank', 'EmployeeIDBank']


################################ Bank User#####################################

################################ Create User's Profile Employer Employee  #####################################

### Create Porfile for Employee
class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'isEmployee', 'UserIDEmployee', ]
        read_only_fields = ('id', 'UserIDEmployee',)


### Create Porfile for Employer
class CreateEmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['id', 'isEmployer', 'UserIDEmployer', ]
        read_only_fields = ('id', 'UserIDEmployer',)


### Create Porfile for User
class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "isEmployee",
            "isEmployer",
            "UserProfile",
        ]
        read_only_fields = ("id", "UserProfile",)


################################ User's Profile Employer Employee #####################################

################################ User's Image AttPhoto #####################################

class AttPhotoImageSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)

    class Meta:
        model = AttPhoto
        fields = ['id', 'UserPhoto', 'TitleImage', 'UserIDAttPhoto', ]
        read_only_fields = ('id', 'UserIDAttPhoto',)

    # def save(self, *args, **kwargs):
    #     if self.instance.UserPhoto:
    #         self.instance.UserPhoto.delete()
    #     return super().save(*args, **kwargs)


################################ User's Image AttPhoto #####################################

class EmployeeAttPhotoSerializer(serializers.ModelSerializer):
    employeeidattphoto = AttPhotoImageSerializer(many=True)

    class Meta:
        model = Employee
        fields = ['id', 'UserIDEmployee', 'isEmployee', 'UserNoted',
                  'employeeidattphoto'
                  ]
        read_only_fields = ('id', 'UserIDEmployee',)

    def create(self, validated_data):
        employeeidattphoto = validated_data.pop('employeeidattphoto')
        employee = Employee.objects.create(**validated_data)
        for attphoto in employeeidattphoto:
            AttPhoto.objects.create(**attphoto, EmployeeIDAttPhoto=employee, UserIDAttPhoto=employee.UserIDEmployee)
        return Employee

    def update(self, instance, validated_data):
        employeeidattphoto = validated_data.pop('employeeidattphoto')
        instance.isEmployee = validated_data.get('isEmployee', instance.isEmployee)
        instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
        instance.save()
        keep_employeeidattphoto = []
        existing_ids = [c.id for c in instance.employeeidattphoto]
        for attphoto in employeeidattphoto:
            if 'id' in attphoto.keys():
                if AttPhoto.objects.filter(id=attphoto['id']).exists():
                    c = AttPhoto.objects.get(id=attphoto['id'])
                    c.TitleImage = attphoto.get('TitleImage', c.TitleImage)
                    c.UserPhoto = attphoto.get('UserPhoto', c.UserPhoto)
                    c.save()
                    keep_employeeidattphoto.append(c.id)
                else:
                    continue
            else:
                c = AttPhoto.objects.create(**attphoto, EmployeeIDAttPhoto=instance,
                                            UserIDAttPhoto=instance.UserIDEmployee)
                keep_employeeidattphoto.append(c.id)
        for attphoto in instance.employeeidattphoto:
            if attphoto.id not in keep_employeeidattphoto:
                attphoto.delete()
        return instance


class AttPhotoEmployeeSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)

    class Meta:
        model = AttPhoto
        fields = ['id', 'UserPhoto', 'TitleImage', 'UserIDAttPhoto', 'EmployeeIDAttPhoto', ]
        read_only_fields = ('id', 'UserIDAttPhoto', 'EmployeeIDAttPhoto',)

    def save(self, *args, **kwargs):
        # if self.instance.UserPhoto:
        #     self.instance.UserPhoto.delete()
        return super().save(*args, **kwargs)


################## Employ - Education #########################

class UserEducationSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)

    class Meta:
        model = Education
        fields = ('id', 'DegreePhoto', 'EducationalInstitution', 'Specialized',
                  'Language', 'DegreeLevel', 'Degree',
                  'UserIDEducation', 'EmployeeIDEducation')
        read_only_fields = ('id', 'UserIDEducation', 'EmployeeIDEducation',)


class EmployeeEduacationSerializer(serializers.ModelSerializer):
    Usereducationserializer = UserEducationSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('id', 'UserNoted', 'UserIDEmployee', 'Usereducationserializer',)
        read_only_fields = ('id', 'UserIDEmployee',)


################## Employ - Education #########################

################## Create - CV -  Education ####################
class EducationIDCurriculumVitaeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ('id',
                  # 'DegreePhoto', 'EducationalInstitution', 'Specialized',
                  # 'Language', 'DegreeLevel','Degree',
                  'UserIDEducation', 'EmployeeIDEducation', 'CurriculumVitaeIDEducation',)
        read_only_fields = ('id',
                            'UserIDEducation',
                            'EmployeeIDEducation',
                            # 'CurriculumVitaeIDEducation',
                            )


class CurriculumVitaeEducationSerializer(serializers.ModelSerializer):
    Usereducationserializer = UserEducationSerializer(many=True)

    class Meta:
        model = CurriculumVitae
        fields = ('id', 'DesiredPosition',
                  # 'CurrentPosition', 'DesiredLevel', 'FormOfWork', 'DesiredSalary',
                  'UserIDCurriculumVitae',
                  # 'ProfileIDCurriculumVitae',
                  # 'educationidcuriculumvitae',
                  'Usereducationserializer',
                  )
        read_only_fields = ('id',
                            'UserIDCurriculumVitae',
                            # 'ProfileIDCurriculumVitae',
                            )

    def create(self, validated_data):
        Usereducationserializer = validated_data.pop('Usereducationserializer')
        curriculumvitae = CurriculumVitae.objects.create(**validated_data)
        employee = Employee.objects.get(UserIDEmployee=curriculumvitae.UserIDCurriculumVitae)
        for educationidcv in Usereducationserializer:
            Education.objects.create(**educationidcv, UserIDEducation=curriculumvitae,
                                     CurriculumVitaeIDEducation=employee.UserIDEmployee, )
        return CurriculumVitae


class CVEmployeeExperiencesSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)

    class Meta:
        model = Experiences
        fields = ('id',
                  # 'ExperiencesName',
                  # 'DegreePhoto', 'EducationalInstitution', 'Specialized',
                  # 'Language', 'DegreeLevel', 'Degree',
                  'UserIDExperiences', 'EmployeeIDExperiences', 'CurriculumVitaeIDExperiences',)
        read_only_fields = ('id', 'UserIDExperiences',
                            # 'CurriculumVitaeIDExperiences',
                            'EmployeeIDExperiences',
                            )

########################### Employee Education #################################

class CVEmployeeEducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = ('id',
                  'Degree',
                  'DegreePhotoBefor',
                  'DegreePhotoAfter',
                  'EducationalInstitution',
                  'Specialized',
                  'Language',
                  'DegreeLevel',
                  'DateTimeSupply',
                  'UserIDEducation',
                  'EmployeeIDEducation',
                  )
        read_only_fields = ('id',
                            'UserIDEducation',
                            'EmployeeIDEducation',
                            )

########################### Employee Education #################################

########################### Employee Career #################################

class EmployeeCareerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Career
        fields = ('id',
                  'Title',
                  'UserIDCareer',
                  'EmployeeIDCareer',
                  )
        read_only_fields = ('id',
                            'UserIDCareer',
                            'EmployeeIDCareer',
                            )

########################### Employee Career #################################


class CVSerializer(serializers.ModelSerializer):
    cvemployeeeducationserializer = CVEmployeeEducationSerializer(many=True)
    cvemployeeexperiences = CVEmployeeExperiencesSerializer(many=True)

    class Meta:
        model = CurriculumVitae
        fields = ('id',
                  # 'DesiredPosition',
                  'isFinishCV',
                  # 'CurrentPosition', 'DesiredLevel', 'FormOfWork', 'DesiredSalary',
                  'ProfileIDCurriculumVitae',
                  'UserIDCurriculumVitae',
                  'cvemployeeeducationserializer',
                  'cvemployeeexperiences',

                  )
        read_only_fields = ('id',
                            'UserIDCurriculumVitae',
                            'ProfileIDCurriculumVitae',
                            'isFinishCV'

                            )

    def create(self, validated_data):

        cvemployeeeducationserializer = validated_data.pop('cvemployeeeducationserializer')
        cvemployeeexperiences = validated_data.pop('cvemployeeexperiences')
        curriculumvitae = CurriculumVitae.objects.create(**validated_data)
        curriculumvitae.save()

        employee = Employee.objects.get(UserIDEmployee=curriculumvitae.UserIDCurriculumVitae)

        for edu in cvemployeeeducationserializer:
            Education.objects.create(**edu,
                                     UserIDEducation=curriculumvitae.UserIDCurriculumVitae,
                                     EmployeeIDEducation=employee,
                                     CurriculumVitaeIDEducation=curriculumvitae.objects.add(id=curriculumvitae.id),
                                     )
        for exper in cvemployeeexperiences:
            Experiences.objects.create(**exper,
                                       UserIDExperiences=curriculumvitae.UserIDCurriculumVitae,
                                       EmployeeIDExperiences=employee,
                                       CurriculumVitaeIDExperiences=curriculumvitae,
                                       )

        return curriculumvitae

    def update(self, instance, validated_data):
        cvemployeeeducationserializer = validated_data.pop('cvemployeeeducationserializer')
        cvemployeeexperiences = validated_data.pop('cvemployeeexperiences')
        instance.DesiredPosition = validated_data.get('DesiredPosition', instance.DesiredPosition)
        instance.save()
        for edu in cvemployeeeducationserializer:
            if 'id' in edu.keys():
                if Education.objects.filter(id=edu['id']).exists():
                    c = Education.objects.get(id=edu['id'])
                    c.Degree = edu.get('Degree', c.Degree)
                    c.save()
                else:
                    continue
            else:
                employee = Employee.objects.get(UserIDEmployee=instance.UserIDCurriculumVitae)
                Education.objects.create(**edu,
                                         UserIDEducation=instance.UserIDCurriculumVitae,
                                         EmployeeIDEducation=employee,
                                         CurriculumVitaeIDEducation=instance,
                                         )
        for exper in cvemployeeexperiences:
            if 'id' in exper.keys():
                if Experiences.objects.filter(id=exper['id']).exists():
                    c = Experiences.objects.get(id=exper['id'])
                    c.ExperiencesName = exper.get('ExperiencesName', c.ExperiencesName)
                    c.save()
                else:
                    continue
            else:
                employee = Employee.objects.get(UserIDEmployee=instance.UserIDCurriculumVitae)
                Experiences.objects.create(**exper,
                                           UserIDExperiences=instance.UserIDCurriculumVitae,
                                           EmployeeIDExperiences=employee,
                                           CurriculumVitaeIDExperiences=instance,
                                           )
        return instance


# CVUpdate

class CVFinishPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        queryset = Schedule.objects.filter(UserIDSchedule__username=self.context['request'].user.username)
        return queryset


class CVFinishSerializer(serializers.ModelSerializer):
    ScheduleIDCurriculumVitae = CVFinishPrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CurriculumVitae
        fields = ('id',
                  'DesiredPositionIDCurriculumVitae',
                  'DesiredLevelIDCurriculumVitae',
                  'CurrentLevelIDCurriculumVitae',
                  'ScheduleIDCurriculumVitae',
                  'CurrencyIDCurriculumVitae',
                  'CurrentSalary',
                  'DesiredSalary',
                  'AddressIDCurriculumVitae',
                  'JobClassificationIDCurriculumVitae',
                  'Introduce',
                  'Interests',
                  'ProfileIDCurriculumVitae',
                  'UserIDCurriculumVitae',
                  'isFinishCV',
                  )
        read_only_fields = ('id',
                            'UserIDCurriculumVitae',
                            'ProfileIDCurriculumVitae',
                            # 'cv_options',
                            )


########################## CV Education ManyToMany ################################

class CVEmEduManyToManySerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)

    class Meta:
        model = Education
        fields = ('id',
                  # 'DegreePhoto', 'EducationalInstitution', 'Specialized',
                  # 'Language', 'DegreeLevel', 'Degree',
                  'UserIDEducation', 'EmployeeIDEducation',
                  'CurriculumVitaeIDEducation',)
        read_only_fields = ('id', 'UserIDEducation',
                            # 'CurriculumVitaeIDEducation',
                            'EmployeeIDEducation',
                            )
        extra_kwargs = {'CurriculumVitaeIDEducation': {'required': False}}


class CVManyToManySerializer(serializers.ModelSerializer):
    cvemployeeeducationserializer = CVEmEduManyToManySerializer(many=True)
    cvemployeeexperiences = CVEmployeeExperiencesSerializer(many=True)

    class Meta:
        model = CurriculumVitae
        fields = ('id', 'DesiredPosition',
                  # 'CurrentPosition', 'DesiredLevel', 'FormOfWork', 'DesiredSalary',
                  'UserIDCurriculumVitae',
                  'cvemployeeeducationserializer',
                  'cvemployeeexperiences',
                  )
        read_only_fields = ('id',
                            'UserIDCurriculumVitae',
                            )
        extra_kwargs = {'cvemployeeeducationserializer': {'required': False}}

    def create(self, validated_data):
        cvemployeeeducationserializer = validated_data.pop('cvemployeeeducationserializer')
        cvemployeeexperiences = validated_data.pop('cvemployeeexperiences')
        curriculumvitae = CurriculumVitae.objects.create(**validated_data)
        curriculumvitae.save()
        # employee = Employee.objects.get(UserIDEmployee=curriculumvitae.UserIDCurriculumVitae)
        # for edu in cvemployeeeducationserializer:
        #     Education.objects.create(**edu,
        #                              UserIDEducation=curriculumvitae.UserIDCurriculumVitae,
        #                              EmployeeIDEducation=employee,
        #                              #CurriculumVitaeIDEducation=curriculumvitae.objects.get(id=curriculumvitae.id),
        #                              )
        # for exper in cvemployeeexperiences:
        #     Experiences.objects.create(**exper,
        #                                UserIDExperiences=curriculumvitae.UserIDCurriculumVitae,
        #                                EmployeeIDExperiences=employee,
        #                                CurriculumVitaeIDExperiences=curriculumvitae,
        #                                )

        return curriculumvitae

    def update(self, instance, validated_data):
        cvemployeeeducationserializer = validated_data.pop('cvemployeeeducationserializer')
        cvemployeeexperiences = validated_data.pop('cvemployeeexperiences')
        instance.DesiredPosition = validated_data.get('DesiredPosition', instance.DesiredPosition)
        instance.save()
        # for edu in cvemployeeeducationserializer:
        #     curriculumvitae = CurriculumVitae.objects.get(id=instance.id)
        #     employee = Employee.objects.get(UserIDEmployee=instance.UserIDCurriculumVitae)
        #     if 'id' in edu.keys():
        #         if Education.objects.filter(id=edu['id']).exists():
        #             c = Education.objects.get(id=edu['id'])
        #             # c.Degree = edu.get('Degree', c.Degree)
        #             c.CurriculumVitaeIDEducation = edu.get('CurriculumVitaeIDEducation',
        #                                                    c.CurriculumVitaeIDEducation([curriculumvitae.objects.add(id=curriculumvitae.id)]))
        #             c.save()
        #         else:
        #             continue
        #     else:
        #         continue
        #         # employee = Employee.objects.get(UserIDEmployee=instance.UserIDCurriculumVitae)
        #         # # curriculumvitae = CurriculumVitae.objects.get(UserIDCurriculumVitae=employee.UserIDEmployee)
        #         #
        #         # Education.objects.create(**edu,
        #         #                          UserIDEducation=instance.UserIDCurriculumVitae,
        #         #                          EmployeeIDEducation=employee,
        #         #                          #CurriculumVitaeIDEducation=instance.curriculumvitae.objects.add(id=curriculumvitae.id),
        #         #                          )
        # for exper in cvemployeeexperiences:
        #     if 'id' in exper.keys():
        #         if Experiences.objects.filter(id=exper['id']).exists():
        #             c = Experiences.objects.get(id=exper['id'])
        #             c.ExperiencesName = exper.get('ExperiencesName', c.ExperiencesName)
        #             c.save()
        #         else:
        #             continue
        #     else:
        #         employee = Employee.objects.get(UserIDEmployee=instance.UserIDCurriculumVitae)
        #         Experiences.objects.create(**exper,
        #                                    UserIDExperiences=instance.UserIDCurriculumVitae,
        #                                    EmployeeIDExperiences=employee,
        #                                    CurriculumVitaeIDExperiences=instance,
        #                                    )
        return instance


########################## CV Education ManyToMany ################################

########################## Khong Phan Quyen ManyToMany CV - Edu ################################

class IsCurriculumVitaeManyToMany(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.UserIDCurriculumVitae == request.user


class EduManyToManySerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['-id']
        model = Education
        fields = ('id',
                  'Degree',
                  'UserIDEducation', 'EmployeeIDEducation',
                  'CurriculumVitaeIDEducation',)
        read_only_fields = ('id', 'UserIDEducation',
                            # 'CurriculumVitaeIDEducation',
                            'EmployeeIDEducation',
                            )
        extra_kwargs = {'CurriculumVitaeIDEducation': {'required': False}}


class CVEduManyToManySerializer(serializers.ModelSerializer):
    cvemployeeeducationserializer = EduManyToManySerializer(many=True, read_only=True, )

    class Meta:
        ordering = ['-id']
        model = CurriculumVitae
        fields = ('id', 'DesiredPosition',
                  'UserIDCurriculumVitae',
                  'cvemployeeeducationserializer',
                  )
        read_only_fields = ('id',
                            'UserIDCurriculumVitae',
                            )
        extra_kwargs = {'cvemployeeeducationserializer': {'required': False}}


########################## Khong Phan Quyen ManyToMany CV - Edu ################################

########################## Update Create Full Full - Edu ################################


class EducationFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ('id', 'Degree',
                  'DegreePhotoBefor', 'DegreePhotoAfter', 'EducationalInstitution', 'Specialized',
                  'Language', 'DegreeLevel',
                  # 'CurriculumVitaeIDEducation',
                  'UserIDEducation', 'EmployeeIDEducation',)
        read_only_fields = ('id',
                            'UserIDEducation',
                            # 'CurriculumVitaeIDEducation',
                            'EmployeeIDEducation',
                            )


########################## Update Create Full Full - Edu ################################

########################## Update Create Full Full - Experiences ################################


# Experiences

class ExperienceFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiences
        fields = ('id', 'ComName',
                  'TimeWorkFrom', 'TimeWorkTo', 'isCurentPosition',
                  'Language', 'Position',
                  'JobDescription', 'JobAchievements',
                  'UserIDExperiences', 'EmployeeIDExperiences',)
        read_only_fields = ('id',
                            'UserIDExperiences',
                            # 'CurriculumVitaeIDEducation',
                            'EmployeeIDExperiences',
                            )


########################## Update Create Full Full - Experiences ################################

class isFinishCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumVitae
        fields = ('id', 'isFinishCV')
        read_only_fields = ('id', 'isFinishCV',)


########################## Search CV: Address################################

class SearchCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumVitae
        fields = ('id',
                  'AddressIDCurriculumVitae',
                  'DesiredPositionIDCurriculumVitae'
                  )
        read_only_fields = (
            'id',
            # 'AddressIDCurriculumVitae',
        )
        # depth = 1


class InOutCVSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = InOut
        fields = ('id',
                  'InOutName',
                  'TimeIn',
                  'TimeOut',
                  'UserIDInOut',
                  'EmployeeIDInOut',
                  'ScheduleIDInOut',
                  )
        read_only_fields = ('id',
                            'UserIDInOut',
                            'EmployeeIDInOut',
                            'ScheduleIDInOut',
                            )
        # depth = 1


class ScheduleCVSerializer(serializers.ModelSerializer):
    inoutidschedule = InOutCVSerializer(many=True)

    class Meta:
        model = Schedule
        fields = (
            'id',
            'UserIDShedule',
            'EmlpoyeeIDSchedule',
            'SchName',
            'inoutidschedule',
        )
        read_only_fields = (
            'id',
            'UserIDShedule',
            'EmlpoyeeIDSchedule',
        )
        # depth = 1

    def create(self, validated_data):
        inoutidschedule = validated_data.pop('inoutidschedule')
        schedule = Schedule.objects.create(**validated_data)
        scheduleidinout = Employee.objects.get(UserIDEmployee=schedule.UserIDShedule)
        for inout in inoutidschedule:
            InOut.objects.create(**inout, EmployeeIDInOut=scheduleidinout,
                                 UserIDInOut=schedule.UserIDShedule,
                                 ScheduleIDInOut=schedule)
        return schedule

    def update(self, instance, validated_data):
        inoutidschedule = validated_data.pop('inoutidschedule')
        instance.InOutName = validated_data.get('InOutName', instance.InOutName)
        instance.TimeIn = validated_data.get('TimeIn', instance.TimeIn)
        instance.TimeOut = validated_data.get('TimeOut', instance.TimeOut)

        instance.save()
        keep_inoutidschedule = []
        existing_ids = [c.id for c in instance.inoutidschedule]
        for inout in inoutidschedule:
            if 'id' in inout.keys():
                if InOut.objects.filter(id=inout['id']).exists():
                    c = InOut.objects.get(id=inout['id'])
                    c.InOutName = inout.get('InOutName', c.InOutName)
                    c.TimeIn = inout.get('TimeIn', c.TimeIn)
                    c.TimeOut = inout.get('TimeOut', c.TimeOut)
                    c.save()
                    keep_inoutidschedule.append(c.id)
                else:
                    continue
            else:
                c = InOut.objects.create(**inout, EmployeeIDInOut=instance, UserIDInOut=c.UserIDShedule)
                keep_inoutidschedule.append(c.id)
        for inout in instance.inoutidschedule:
            if inout.id not in keep_inoutidschedule:
                inout.delete()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id',
                  'CountryIDAddress',
                  'ProvinceCityIDAddress',
                  'DistrictIDAddress',
                  'WardIDAddress',
                  'NameStreet',
                  'NoLoad',
                  'AddressLine',

                  )
        read_only_fields = ('id', 'AddressLine',)
        # depth = 1

class CheckInOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInOut
        fields = ('id',
                  'UserIDCheckInOut',
                  # 'CompanyIDInOutArr',
                   'JobApplyIDInOutArr',
                  'ScheduleIDCheckInOut',
                  # 'MachineNo',
                  'IPAddressCheckInOut',
                  'LocationIDCheckInOut',

                  )
        read_only_fields = (
            'id',
            'UserIDCheckInOut',
            'LocationIDCheckInOut',
            # 'IPAddressCheckInOut',
            'ScheduleIDCheckInOut',
            # 'CompanyIDCheckInOut',
            # 'JobIDCheckInOut',
            # 'CurriculumVitaeIDCheckInOut'
        )
        # depth = 1


# Checkinout Lồng Location, Checkinout
class LocationSerializer(serializers.ModelSerializer):
    checkinout = CheckInOutSerializer(required=False)

    class Meta:
        model = Location
        fields = (
            'id',
            'GPS_EMP_LAT',
            'GPS_EMP_LONG',
            'UserIDLocation',
            'TimeL',
            'JobApplyIDLocation',
            'checkinout',

        )

        read_only_fields = (
            'id',
            'UserIDLocation',
            'TimeL',
            # 'ScheduleIDCheckInOut',
            # 'CompanyIDCheckInOut',
            # 'JobIDCheckInOut',
            # 'CurriculumVitaeIDCheckInOut'
        )
    def create(self, validated_data):
        checkinout_data = validated_data.pop('checkinout')
        location = Location.objects.create(**validated_data)
        CheckInOut.objects.create(
            LocationIDCheckInOut=location,
            IPAddressCheckInOut=checkinout_data['IPAddressCheckInOut'],
            # MachineNo=checkinout_data['MachineNo'],
            UserIDCheckInOut=location.UserIDLocation,
            # ScheduleIDCheckInOut=checkinout_data['ScheduleIDCheckInOut'],
            JobApplyIDInOutArr=checkinout_data['JobApplyIDInOutArr'],
            # JobIDCheckInOut=checkinout_data['JobIDCheckInOut'],
            # CurriculumVitaeIDCheckInOut=checkinout_data['CurriculumVitaeIDCheckInOut'],
        )
        return location


class CompanyEmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id',
                  'UserIDCompany',
                  # 'ScheduleIDCheckInOut',
                  # 'InOutCode',
                  # 'MachineNo',
                  # 'IPAddressCheckInOut',
                  'ComName',
                  'AddressIDCompany',
                  # 'JobIDCheckInOut',
                  # 'CurriculumVitaeIDCheckInOut'
                  )
        read_only_fields = (
            'id',
            'UserIDCompany',
            # 'LocationIDCheckInOut',
            # 'ScheduleIDCheckInOut',
            # 'CompanyIDCheckInOut',
            # 'JobIDCheckInOut',
            # 'CurriculumVitaeIDCheckInOut'
        )
        # depth = 1

# chay create CV - Viet
# ########## Nested ViewSet - Post Employee - CurriculumVitae #########################
class EmployeeCurriculumVitaeViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumVitae
        fields = (
            'id',
            'UserIDCurriculumVitae',
            'EmployeeIDCurriculumVitae',
            'ProfileIDCurriculumVitae',
            'AddressIDCurriculumVitae',
            'EducationIDCurriculumVitae',
            'CareerIDCurriculumVitae',
            'WorkLocationIDCurriculumVitae',
            # 'ShiftIDCurriculumVitae',
            'Title',
            # 'MaritalStatus',
            # 'Introduce', 'Career', 'FormOfWork', 'WorkLocation', 'DesiredSalary',
            # 'Skill',
        )
        read_only_fields = (
            'id',
            'UserIDCurriculumVitae',
            'EmployeeIDCurriculumVitae',
            'ProfileIDCurriculumVitae',
            'AddressIDCurriculumVitae',
        )
        # depth =1


############################### Career ######################################

class CareerViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = (
            'id',
            'Title',
            'UserIDCareer',
            'EmployeeIDCareer',
        )
        read_only_fields = (
            'id',
            'UserIDCareer',
            'EmployeeIDCareer',
        )

################################### Career #######################################

############################### WorkLocation ######################################

class WorkLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkLocation
        fields = (
            'id',
            'Title',
            'CountryIDWorkLocation',
            'ProvinceCityIDWorkLocation',
            'DistrictIDWorkLocation',
            'WardIDWorkLocation',
            'UserIDWorkLocation',
        )
        read_only_fields = (
            'id',
            'UserIDWorkLocation',
        )

############################### WorkLocation ######################################

# create employer & employee
class ProfileSerializerCheck(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'isEmployee', 'isEmployer', 'UserProfile')
        read_only_fields = ('id', 'UserProfile',)

    def create(self, validated_data):
        pro = Profile.objects.create(**validated_data)
        Employee.objects.create(
            UserIDEmployee=pro.UserProfile,
            isEmployee=validated_data['isEmployee'],
        )
        Employer.objects.create(
            UserIDEmployer=pro.UserProfile,
            isEmployer=validated_data['isEmployer'],
        )
        return pro