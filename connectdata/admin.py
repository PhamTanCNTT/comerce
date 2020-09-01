from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from connectdata.models import *
from django.contrib.auth import get_user_model
User = get_user_model()

admin.site.register(Course)
admin.site.register(Note)
admin.site.register(UserBank)
admin.site.register(CheckInOut)
admin.site.register(Company)
admin.site.register(InOut)
admin.site.register(InFoCheckinout)
admin.site.register(CurriculumVitae)
admin.site.register(Education)
admin.site.register(Wallet)
admin.site.register(AttPhoto)
admin.site.register(ShiftInOut)
admin.site.register(Jobs)
admin.site.register(JobApply)
admin.site.register(CVApply)
admin.site.register(Bank)
admin.site.register(TaxCode)
admin.site.register(Insurance)
admin.site.register(Experiences)
admin.site.register(Languages)
admin.site.register(Schedule)
admin.site.register(Shift)
admin.site.register(PhotoCard)
admin.site.register(Address)
admin.site.register(InOutArr)
admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(Profile)
admin.site.register(WorkLocation)
admin.site.register(Career)
