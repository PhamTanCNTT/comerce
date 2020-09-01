from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


################################ Currency ####################################

class Currency(models.Model):
    SymCurrency = models.CharField(max_length=30, unique=True, blank=True)
    NameCurrency = models.CharField(max_length=100, unique=True, blank=True)
    ValueCurrency = models.IntegerField()
    ValueVND = models.IntegerField()

    def __str__(self):
        return self.SymCurrency


################################ Currency ####################################

########################### JobClassification #################################

class JobClassification(models.Model):
    NameJobClassification = models.CharField(max_length=256, unique=True, blank=True)

    def __str__(self):
        return self.NameJobClassification


########################### JobClassification #################################

################################ Degree #######################################

class Degree(models.Model):
    NameDegree = models.CharField(max_length=256, unique=True, blank=True)

    def __str__(self):
        return self.NameDegree


################################ Degree #######################################

################################ JobLevel #####################################

class JobLevel(models.Model):
    NamePosition = models.CharField(max_length=256, unique=True, blank=True)

    def __str__(self):
        return self.NamePosition


################################ JobLevel #####################################

################################ Address ######################################

################################ Country ######################################

class Country(models.Model):
    UserIDCountry = models.ForeignKey(User, on_delete=models.CASCADE)
    NameCountry = models.CharField(max_length=100, unique=True, blank=True)
    CodeCountry = models.CharField(max_length=100, unique=True, blank=True)
    PopulationCountry = models.BigIntegerField(blank=True)

    def __str__(self):
        return self.NameCountry


################################ Country ######################################

############################# ProvinceCity ####################################

class ProvinceCity(models.Model):
    UserIDProvinceCity = models.ForeignKey(User, on_delete=models.CASCADE)
    NameProvinceCity = models.CharField(max_length=128, blank=True, unique=True)
    PopulationProvinceCity = models.IntegerField()
    CountryIDProvinceCity = models.ManyToManyField(Country, related_name='provincecity')
    CodeProvinceCity = models.IntegerField(blank=True)

    slug = models.CharField(max_length=128, blank=True)
    type = models.CharField(max_length=128, blank=True)
    name_with_type = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = "ProvinceCity"

    def __str__(self):
        return self.NameProvinceCity


############################# ProvinceCity ####################################

############################### District ######################################

class District(models.Model):
    UserIDDistrict = models.ForeignKey(User, on_delete=models.CASCADE)
    NameDistrict = models.CharField(max_length=128, unique=True, blank=True)
    PopulationDistrict = models.IntegerField()
    ProvinceCityIDDistrict = models.ManyToManyField(ProvinceCity, related_name='provincecitydistrict')
    CodeDistrict = models.IntegerField()
    type = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    name_with_type = models.CharField(max_length=128)
    path = models.CharField(max_length=128)
    path_with_type = models.CharField(max_length=128)

    # parent_code = models.ForeignKey(ProvinceCity, on_delete=models.CASCADE)

    class Meta:
        db_table = "District"
        ordering = ('NameDistrict',)

    def __str__(self):
        return self.NameDistrict


############################### District ######################################

################################# Ward ########################################

class Ward(models.Model):
    UserIDWard = models.ForeignKey(User, on_delete=models.CASCADE)
    NameWard = models.CharField(max_length=100, unique=True, blank=True)
    PopulationWard = models.IntegerField()
    CodeWard = models.IntegerField()
    DistrictIDWard = models.ManyToManyField(District, related_name='districtward')
    type = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)

    class Meta:
        db_table = "Ward"

    def __str__(self):
        return self.NameWard


################################# Ward ########################################


class LanguageUser(models.Model):
    UserIDLanguage = models.ForeignKey(User, on_delete=models.CASCADE)
    NameLanguage = models.CharField(max_length=128)

    class Meta:
        db_table = "LanguageUser"

    def __str__(self):
        return self.NameLanguage


################################ Career ######################################

################################ MainCareer ##################################

class MainCareer(models.Model):
    UserIDMainCareer = models.ForeignKey(User, on_delete=models.CASCADE)
    NameMainCareer = models.CharField(max_length=100, unique=True, blank=True)
    CodeMainCareer = models.CharField(max_length=100)
    CountMainCareer = models.BigIntegerField(blank=True)

    def __str__(self):
        return self.NameMainCareer


################################ MainCareer ##################################

############################# Level1Career ###################################

class Level1Career(models.Model):
    UserIDLevel1Career = models.ForeignKey(User, on_delete=models.CASCADE)
    NameLevel1Career = models.CharField(max_length=128, blank=True)
    MainCareerIDLevel1Career = models.ManyToManyField(MainCareer, related_name='maincareer')
    CodeLevel1Career = models.CharField(max_length=100)
    CountLevel1Career = models.BigIntegerField(blank=True)

    class Meta:
        db_table = "Level1Career"

    def __str__(self):
        return self.NameLevel1Career


############################# Level1Career ###################################

############################### Level2Career #################################

class Level2Career(models.Model):
    UserIDLevel2Career = models.ForeignKey(User, on_delete=models.CASCADE)
    NameLevel2Career = models.CharField(max_length=128, unique=True, blank=True)
    Level1CareerIDLevel2Career = models.ManyToManyField(Level1Career, related_name='level1career')
    CodeLevel2Career = models.CharField(max_length=100)
    CountLevel2Career = models.BigIntegerField(blank=True)

    class Meta:
        db_table = "Level2Career"
        ordering = ('NameLevel2Career',)

    def __str__(self):
        return self.NameLevel2Career


############################### Level2Career #################################

################################# Level3Career ###############################

class Level3Career(models.Model):
    UserIDLevel3Career = models.ForeignKey(User, on_delete=models.CASCADE)
    NameLevel3Career = models.CharField(max_length=100, unique=True, blank=True)
    Level2CareerIDLevel3Career = models.ManyToManyField(Level2Career, related_name='level2career')
    CodeLevel3Career = models.CharField(max_length=100)
    CountLevel3Career = models.BigIntegerField(blank=True)

    class Meta:
        db_table = "Level3Career"

    def __str__(self):
        return self.NameLevel3Career

################################# Ward #######################################
