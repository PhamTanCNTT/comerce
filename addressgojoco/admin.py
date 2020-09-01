from __future__ import unicode_literals
from django.contrib import admin
from addressgojoco.models import *
    # Country, ProvinceCity, District, Ward, \
    # Currency, JobClassification, Degree, JobLevel, LanguageUser

admin.site.register(Country)
admin.site.register(ProvinceCity)
admin.site.register(District)
admin.site.register(Ward)
admin.site.register(Currency)
admin.site.register(JobClassification)
admin.site.register(Degree)
admin.site.register(JobLevel)
admin.site.register(LanguageUser)
admin.site.register(MainCareer)
admin.site.register(Level1Career)
admin.site.register(Level2Career)
admin.site.register(Level3Career)


