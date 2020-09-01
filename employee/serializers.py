from rest_framework import serializers, fields
from connectdata.models import UserBank, Education
from connectdata.models import *
from connectdata.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


######################### Employee ##########################

class UserBankIDAll(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    class Meta:
        model = UserBank
        fields = ['id', 'idTK', 'ownTK', 'BankName', 'BranchName', 'EmployeeID']
        # read_only_fields = ('EmployeeID')


class EmployeeSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'UserNoted']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'Salary', 'Designation', 'Picture']


###########Nested Get - Post Employee - Bank ##########

class UserBankIDSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = UserBank
        fields = ('id', 'idTK', 'ownTK', 'BankName', 'BranchName',
                  'EmployeeID', 'UserIDBank')
        read_only_fields = ('EmployeeID', 'UserIDBank',)
        depth = 1


###########Nested Get - Post Employee - Bank ##########

class EmployeeBankSerializer(serializers.ModelSerializer):
    userbankid = UserBankIDSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('id', 'UserNoted', 'userbankid',)
        # read_only_fields = ('UserIDEmployee',)

    def create(self, validated_data):
        userbankid = validated_data.pop('userbankid')
        employee = Employee.objects.create(**validated_data)
        for bankid in userbankid:
            UserBank.objects.create(**bankid, EmployeeID=employee, UserIDBank=employee.UserIDEmployee)
        return employee

    def update(self, instance, validated_data):
        # course = Course.objects.get(instance)
        userbankid = validated_data.pop('userbankid')
        # instance.IDUserBank = validated_data.get('IDUserBank', instance.IDUserBank)
        instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
        # instance.UserID = validated_data.get('UserID', instance.UserID)
        instance.save()
        # keep_userbankid = []
        # existing_ids = [c.id for c in instance.userbankid]
        for bankid in userbankid:
            if 'id' in bankid.keys():
                if UserBank.objects.filter(id=bankid['id']).exists():
                    c = UserBank.objects.get(id=bankid['id'])
                    c.idTK = bankid.get('idTK', c.idTK)
                    c.ownTK = bankid.get('ownTK', c.ownTK)
                    c.BankName = bankid.get('BankName', c.BankName)
                    c.BranchName = bankid.get('BranchName', c.BranchName)
                    c.save()
                    # keep_userbankid.append(c.id)
                else:
                    continue
            else:
                c = UserBank.objects.create(**bankid, EmployeeID=instance, UserIDBank=instance.UserIDEmployee)
        #         keep_userbankid.append(c.id)
        # for bankid in instance.userbankid:
        #     if bankid.id not in keep_userbankid:
        #         bankid.delete()
        return instance


###########Nested Get - Post Employee - Bank ##########


########### Viewset Employ ##########


class EmployeeUserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['isWorker', 'UserNoted']


################################ Employee User #####################################

###########Nested Get - Post Employee - Bank #########################

class UserBankIDABCSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = UserBank
        fields = ('id', 'idTK', 'ownTK', 'BankName', 'BranchName',
                  'EmployeeID', 'UserIDBank')
        read_only_fields = ('EmployeeID', 'UserIDBank')


class EmployeeBankABCSerializer(serializers.ModelSerializer):
    userbankid = UserBankIDABCSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('id', 'UserNoted', 'userbankid',)
        # read_only_fields = ('UserIDEmployee',)
        depth = 1


################ Nested Get - Post Employee - Bank ###################

class EmployeeBankViewSerializer(serializers.ModelSerializer):
    userbankid = UserBankIDSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('id', 'UserNoted', 'userbankid',)
        # read_only_fields = ('UserIDEmployee',)
        # depth = 1


################ Nested ViewSet - Post Employee - Bank ###################

class EmployeeBankViewSetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = UserBank
        fields = ('id', 'idTK', 'ownTK', 'BankName', 'BranchName',
                  'EmployeeID', 'UserIDBank')
        read_only_fields = ('EmployeeID', 'UserIDBank',)
        depth = 1


class EmployeeBankVSSerializer(serializers.ModelSerializer):
    employeebank = EmployeeBankViewSetSerializer(many=True)

    # employeeeducate = EmployeeEducateViewSetSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('id', 'UserNoted', 'employeebank',)

    def create(self, validated_data):
        employeebank = validated_data.pop('employeebank')
        employee = Employee.objects.create(**validated_data)
        for ebank in employeebank:
            UserBank.objects.create(**ebank, EmployeeID=employee, UserIDBank=employee.UserIDEmployee)
        return employee

    def update(self, instance, validated_data):
        # course = Course.objects.get(instance)
        employeebank = validated_data.pop('employeebank')
        instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
        instance.save()
        keep_employeebank = []
        existing_ids = [c.id for c in instance.employeebank]
        for ebank in employeebank:
            if 'id' in ebank.keys():
                if UserBank.objects.filter(id=ebank['id']).exists():
                    c = UserBank.objects.get(id=ebank['id'])
                    c.idTK = ebank.get('idTK', c.idTK)
                    c.ownTK = ebank.get('ownTK', c.ownTK)
                    c.BankName = ebank.get('BankName', c.idTK)
                    c.BranchName = ebank.get('BranchName', c.BranchName)
                    c.save()
                    keep_employeebank.append(c.id)
                else:
                    continue
            else:
                c = UserBank.objects.create(**ebank, EmployeeID=instance, UserIDBank=c.UserIDBank)
                keep_employeebank.append(c.id)
        for ebank in instance.employeebank:
            if ebank.id not in keep_employeebank:
                ebank.delete()
        return instance


########### Nested ViewSet - Post Employee - Bank #########################

# ######################## Employee User ##########################


# ##########Nested Get - Post Employee - Bank ##########

class EmployeeUserBankViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBank
        fields = ('id', 'UserIDUserBank', 'EmployeeIDUserBank', 'AddressIDUserBank', 'idTK', 'ownTK', 'BankName',
                  'BranchName', 'DateCreate', 'DateAuth')
        read_only_fields = ('id', 'UserIDUserBank', 'EmployeeIDUserBank',)


# ##########Nested Get - Post Employee - Bank ##########

class EmployeeUserBankDetailSerializer(serializers.ModelSerializer):
    employeebank = EmployeeUserBankViewSetSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('id', 'UserNoted', 'employeebank',)

    def update(self, instance, validated_data):
        # course = Course.objects.get(instance)
        userbankid = validated_data.pop('employeebank')
        instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
        instance.save()
        for ebank in userbankid:
            if 'id' in ebank.keys():
                if UserBank.objects.filter(id=ebank['id']).exists():
                    e = UserBank.objects.get(id=ebank['id'])
                    e.AddressIDUserBank = ebank.get('AddressIDUserBank', e.AddressIDUserBank)
                    e.idTK = ebank.get('idTK', e.idTK)
                    e.ownTK = ebank.get('ownTK', e.ownTK)
                    e.BankName = ebank.get('BankName', e.idTK)
                    e.BranchName = ebank.get('BranchName', e.BranchName)
                    e.DateCreate = ebank.get('DateCreate', e.DateCreate)
                    e.DateAuth = ebank.get('DateAuth', e.DateAuth)
                    e.save()
                else:
                    continue
            else:
                UserBank.objects.create(EmployeeID=instance, UserIDBank=instance.UserIDEmployee, **ebank)
        return instance


# ############################### Employee User #####################################


# ########## Nested ViewSet - Post Employee - Educate #########################

# check isFinishCVSerializer
class isFinishCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumVitae
        fields = ('id', 'isFinishCV')
        read_only_fields = ('id', 'isFinishCV',)


# education - checkbox
################## Create - CV -  Education####################
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


class EmployeeEducateViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = (
            'id',
            'UserIDEducation',
            'EmployeeIDEducation',
            'EducationalInstitution',
            'Specialized',
            'Language',
            'DateTimeSupply',
            'DateTimeEnd',
            'DegreeLevel',
            'Degree',
            'DegreePhotoBefor',
            'DegreePhotoAfter'

        )
        read_only_fields = (
            'id',
            'EmployeeIDEducation',
            'UserIDEducation',
        )


class EmployeeEducateDetailSerializer(serializers.ModelSerializer):
    employeeeducate = EmployeeEducateViewSetSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('id', 'UserNoted', 'employeeeducate',)

    def update(self, instance, validated_data):
        # course = Course.objects.get(instance)
        employeeeducate = validated_data.pop('employeeeducate')
        instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
        instance.save()
        for edu in employeeeducate:
            if 'id' in edu.keys():
                if Education.objects.filter(id=edu['id']).exists():
                    e = Education.objects.get(id=edu['id'])
                    e.DateTime_Supply = edu.get('DateTime_Supply', e.DateTime_Supply)
                    e.EducationalInstitution = edu.get('EducationalInstitution', e.EducationalInstitution)
                    e.Specialized = edu.get('Specialized', e.Specialized)
                    e.Language = edu.get('Language', e.Language)
                    e.Role = edu.get('Role', e.Role)
                    e.Degree = edu.get('Degree', e.Degree)
                    e.DegreePhoto = edu.get('DegreePhoto', e.DegreePhoto)
                    e.CV = edu.get('CV', e.CV)
                    e.save()
                    # keep_employeebank.append(c.id)
                else:
                    continue
            else:
                Education.objects.create(EmployeeIDEducation=instance, UserIDEducation=instance.UserIDEducation, **edu)
        return instance


# ************************************** Employer - Address *************************
class EmployeeAdressViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'id', 'UserIDAddress', 'EmployeeIDAddress', 'Place', 'Ward', 'District', 'Province', 'Nation',)
        # 'AddressFull', )
        read_only_fields = ('id', 'UserIDAddress', 'EmployeeIDAddress', 'AddressFull')


# ***************************** Detail - Employer - Address ****************************
class EmployeeAddressDetailSerializer(serializers.ModelSerializer):
    employeeaddress = EmployeeAdressViewSetSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('id', 'UserNoted', 'employeeaddress',)

    def update(self, instance, validated_data):
        employeraddress = validated_data.pop('employeeaddress')
        instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
        instance.save()
        for eeadd in employeraddress:
            if 'id' in eeadd.keys():
                if Address.objects.filter(id=eeadd['id']).exists():
                    a = Address.objects.get(id=eeadd['id'])
                    a.Place = eeadd.get('Place', a.Place)
                    a.Ward = eeadd.get('Ward', a.Ward)
                    a.District = eeadd.get('District', a.District)
                    a.Province = eeadd.get('Province', a.Province)
                    a.Nation = eeadd.get('Nation', a.Nation)
                    a.save()
                else:
                    continue
            else:
                Address.objects.create(EmployeeIDAddress=instance, UserIDAddress=instance.UserIDAddress, **eeadd)
        return instance


# *************************************** Experiences **********************************************************
class EmployeeExperiencesViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiences
        fields = ('id', 'UserIDExperiences', 'EmployeeIDExperiences', 'ExperiencesName', 'ComName', 'Position',
                  'isCurrentPosition', 'TimeWorkFrom', 'TimeWorkTo', 'JobDescription', 'JobAchievements', 'TimeWork',
                  'Language')

        read_only_fields = ('id', 'UserIDExperiences', 'EmployeeIDExperiences')


# ***************************** Detail - Employer - Address ****************************
class EmployeeExperiencesDetailSerializer(serializers.ModelSerializer):
    employerexperiences = EmployeeExperiencesViewSetSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('id', 'UserNoted', 'employerexperiences',)

    def update(self, instance, validated_data):
        employerexperiences = validated_data.pop('employerexperiences')
        instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
        instance.save()
        for eexperi in employerexperiences:
            if 'id' in eexperi.keys():
                if Experiences.objects.filter(id=eexperi['id']).exists():
                    a = Experiences.objects.get(id=eexperi['id'])
                    a.ExperiencesName = eexperi.get('ExperiencesName', a.ExperiencesName)
                    a.ComName = eexperi.get('ComName', a.ComName)
                    a.Position = eexperi.get('Position', a.Position)
                    a.TimeSince = eexperi.get('TimeSince', a.TimeSince)
                    a.TimeUntill = eexperi.get('TimeUntill', a.TimeUntill)
                    a.CurriculumVitaeExperiences = eexperi.get('CurriculumVitaeExperiences', a.TimeWork)
                    a.save()
                else:
                    continue
            else:
                Experiences.objects.create(EmployeeIDExperiences=instance, UserIDExperiences=instance.UserIDExperiences,
                                           **eexperi)
        return instance


# ########## Nested ViewSet - Post Employee - CurriculumVitae #########################
class EmployeeCurriculumVitaeViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumVitae
        fields = ('id', 'UserIDCurriculumVitae', 'EmployeeIDCurriculumVitae', 'ProfileIDCurriculumVitae',
                  'AddressWorkIDCurriculumVitae', 'CareerIDCurriculumVitae', 'ExperienceIDCurriculumVitae',
                  'EducateIDCurriculumVitae', 'WorkLocationIDCurriculumVitae', 'ShiftIDCurriculumVitae', 'Title',
                  'DesiredPositionIDCurriculumVitae', 'FullName', 'Sex', 'BirthDay', 'Phone', 'MaritalStatus',
                  'Email', 'HealthCertification', 'Insurrance', 'Introduce', 'FormOfWork', 'WorkLocation',
                  'DesiredSalary', 'Skill', 'PersonalSkill', 'DateTime_create', 'DateTime_update')
        read_only_fields = ('id', 'UserIDCurriculumVitae', 'EmployeeIDCurriculumVitae', 'ProfileIDCurriculumVitae')


class EmployeeCurriculumVitaeDetailSerializer(serializers.ModelSerializer):
    employeecurriculumvitae = EmployeeCurriculumVitaeViewSetSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('id', 'UserNoted', 'employeecurriculumvitae',)

    def update(self, instance, validated_data):
        # course = Course.objects.get(instance)
        employeeecurriculumvitae = validated_data.pop('employeecurriculumvitae')
        instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
        instance.save()
        for curri in employeeecurriculumvitae:
            if 'id' in curri.keys():
                if CurriculumVitae.objects.filter(id=curri['id']).exists():
                    c = CurriculumVitae.objects.get(id=curri['id'])
                    c.Title = curri.get('Title', c.Title)
                    c.FullName = curri.get('FullName', c.FullName)
                    c.Sex = curri.get('Sex', c.Sex)
                    c.BirthDay = curri.get('BirthDay', c.BirthDay)
                    c.Phone = curri.get('Phone', c.Phone)
                    c.MaritalStatus = curri.get('MaritalStatus', c.MaritalStatus)
                    c.Email = curri.get('Email', c.Email)
                    c.Address = curri.get('Address', c.Address)
                    # c.HealthCertification = curri.get('HealthCertification', c.HealthCertification)
                    # c.Insurrance = curri.get('Insurrance', c.Insurrance)
                    c.Introduce = curri.get('Introduce', c.Introduce)
                    c.Career = curri.get('Career', c.Career)
                    c.FormOfWork = curri.get('FormOfWork', c.FormOfWork)
                    c.WorkLocation = curri.get('WorkLocation', c.WorkLocation)
                    c.DesiredSalary = curri.get('DesiredSalary', c.DesiredSalary)
                    c.Experience = curri.get('Experience', c.Experience)
                    c.Skill = curri.get('Skill', c.Skill)
                    c.Interests = curri.get('Interests', c.Interests)
                    c.save()
                else:
                    continue
            else:
                CurriculumVitae.objects.create(EmployeeIDCurriculumVitae=instance,
                                               UserIDCurriculumVitae=instance.UserIDEducate, **curri)
        return instance


# ******************************** get id CV *************************************
# check isFinishCVSerializer
class isFinishCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumVitae
        fields = ('id', 'isFinishCV')
        read_only_fields = ('id', 'isFinishCV',)


# ************************************** Array education CV ***********************************
# education - checkbox
################## Create - CV -  Education####################
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


################################ CV ######################################

class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumVitae
        fields = ('id',
                  'Title',
                  'MaritalStatus',
                  'Introduce',
                  'Career',
                  'FormOfWork',
                  'DesiredSalary',
                  'Skill',
                  'ProfileIDCurriculumVitae',
                  'AddressIDCurriculumVitae',

                  'EducationIDCurriculumVitae',
                  'CareerIDCurriculumVitae',
                  'WorkLocationIDCurriculumVitae',
                  # 'ShiftIDCurriculumVitae',
                  'DesiredPositionIDCurriculumVitae',

                  'UserIDCurriculumVitae',
                  'EmployeeIDCurriculumVitae',
                  'DateTime_create',
                  'DateTime_update',
                  )
        read_only_fields = ('id',
                            'UserIDCurriculumVitae',
                            'EmployeeIDCurriculumVitae',
                            'DateTime_create',
                            'DateTime_update',
                            )


################################ CV ######################################

############################# APPLY JOB ##################################


class JobApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApply
        fields = ('id',
                  'UserIDJobApply',
                  'EmployeeIDJobApply',
                  'EmployerIDJobApply',
                  'JobIDJobApply',
                  'CurriculumVitaeIDJobApply',
                  'DatetimeApply',
                  'DateStartWork',
                  'DateEndWork',
                  'DateNoWork',
                  'DateWork',
                  'TimeStartWork',
                  'TimeEndWork',
                  'TimeNoWork',
                  'TimeWork',
                  'AddressWork',
                  'UserIDJobCreate',
                  'isEmployerAgree',
                  'JobIDName',
                  # 'SalaryTime',
                  # 'SalaryDate',
                  # 'LocationWork',
                  # 'Wage',
                  # 'WageReal',
                  # 'Tip',
                  # 'Punish',
                  # 'Total',
                  )
        # 'DateWorkReal','TimeWorkReal','TotalReal'
        read_only_fields = ('id',
                            'UserIDJobApply',
                            'EmployeeIDJobApply',
                            'isEmployerAgree',
                            'DateWork',
                            'JobIDName',
                            'TimeWork',)


############################# APPLY JOB ###################################

# ################################# Career ################################
class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ('id', 'UserIDCareer', 'EmployeeIDCareer', 'MainCareerIDCareer', 'Level1CareerIDCareer',
                  'Level2CareerIDCareer', 'Level3CareerIDCareer', 'NameCareer')
