################################ Library #####################################

import os
import sys
from django.core import validators
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
# from jwtauth.models import Profile
from addressgojoco.models import *

User = get_user_model()

################################ Library #####################################

##################### Functions RegexValidator ###############################

name_regex = validators.RegexValidator(
    regex=r'^(?=.{1,})([aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiI'
          r'ìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyY'
          r'ỳỲỷỶỹỸýÝỵỴzZ+\s+])*$',
    message="Name required a-zA-Z, not number and special characters",
)
# Validate trường Phone
phone_regex = validators.RegexValidator(
    regex=r'^(?=.{1,})([0-9]{9,14})*$',
    message="Phone required 10 characters 0-9",
)


##################### Functions RegexValidator ###############################

############################### Functions ####################################

def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"users/{instance.pk}//{instance.UserProfile}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


def upload_to_userattphoto(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"users/{instance.UserIDAttPhoto}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


def upload_to_education(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"users/{instance.UserIDEducation}/Employee/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


def upload_to_company(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"users/{instance.UserIDCompany}/Company/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


def upload_to_job(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"users/{instance.UserIDJob}/Jobs/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


def upload_to_checkinout(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"users/{instance.UserIDCheckInOut}/CheckInOut/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


############################### Functions ####################################

################################ Address #####################################

class Address(models.Model):
    UserIDAddress = models.ForeignKey(User, on_delete=models.CASCADE)
    CountryIDAddress = models.ForeignKey(Country, related_name='AddressIDCurriculumVitae', on_delete=models.SET_NULL,
                                         null=True)
    ProvinceCityIDAddress = models.ForeignKey(ProvinceCity, related_name='AddressIDCurriculumVitae',
                                              on_delete=models.SET_NULL, null=True)
    DistrictIDAddress = models.ForeignKey(District, related_name='AddressIDCurriculumVitae', on_delete=models.SET_NULL,
                                          null=True)
    WardIDAddress = models.ForeignKey(Ward, related_name='AddressIDCurriculumVitae', on_delete=models.SET_NULL,
                                      null=True)
    NoLoad = models.CharField(max_length=50)
    NameStreet = models.CharField(max_length=100)
    AddressLine = models.CharField(max_length=100, default=None, null=True, blank=True)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "Address"

    def save(self, *args, **kwargs):
        self.AddressLine = 'Số ' + self.NoLoad + ', ' + self.NameStreet + ', ' + \
                           self.WardIDAddress.NameWard + ', ' + \
                           self.DistrictIDAddress.NameDistrict + ', ' + \
                           self.ProvinceCityIDAddress.NameProvinceCity + ', ' + \
                           self.CountryIDAddress.NameCountry
        super(Address, self).save(*args, **kwargs)

    def __str__(self):
        return self.AddressLine


################################ Address #####################################

################################ Profile #####################################

class Profile(models.Model):
    UserProfile = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileserializer')
    Designation = models.CharField(max_length=20, null=False, blank=False)
    Salary = models.IntegerField(null=True, blank=True)
    Picture = models.ImageField(upload_to='pictures/%Y/%m/%d/', max_length=255, null=True, blank=True)

    # Thông Tin Tài Khoản
    UserPhone = models.CharField(max_length=128, validators=[phone_regex])
    Email = models.EmailField()
    # EmailToken = models.CharField(max_length=128)
    UserEnabled = models.BooleanField(default=True)
    isEmployee = models.BooleanField(default=False)
    isEmployer = models.BooleanField(default=False)
    # IDWallet = models.OneToOneField(Wallet, on_delete=models.CASCADE, related_name='UserInfo')
    UserInfoStatusID = models.IntegerField()  # Status's AccountUser

    # Họ Và Tên
    UserFirstName = models.CharField(max_length=128, validators=[name_regex])
    UserMiddleName = models.CharField(max_length=128, validators=[name_regex])
    UserLastName = models.CharField(max_length=128, validators=[name_regex])
    UserFullName = models.CharField(max_length=256)

    AddressIDProfile = models.ForeignKey(Address, on_delete=models.CASCADE)
    City = models.CharField(max_length=128)
    Country = models.CharField(max_length=128)
    PostalCode = models.IntegerField()
    Description = models.TextField()
    UserImage = models.ImageField(upload_to=upload_to, max_length=255, null=True, blank=True)
    # ProfileImage = models.ForeignKey(User, on_delete=models.CASCADE,)

    # Ngày Nơi - GT Sinh
    UserBirthDay = models.DateField()
    UserBirthPlace = models.IntegerField()
    UserSex = models.CharField(max_length=128)
    # UserPhoto = models.ImageField(AttPhoto, on_delete=models.CASCADE, related_name='AttPhoto')
    MaritalStatus = models.CharField(max_length=128)  # Tình trạng hôn nhân
    UserNationality = models.CharField(max_length=128)  # Quốc tịch
    UserNation = models.CharField(max_length=128)  # Quốc gia, dân tộc
    # UserAddress = models.CharField(Address, on_delete=models.CASCADE, related_name='Address')

    # Chứng Minh Nhân Dân
    # IDCMND = models.ForeignKey(CMND, on_delete=models.CASCADE, related_name='CMND')
    UserIDCard = models.CharField(max_length=128)
    IDCardPlaceOfIssue = models.CharField(max_length=128)  # Nơi Phát hành cmnd
    UserApplyDate = models.DateField()  # Ngày cấp
    UserNameDisplay = models.CharField(max_length=128)

    CMND1 = models.ImageField(upload_to=upload_to, max_length=255, null=True, blank=True)
    CMND2 = models.ImageField(upload_to=upload_to, max_length=255, null=True, blank=True)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "Profile"
        ordering = ('-Salary',)

    def save(self, *args, **kwargs):
        self.UserFullName = self.UserFirstName + ' ' + self.UserMiddleName + ' ' + self.UserLastName
        self.UserNameDisplay = self.UserProfile.username
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.UserProfile.username


################################ Profile #####################################

############################# Model Employee #################################

class Employee(models.Model):
    UserIDEmployee = models.OneToOneField(User, on_delete=models.CASCADE)
    UserProfileIDEmployee = models.OneToOneField(Profile, on_delete=models.CASCADE)
    isEmployee = models.BooleanField(default=False)
    UserNoted = models.TextField()

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    def __str__(self):
        return self.UserIDEmployee.username

    class Meta:
        db_table = "Employee"


############################## Employee User #################################

############################## Employer User #################################

class Employer(models.Model):
    UserIDEmployer = models.OneToOneField(User, on_delete=models.CASCADE)
    UserProfileIDEmployer = models.OneToOneField(Profile, on_delete=models.CASCADE)
    isEmployer = models.BooleanField(default=False)
    UserNoted = models.TextField()

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    def __str__(self):
        return self.UserIDEmployer.username

    class Meta:
        db_table = "Employer"


############################## Employer User #################################

############################### Model Note ###################################

class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    class Meta:
        db_table = "Note"

    def __str__(self):
        return self.title


############################### Model Note ###################################

############################# Model Course ####################################

class Course(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    IDC = models.IntegerField(null=False)
    code = models.CharField(max_length=5, null=False)
    title = models.CharField(max_length=30, null=False)
    duration = models.IntegerField(null=True)
    fee = models.IntegerField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Course"

    @property
    def company(self):
        return self.company_set.all()


############################# Model Course ####################################

################################ Company ######################################

class Company(models.Model):
    UserIDCompany = models.ForeignKey(User, on_delete=models.CASCADE)
    EmployerIDCompany = models.ForeignKey(Employer, on_delete=models.CASCADE)
    ComName = models.CharField(max_length=128)
    ComTel = models.IntegerField(validators=[phone_regex], null=True)
    ComFax = models.IntegerField(validators=[phone_regex], null=True)
    Logo = models.ImageField(upload_to=upload_to_company, max_length=1368,
                             null=True, height_field=None, width_field=None, )
    LogoThumnail = models.ImageField(upload_to=upload_to_company, max_length=1368,
                                     null=True, height_field=None, width_field=None, )
    ComTax = models.IntegerField(validators=[phone_regex], null=True)
    ComEmail = models.EmailField(max_length=128, null=True)
    ComWeb = models.CharField(max_length=128)

    Status = models.CharField(max_length=128, default='Not Verify')
    AddressIDCompany = models.ForeignKey(Address, on_delete=models.CASCADE, null=False)

    # BranchCom = models.ForeignKey(BranchCompany, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.ComName

    class Meta:
        db_table = "Company"


################################ Company ######################################

############################### Bank User #####################################

class UserBank(models.Model):
    idTK = models.IntegerField(null=False)
    ownTK = models.CharField(max_length=128)
    BankName = models.CharField(max_length=128)
    BranchName = models.CharField(max_length=128)
    UserIDBank = models.ForeignKey(User, on_delete=models.CASCADE)  # Người Tạo
    EmployeeIDBank = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employeebank')
    EmployerIDBank = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='employerbank')
    dateCreate = models.DateTimeField(auto_now_add=True)
    dateAuth = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "UserBank"

    def __str__(self):
        return self.BankName


############################### Bank User #####################################

################################ Schedule #####################################

class Schedule(models.Model):
    UserIDShedule = models.ForeignKey(User, on_delete=models.CASCADE)

    # CurriculumVitaeIDShedule = models.ForeignKey(CurriculumVitae, on_delete=models.CASCADE)
    EmployerIDSchedule = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='emlpoyeridschedule')
    EmployeeIDSchedule = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='emlpoyeeidschedule')

    CompanyIDSchedule = models.ForeignKey(Company, on_delete=models.CASCADE)
    SchID = models.IntegerField()  # IDsu dung cho cong ty
    SchName = models.CharField(max_length=128)
    # InOutIDSchedule = models.ForeignKey(InOut, on_delete=models.CASCADE)  # Link inout
    DateStartWork = models.DateField()
    DateEndWork = models.DateField()
    DateWork = models.IntegerField()

    # DateScheduleInOut = models.ManyToManyField(DateInout)

    IsWeekend = models.BooleanField(default=True)
    IsAbsentSat = models.BooleanField(default=True)
    IsAbsentSun = models.BooleanField(default=True)
    IsAbsentHol = models.BooleanField(default=True)
    IsCountHol = models.BooleanField(default=True)
    CycleMode = models.IntegerField()
    IsDateOfOutTime = models.BooleanField(default=True)
    isSchedule = models.BooleanField(default=True)

    # Test CSDL Calender

    title = models.CharField(max_length=128)
    start = models.DateTimeField()
    end = models.DateTimeField()

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "Schedule"

    def __str__(self):
        return self.SchName

    # def save(self, *args, **kwargs):
    #     self.DateWork = (self.DateEndWork - self.DateStartWork).days
    #     super(Schedule, self).save(*args, **kwargs)


################################ Schedule #####################################

############################### PhotoCard #####################################

class PhotoCard(models.Model):
    UserIDPhotoCard = models.ForeignKey(User, on_delete=models.CASCADE)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "Photo"


############################### PhotoCard #####################################

################################## Jobs #######################################

class Jobs(models.Model):
    UserIDJob = models.ForeignKey(User, on_delete=models.CASCADE)
    EmployerIDJob = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='employerjobs')
    CompanyIDJob = models.ForeignKey(Company, on_delete=models.CASCADE)
    AddressIDJob = models.ForeignKey(Address, on_delete=models.CASCADE)
    # JobClassificationIDJob = models.ForeignKey(JobClassification, on_delete=models.CASCADE, null=True)
    ScheduleIDJob = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    # DegreeIDJob = models.ForeignKey(Degree, on_delete=models.CASCADE, null=True)
    # CurrencyIDJob = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)

    JobTitle = models.CharField(max_length=128)
    JobType = models.CharField(max_length=128)
    JobRole = models.CharField(max_length=128)
    ImageJob = models.ImageField(upload_to=upload_to_job, max_length=255, null=True, height_field=None,
                                 width_field=None)
    JobRequirements = models.CharField(max_length=128)
    JobExperience = models.CharField(max_length=128)
    JobDescription = models.CharField(max_length=128)
    MinSalary = models.CharField(max_length=128)
    MaxSalary = models.CharField(max_length=128)
    DateTime_create = models.DateTimeField(auto_now_add=True)
    DateTime_update = models.DateTimeField(auto_now=True)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "Jobs"

    def __str__(self):
        return self.JobTitle


################################## Jobs #######################################

################################# CVApply #####################################

class CVApply(models.Model):
    UserIDCVApply = models.ForeignKey(User, on_delete=models.CASCADE)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "CVApply"


################################# CVApply #####################################

################################# TaxCode #####################################

class TaxCode(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "TaxCode"


################################# TaxCode #####################################

############################# CurriculumVitae #################################
#
# class CurriculumVitae(models.Model):
#     UserIDCurriculumVitae = models.ForeignKey(User, on_delete=models.CASCADE, )
#     ProfileIDCurriculumVitae = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     DesiredPositionIDCurriculumVitae = models.CharField(max_length=256)  # Vị Trí mong muốn
#     DesiredLevelIDCurriculumVitae = models.ForeignKey(JobLevel, on_delete=models.CASCADE, null=True,
#                                                       related_name='DesiredLevelIDCurriculumVitae')  # Vị Trí Mong Muốn
#     CurrentLevelIDCurriculumVitae = models.ForeignKey(JobLevel, on_delete=models.CASCADE, null=True,
#                                                       related_name='CurrentLevelIDCurriculumVitae')  # Vị Trí Hiện tại
#     AddressIDCurriculumVitae = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)  # Search
#     isFinishCV = models.BooleanField(default=True)
#     FormOfWork = models.CharField(max_length=128)  # Hình thức làm việc
#     JobClassificationIDCurriculumVitae = models.ForeignKey(JobClassification, on_delete=models.CASCADE, null=True)
#     ScheduleIDCurriculumVitae = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
#     DegreeIDCurriculumVitae = models.ForeignKey(Degree, on_delete=models.CASCADE, null=True)
#     CurrentSalary = models.CharField(max_length=128)  # Mức lương hiện tại
#     DesiredSalary = models.CharField(max_length=128)  # Mức lương mong muốn
#     CurrencyIDCurriculumVitae = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
#     Introduce = models.TextField()  # Giới thiệu bản thân
#
#     FullName = models.CharField(max_length=128, validators=[name_regex])
#     Sex = models.CharField(max_length=128)
#     BirthDay = models.DateTimeField(auto_now_add=False)
#     Phone = models.IntegerField(validators=[phone_regex])
#     MaritalStatus = models.CharField(max_length=128)  # Tình trạng hôn nhân
#     Email = models.EmailField()
#     Address = models.CharField(max_length=128)
#     HealthCertification = models.ImageField()  # Giấy khám sức khỏe
#     Insurrance = models.ImageField()  # Bảo hiểm
#
#     Career = models.CharField(max_length=128)  # Nghề nghiệp
#     WorkLocation = models.CharField(max_length=128)  # Địa điểm muốn làm việc
#     Experience = models.TextField()  # Kinh nghiệm
#     Skill = models.TextField()  # Kỹ năng
#     Interests = models.TextField()  # Sở thích
#
#     # IDE = models.ForeignKey(
, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.DesiredPositionIDCurriculumVitae
#
#     class Meta:
#         db_table = "CurriculumVitae"


############################# CurriculumVitae #################################

############################### Educate User ##################################

class Education(models.Model):
    UserIDEducation = models.ForeignKey(User, on_delete=models.CASCADE, )
    EmployeeIDEducation = models.ForeignKey(Employee, on_delete=models.CASCADE)

    EducationalInstitution = models.CharField(max_length=128)  # Cơ sở đào tạo
    Specialized = models.CharField(max_length=128)  # Chuyên ngành

    DateTimeSupply = models.DateField(auto_now_add=False)  # Thời gian học
    DateTimeStart = models.DateField(auto_now_add=False)  # Thời gian học

    DateTimeEnd = models.DateField(auto_now_add=False)  # Thời gian học

    DegreeLevel = models.CharField(max_length=128)  # Loại tốt nghiệp
    Degree = models.CharField(max_length=128)  # Tên bằng tốt nghiệp
    DegreePhotoBefor = models.ImageField(upload_to=upload_to_education, max_length=255, null=True, height_field=None,
                                         width_field=None, )  # Hình ảnh bằng tốt nghiệp 1
    DegreePhotoAfter = models.ImageField(upload_to=upload_to_education, max_length=255, null=True, height_field=None,
                                         width_field=None, )  # Hình ảnh bằng tốt nghiệp 2

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "Education"

    def __str__(self):
        return self.Degree


############################### Educate User ##################################


################################ Experiences ##################################

class Experiences(models.Model):
    UserIDExperiences = models.ForeignKey(User, on_delete=models.CASCADE)
    EmployeeIDExperiences = models.ForeignKey(Employee, on_delete=models.CASCADE)
    ExperiencesName = models.CharField(max_length=1368)
    ComName = models.CharField(max_length=1368)  # models.ManyToManyField(Company)
    isCurrentPosition = models.BooleanField(default=False)
    Position = models.CharField(max_length=128)
    TimeWorkFrom = models.DateField(auto_now_add=False)
    TimeWorkTo = models.DateField(auto_now_add=False)

    JobDescription = models.TextField()
    JobAchievements = models.TextField()
    TimeWork = models.CharField(max_length=128)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "Experiences"

    def __str__(self):
        return self.ExperiencesName


################################ Experiences ##################################

################################# Insurance ###################################

class Insurance(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "Insurance"


################################# Insurance ###################################

################################# Languages ###################################

class Languages(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Languages"


################################# Languages ###################################

################################### Shift #####################################

class Shift(models.Model):
    UserIDShift_Create = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    UserIDShift_Update = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "Shift"


################################### Shift #####################################

################################# ShiftInOut ##################################

class ShiftInOut(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "ShiftInOut"


################################# ShiftInOut ##################################

################################# Career ######################################

class Career(models.Model):
    UserIDCareer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='useridcareer')
    EmployeeIDCareer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True,
                                         related_name='employeeidcareer')
    EmployerIDCareer = models.ForeignKey(Employer, on_delete=models.SET_NULL, null=True,
                                         related_name='employeridcareer')
    MainCareerIDCareer = models.ForeignKey(MainCareer, on_delete=models.SET_NULL, null=True,
                                           related_name='maincareeridcareer')
    Level1CareerIDCareer = models.ForeignKey(Level1Career, on_delete=models.SET_NULL, null=True,
                                             related_name='level1careeridcareer')
    Level2CareerIDCareer = models.ForeignKey(Level2Career, on_delete=models.SET_NULL, null=True,
                                             related_name='level2careeridcareer')
    Level3CareerIDCareer = models.ForeignKey(Level3Career, on_delete=models.SET_NULL, null=True,
                                             related_name='level3careeridcareer')
    NameCareer = models.CharField(max_length=128)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "Career"

    def __str__(self):
        return self.NameCareer

    def save(self, *args, **kwargs):
        self.NameCareer = self.MainCareerIDCareer.NameMainCareer + ' >> ' + \
                          self.Level1CareerIDCareer.NameLevel1Career + ' >> ' + \
                          self.Level2CareerIDCareer.NameLevel2Career + ' >> ' + \
                          self.Level3CareerIDCareer.NameLevel3Career
        super(Career, self).save(*args, **kwargs)


################################# Career ######################################

################################# Wallet ######################################

class Wallet(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "Wallet"


################################# Wallet ######################################

############################ InFoCheckinout ####################################

class InFoCheckinout(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    TimeSum = models.CharField(max_length=128)
    Late = models.BooleanField(default=True)
    SumSalary = models.CharField(max_length=128)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "InFoCheckinout"


############################ InFoCheckinout ####################################

################################ DateInOut #####################################

class DateInOut(models.Model):
    UserIDDateInOut = models.ForeignKey(User, on_delete=models.CASCADE)
    EmployerIDDateInOut = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='employerinout1')
    CompanyIDDateInOut = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employerinout2')
    EmployeeIDDateInOut = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employerinout3')
    ScheduleIDDateInOut = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='dateinoutschedule')
    DateIDInOut = models.DateField()
    TimeIn = models.TimeField(auto_now_add=False)
    TimeOut = models.TimeField(auto_now_add=False)
    InOutCode = models.CharField(max_length=32)
    InOutName = models.TextField()
    StartIn = models.DateTimeField(auto_now_add=False)
    EndIn = models.DateTimeField(auto_now_add=False)
    StartOut = models.DateTimeField(auto_now_add=False)
    EndOut = models.DateTimeField(auto_now_add=False)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "DateInOut"

    def __str__(self):
        t = str(self.DateIDInOut)
        return t


################################ DateInOut #####################################

################################### InOut ######################################

class InOut(models.Model):
    UserIDInOut = models.ForeignKey(User, on_delete=models.CASCADE)
    EmployerIDInOut = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='employerinout')
    CompanyIDInOut = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employerinout')
    EmployeeIDInOut = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employerinout')
    ScheduleIDInOut = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='inoutidschedule')

    DateInOutIDInOut = models.ManyToManyField(DateInOut, related_name='inoutdateinoutschedule')

    DateInOutIDInOutSchedule = models.ForeignKey(DateInOut, on_delete=models.CASCADE, related_name='inoutdateinout')

    InOutName = models.TextField()
    TimeIn = models.TimeField(auto_now_add=True)
    TimeOut = models.TimeField(auto_now_add=True)

    TimeInReal = models.TimeField(auto_now_add=False)
    TimeOutReal = models.TimeField(auto_now_add=False)

    InOutCode = models.CharField(max_length=32)

    StartIn = models.DateTimeField(auto_now_add=False)
    EndIn = models.DateTimeField(auto_now_add=False)
    StartOut = models.DateTimeField(auto_now_add=False)
    EndOut = models.DateTimeField(auto_now_add=False)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "InOut"

    def __str__(self):
        t = str(self.id)
        return self.InOutName

    # # Add fields checkinout
    # Odd_Even = models.IntegerField()
    # OriginType = models.CharField(max_length=128)
    # NewType = models.CharField(max_length=128)
    # Source = models.CharField(max_length=128)
    # TimeStr = models.CharField(max_length=128)


################################### InOut ######################################


#################################### Bank ######################################

class Bank(models.Model):
    BankName = models.CharField(max_length=128)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "Bank"


#################################### Bank ######################################

################################ WorkLocation ##################################

class WorkLocation(models.Model):
    UserIDWorkLocation = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=128)
    CountryIDWorkLocation = models.ForeignKey(Country, on_delete=models.CASCADE)
    ProvinceCityIDWorkLocation = models.ForeignKey(ProvinceCity, on_delete=models.CASCADE, null=True)
    DistrictIDWorkLocation = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    WardIDWorkLocation = models.ForeignKey(Ward, on_delete=models.CASCADE, null=True)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "WorkLocation"

    def __str__(self):
        return self.Title


################################ WorkLocation ##################################

##################################### CV #######################################

class CurriculumVitae(models.Model):
    # Các khóa ngoại
    UserIDCurriculumVitae = models.ForeignKey(User, on_delete=models.CASCADE)  # Khóa ngoại về bảng User
    EmployeeIDCurriculumVitae = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                                  related_name='employeecurriculumvitae')  # Khóa ngoại về bảng Employee
    ProfileIDCurriculumVitae = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Khóa ngoại về bảng Profile
    AddressWorkIDCurriculumVitae = models.ForeignKey(Address, on_delete=models.CASCADE)  # Khóa ngoại về bảng Address
    CareerIDCurriculumVitae = models.ForeignKey(Career, on_delete=models.CASCADE)  # Khóa ngoại về bange Career

    ExperienceIDCurriculumVitae = models.ManyToManyField(Experiences)  # Many-to-many về bảng Experiences
    EducateIDCurriculumVitae = models.ManyToManyField(Education)  # Many-to-many về bảng Education
    WorkLocationIDCurriculumVitae = models.ManyToManyField(WorkLocation)  # Many-to-many về bảng WorkLocation
    ShiftIDCurriculumVitae = models.ManyToManyField(Shift)  # Many-to-many về bảng Shift

    # Thông tin CV
    Title = models.CharField(max_length=128)  # Tiêu đề CV
    DesiredPositionIDCurriculumVitae = models.CharField(max_length=1268)
    FullName = models.CharField(max_length=128, validators=[name_regex])
    Sex = models.CharField(max_length=128)
    BirthDay = models.DateField(auto_now_add=False)
    Phone = models.IntegerField(validators=[phone_regex])
    MaritalStatus = models.CharField(max_length=128)  # Tình trạng hôn nhân
    Email = models.EmailField()
    HealthCertification = models.ImageField()  # Giấy khám sức khỏe
    Insurrance = models.ImageField()  # Bảo hiểm
    Introduce = models.TextField()  # Giới thiệu bản thân
    FormOfWork = models.CharField(max_length=128)  # Hình thức làm việc
    WorkLocation = models.ForeignKey(ProvinceCity, on_delete=models.CASCADE)  # Địa điểm muốn làm việc
    DesiredSalary = models.CharField(max_length=128)  # Mức lương mong muốn
    Skill = models.CharField(max_length=128)  # Kỹ năng
    PersonalSkill = models.CharField(max_length=128)  # Kỹ năng cá nhân
    DateTime_create = models.DateTimeField(auto_now_add=True)
    DateTime_update = models.DateTimeField(auto_now=True)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "CV"
        ordering = ('id',)

    def __str__(self):
        return self.Title


##################################### CV #######################################

################################## AttPhoto ####################################

class AttPhoto(models.Model):
    TitleImage = models.CharField(max_length=128, null=True, blank=True)
    UserIDAttPhoto = models.ForeignKey(User, on_delete=models.CASCADE)
    UserPhoto = models.ImageField(upload_to=upload_to_userattphoto, max_length=255, null=True, height_field=None,
                                  width_field=None, )
    EmployeeIDAttPhoto = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employeeidattphoto')
    CVIDAttPhoto = models.ForeignKey(CurriculumVitae, on_delete=models.CASCADE)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "AttPhoto"

    def __str__(self):
        return self.TitleImage


################################## AttPhoto ####################################

################################## JobApply ####################################

class JobApply(models.Model):
    UserIDJobApply = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applyjob")
    UserIDJobCreate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applycreate")
    EmployeeIDJobApply = models.ForeignKey(Employee, on_delete=models.CASCADE)
    EmployerIDJobApply = models.ForeignKey(Employer, on_delete=models.CASCADE)
    JobIDJobApply = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    CurriculumVitaeIDJobApply = models.ForeignKey(CurriculumVitae, on_delete=models.CASCADE, related_name="onecv")

    DatetimeApply = models.DateTimeField(auto_now_add=True)
    DatetimeAgree = models.DateTimeField(auto_now=True)
    DatetimeFinish = models.DateTimeField(auto_now=True)
    DateStartWork = models.DateField()  # Ngày bắt đầu đi làm lấy từ bảng lập lịch của job
    DateEndWork = models.DateField()  # Ngày kết thúc đi làm lấy từ bảng lập lịch của job
    DateNoWork = models.DateField()  # Ngày ko đi làm lấy từ bảng lập lịch của job
    DateWork = models.IntegerField()  # Bao nhieu ngày làm ( tính)
    DateWorkReal = models.IntegerField()  # Chấm công
    SalaryDate = models.IntegerField(default=0)  # Tính theo ngày (tính)

    TimeStartWork = models.TimeField()  # Lấy từ bảng lập lịch của job
    TimeEndWork = models.TimeField()  # Lấy từ bảng lập lịch của job
    TimeNoWork = models.TimeField()  # Lấy từ bảng lập lịch của job
    TimeWork = models.FloatField()  # Bao nhiều giờ trong một ngày (tính)

    TimeWorkReal = models.IntegerField()  # Dừa vào vào bãng chấm công
    SalaryTime = models.IntegerField(default=0)  # Lấy từ bảng lập lịch của job

    AddressWork = models.ForeignKey(Address, on_delete=models.CASCADE)  # Lấy từ Job ra
    # LocationWork = models.ForeignKey(Location, on_delete=models.CASCADE)  # Lấy từ Job ra
    JobIDName = models.CharField(max_length=256)  # Tên Job
    Confirm = models.BooleanField()
    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    Wage = models.IntegerField()  # Tiền tạm tính theo lý thuyết
    WageReal = models.IntegerField()  # Thực tế
    Tip = models.IntegerField()  # Tự nhập
    Punish = models.IntegerField()
    Total = models.IntegerField()
    TotalReal = models.IntegerField()
    isEmployerAgree = models.BooleanField(null=True)

    # CurriculumVitaeIDJobApply = models.ManyToManyField(CurriculumVitae, related_name="manycv")

    class Meta:
        db_table = "JobApply"

    def save(self, *args, **kwargs):
        self.DateWork = (self.DateEndWork - self.DateStartWork).days
        self.TimeWork = round(((self.TimeEndWork.hour - self.TimeStartWork.hour) * 60 + (
                self.TimeEndWork.minute - self.TimeStartWork.minute)) / 60, 2)
        self.JobIDName = self.JobIDJobApply.JobTitle
        super(JobApply, self).save(*args, **kwargs)

    def __str__(self):
        return self.JobIDName


################################## JobApply ####################################

################################## InOutArr ####################################

class InOutArr(models.Model):
    UserIDInOutArr = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercreatecv')
    UserIDInOutCreate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercreatejob')
    EmployerIDInOutArr = models.ForeignKey(Employer, on_delete=models.CASCADE)
    EmployeeIDInOutArr = models.ForeignKey(Employee, on_delete=models.CASCADE)
    CompanyIDInOutArr = models.ForeignKey(Company, on_delete=models.CASCADE)
    JobApplyIDInOutArr = models.ForeignKey(JobApply, on_delete=models.CASCADE)
    JobsIDInOutArr = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    CVIDInOutArr = models.ForeignKey(CurriculumVitae, on_delete=models.CASCADE)
    ScheduleIDInOutArr = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    # DateInOutIDInOutArr = models.ForeignKey(DateInOut, on_delete=models.CASCADE)
    # InOutIDInOutArr = models.ForeignKey(InOut, on_delete=models.CASCADE)

    InOutCode = models.CharField(max_length=128)
    InOutName = models.CharField(max_length=128)
    AutoMax = models.IntegerField()
    AutoMin = models.IntegerField()
    AutoInterval = models.IntegerField()
    InOutMode = models.IntegerField()
    SelectMode = models.IntegerField()
    RemoveStart = models.CharField(max_length=128)
    RemoveEnd = models.CharField(max_length=128)
    GetMax = models.IntegerField()
    RemoveOut = models.BooleanField(default=True)
    DayCount = models.IntegerField()
    StartTime = models.CharField(max_length=128)
    EndTime = models.CharField(max_length=128)
    StartDay = models.IntegerField()
    InOutIDInOutArr = models.ManyToManyField(InOut)
    DateInOutIDInOutArr = models.ManyToManyField(DateInOut)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "InOutArr"


################################## InOutArr ####################################

################################## Location ####################################

class Location(models.Model):
    UserIDEmployee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    UserIDEmployer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    UserIDLocation = models.ForeignKey(User, on_delete=models.CASCADE)
    JobApplyIDLocation = models.ForeignKey(JobApply, on_delete=models.CASCADE)
    GPS_HIRE_LAT = models.FloatField()
    GPS_HIRE_LONG = models.FloatField()
    GPS_EMP_LAT = models.FloatField()
    GPS_EMP_LONG = models.FloatField()
    GPS_LOC_LAT = models.FloatField()
    GPS_LOC_LONG = models.FloatField()
    DIST_WALK = models.IntegerField()
    DIST_PLANE = models.IntegerField()
    ShiftID = models.IntegerField()
    ShiftCode = models.CharField(max_length=128)
    UserAccount = models.CharField(max_length=128)
    RoleID = models.IntegerField()
    TimeL = models.DateTimeField(auto_now_add=True)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    class Meta:
        db_table = "Location"


################################## Location ####################################

################################# CheckInOut ###################################

class CheckInOut(models.Model):
    UserIDCheckInOut = models.ForeignKey(User, on_delete=models.CASCADE, related_name='useridcreatecv')
    UserIDCreateJob = models.ForeignKey(User, on_delete=models.CASCADE, related_name='useridcreatejob')
    CompanyIDInOutArr = models.ForeignKey(Company, on_delete=models.CASCADE)
    JobApplyIDInOutArr = models.ForeignKey(JobApply, on_delete=models.CASCADE)
    ScheduleIDCheckInOut = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    DateInOutIDCheckInOut = models.ForeignKey(DateInOut, on_delete=models.CASCADE)
    InOutIDCheckInOut = models.ForeignKey(InOut, on_delete=models.CASCADE)

    DateCheckInOut = models.DateField(auto_now_add=True)
    TimeCheckInOut = models.TimeField(auto_now_add=True)
    DateTimeCheckInOut = models.DateTimeField(auto_now_add=True)
    isIn = models.BooleanField(default=False)
    isOut = models.BooleanField(default=False)
    # DateCheckOut = models.DateField(auto_now_add=True)
    # TimeCheckOut = models.TimeField(auto_now_add=True)

    TimeDateCheckInOut = models.DateTimeField(auto_now_add=False)
    TimeDateJobs = models.DateTimeField(auto_now_add=True)
    MachineNo = models.CharField(max_length=128)
    IPAddressCheckInOut = models.GenericIPAddressField(max_length=128)
    # CompanyIDCheckInOut = models.ForeignKey(Company, on_delete=models.CASCADE)  # Khóa ngoại với bảng company
    LocationIDCheckInOut = models.OneToOneField(Location, on_delete=models.CASCADE)  # Khóa ngoại với bảng Location
    ImageCheckInOut = models.ImageField(upload_to=upload_to_checkinout, max_length=255, null=True, blank=True)

    Language = models.ForeignKey(LanguageUser, on_delete=models.CASCADE)  # Ngôn ngữ

    # JobIDCheckInOut = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    # CurriculumVitaeIDCheckInOut = models.ForeignKey(CurriculumVitae, on_delete=models.CASCADE)

    class Meta:
        db_table = "CheckInOut"

    def __str__(self):
        t = str(self.JobApplyIDInOutArr.JobIDJobApply.JobTitle)
        return t

    def save(self, *args, **kwargs):
        self.ScheduleIDCheckInOut = self.JobApplyIDInOutArr.JobIDJobApply.ScheduleIDJob
        super(CheckInOut, self).save(*args, **kwargs)

################################# CheckInOut ###################################
