from rest_framework import serializers

from connectdata.models import *


################################# EMPLOYER #######################################

############################# EMPLOYER COMPANY ###################################

class EmployerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id',
                  'UserIDCompany',
                  'EmployerIDCompany',
                  'AddressIDCompany',
                  'ComName',
                  'ComTel',
                  'Logo',
                  # 'LogoThumnail',
                  'ComTax',
                  'ComEmail',
                  'ComWeb',
                  'Status')
        read_only_fields = ('id',
                            'EmployerIDCompany',
                            'UserIDCompany',
                            )


############################# EMPLOYER COMPANY ###################################

############################### EMPLOYER JOB #####################################

class EmployerJobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ('id',
                  'UserIDJob',
                  'EmployerIDJob',
                  'CompanyIDJob',
                  'AddressIDJob',
                  'ScheduleIDJob',
                  'JobTitle',
                  'JobType',
                  'JobRole',
                  'ImageJob',
                  'JobRequirements',
                  'JobExperience',
                  'JobDescription',
                  'MinSalary',
                  'MaxSalary',
                  'DateTime_create',
                  'DateTime_update'
                  )

        read_only_fields = ('id',
                            'UserIDJob',
                            'EmployerIDJob',
                            'DateTime_create',
                            'DateTime_update'
                            )


############################### EMPLOYER JOB #####################################

############################### Schedule JOB #####################################

class InOutJobSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = InOut
        fields = ('id',
                  'InOutName',
                  'TimeIn',
                  'TimeOut',
                  'UserIDInOut',
                  'EmployerIDInOut',
                  'ScheduleIDInOut',
                  )
        read_only_fields = ('id',
                            'UserIDInOut',
                            'EmployerIDInOut',
                            'ScheduleIDInOut',
                            )


class ScheduleJobSerializer(serializers.ModelSerializer):
    inoutidschedule = InOutJobSerializer(many=True)

    class Meta:
        model = Schedule
        fields = (
            'id',
            'UserIDShedule',
            'EmlpoyerIDSchedule',
            'SchName',

            'DateStartWork',
            'DateEndWork',
            'IsWeekend',
            'IsAbsentSat',
            'IsAbsentSun',
            'IsAbsentHol',
            'CycleMode',
            'DateWork',
            'inoutidschedule',
        )
        read_only_fields = (
            'id',
            'UserIDShedule',
            'EmlpoyerIDSchedule',
            'DateWork',
        )

    def create(self, validated_data):
        inoutidschedule = validated_data.pop('inoutidschedule')
        schedule = Schedule.objects.create(**validated_data)
        scheduleidinout = Employer.objects.get(UserIDEmployer=schedule.UserIDShedule)
        for inout in inoutidschedule:
            InOut.objects.create(**inout,
                                 EmployerIDInOut=scheduleidinout,
                                 UserIDInOut=schedule.UserIDShedule,
                                 ScheduleIDInOut=schedule)
        return schedule

    def update(self, instance, validated_data):
        inoutidschedule = validated_data.pop('inoutidschedule')
        instance.SchName = validated_data.get('SchName', instance.SchName)
        instance.DateStartWork = validated_data.get('DateStartWork', instance.DateStartWork)
        instance.DateEndWork = validated_data.get('DateEndWork', instance.DateEndWork)
        instance.IsWeekend = validated_data.get('IsWeekend', instance.IsWeekend)
        instance.IsAbsentSat = validated_data.get('IsAbsentSat', instance.IsAbsentSat)
        instance.CycleMode = validated_data.get('CycleMode', instance.CycleMode)
        instance.save()
        keep_inoutidschedule = []
        existing_ids = [c.id for c in instance.inoutidschedule.all()]
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
                scheduleidinout = Employer.objects.get(UserIDEmployer=instance.UserIDShedule)
                c = InOut.objects.create(**inout,
                                         EmployerIDInOut=scheduleidinout,
                                         UserIDInOut=c.UserIDInOut,
                                         ScheduleIDInOut=instance
                                         )
                keep_inoutidschedule.append(c.id)

        for inout in instance.inoutidschedule.all():
            if inout.id not in keep_inoutidschedule:
                inout.delete()
        return instance


############################### EMPLOYER JOB #####################################
############################### ScheduleDate #####################################

############################### ScheduleDate #####################################


class ScheduleDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            'id', 'title', 'start', 'end', 'UserIDShedule'
        )
        read_only_fields = ('id', 'UserIDShedule')


class ScheduleDatelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            'id', 'title', 'start', 'end',
        )

    read_only_fields = ('id')


################################# APPLY JOB ######################################

class EmployerJobApplyCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApply
        fields = ('id',
                  'UserIDJobCreate',
                  'EmployerIDJobApply',
                  'JobIDJobApply',
                  'CurriculumVitaeIDJobApply',
                  'CurriculumVitaeIDEmployer',
                  'isEmployerAgree',
                  'DatetimeApply',
                  'DatetimeAgree',
                  'DateStartWork',
                  'DateEndWork',
                  'DateNoWork',
                  # 'DateWork',
                  'TimeStartWork',
                  'TimeEndWork',
                  'TimeNoWork',
                  # 'TimeWork',
                  'AddressWork',
                  'SalaryTime',
                  'SalaryDate',
                  'LocationWork',
                  # 'Wage',
                  # 'WageReal',
                  # 'Tip',
                  # 'Punish',
                  # 'Total',
                  )
        # 'DateWorkReal','TimeWorkReal','TotalReal'
        read_only_fields = ('id',
                            'UserIDJobCreate',
                            'EmployerIDJobApply',
                            'JobIDJobApply',
                            'CurriculumVitaeIDJobApply',
                            'CurriculumVitaeIDEmployer',
                            # 'isEmployerAgree',
                            'DatetimeApply',
                            # 'DatetimeAgree'
                            'DateStartWork',
                            'DateEndWork',
                            'DateNoWork',
                            # 'DateWork',
                            'TimeStartWork',
                            'TimeEndWork',
                            'TimeNoWork',
                            # 'TimeWork',
                            'AddressWork',
                            'SalaryTime',
                            'SalaryDate',
                            'LocationWork',
                            # 'Wage',
                            # 'WageReal',
                            # 'Tip',
                            # 'Punish',
                            # 'Total',
                            )


class EmployerJobApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApply
        fields = ('id',
                  'UserIDJobCreate',
                  # 'EmployerIDJobApply',
                  # 'JobIDJobApply',
                  # 'CurriculumVitaeIDJobApply',
                  # 'CurriculumVitaeIDEmployer',
                  'isEmployerAgree',
                  # 'DatetimeApply',
                  # 'DatetimeAgree',
                  # 'DateStartWork',
                  # 'DateEndWork',
                  # 'DateNoWork',
                  # # 'DateWork',
                  # 'TimeStartWork',
                  # 'TimeEndWork',
                  # 'TimeNoWork',
                  # # 'TimeWork',
                  # 'AddressWork',
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
                            'UserIDJobCreate',
                            # 'EmployerIDJobApply',
                            # 'JobIDJobApply',
                            # 'CurriculumVitaeIDJobApply',
                            # 'CurriculumVitaeIDEmployer',
                            # 'isEmployerAgree',
                            # 'DatetimeApply',
                            # 'DatetimeAgree',
                            # 'DateStartWork',
                            # 'DateEndWork',
                            # 'DateNoWork',
                            # # 'DateWork',
                            # 'TimeStartWork',
                            # 'TimeEndWork',
                            # 'TimeNoWork',
                            # # 'TimeWork',
                            # 'AddressWork',
                            # 'SalaryTime',
                            # 'SalaryDate',
                            # 'LocationWork',
                            # 'Wage',
                            # 'WageReal',
                            # 'Tip',
                            # 'Punish',
                            # 'Total',
                            )


################################# APPLY JOB ######################################


####################### UPDATE SCHEDULE JOB DATE INOUT ###########################

########################## SCHEDULE JOB DATE INOUT ###############################


############################ SCHEDULE DATE INOUT #################################

class DateInOutSingleSerialzier(serializers.ModelSerializer):
    class Meta:
        model = DateInOut
        fields = ('id',
                  'UserIDDateInOut',
                  'EmployerIDDateInOut',
                  'CompanyIDDateInOut',
                  'ScheduleIDDateInOut',
                  'DateIDInOut')
        read_only_fields = ('id',
                            'UserIDDateInOut',
                            'EmployerIDDateInOut',
                            'CompanyIDDateInOut',
                            'ScheduleIDDateInOut',
                            )


class ScheduleDateTimeSerializer(serializers.ModelSerializer):
    dateinoutschedule = DateInOutSingleSerialzier(many=True)

    class Meta:
        model = Schedule
        fields = ('id',
                  'UserIDShedule',
                  'EmployerIDSchedule',
                  'CompanyIDSchedule',
                  'SchName',
                  'DateStartWork',
                  'DateEndWork',
                  'DateWork',
                  'IsWeekend',
                  'IsAbsentSat',
                  'IsAbsentSun',
                  'IsAbsentHol',
                  'CycleMode',
                  'dateinoutschedule',
                  )
        read_only_fields = ('id',
                            'UserIDShedule',
                            'EmployerIDSchedule',
                            # 'CompanyIDSchedule',
                            'DateWork',
                            )

    def create(self, validated_data):
        dateinout_data = validated_data.pop('dateinoutschedule')
        sch = Schedule.objects.create(**validated_data)
        for dateinout in dateinout_data:
            DateInOut.objects.create(**dateinout, UserIDDateInOut=sch.UserIDShedule,
                                     EmployerIDDateInOut=sch.EmployerIDSchedule,
                                     ScheduleIDDateInOut=sch,
                                     CompanyIDDateInOut=sch.CompanyIDSchedule,
                                     # CompanyIDSchedule = sch.CompanyIDSchedule,
                                     )
        return sch


############################ SCHEDULE DATE INOUT #################################

############################## DATEINOUT INOUT ###################################

class InoutDateInOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = InOut
        fields = ('id',
                  'UserIDInOut',
                  'EmployerIDInOut',
                  # 'CompanyIDInOut',
                  'ScheduleIDInOut',
                  'InOutName',
                  'TimeIn',
                  'TimeOut',
                  'DateInOutIDInOut',
                  )
        read_only_fields = ('id',
                            'UserIDInOut',
                            'EmployerIDInOut',
                            # 'CompanyIDInOut',
                            # 'ScheduleIDInOut',
                            # 'DateInOutIDInOut'
                            )


############################## DATEINOUT INOUT ###################################

####################### Schedule CheckInOut ##############################

class ScheduleViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
        # fields = ('id',
        #           'UserIDShedule',
        #           'EmployerIDSchedule',
        #           'CompanyIDSchedule',
        #           'SchName',
        #           'DateStartWork',
        #           'DateEndWork',
        #           'DateWork',
        #           'IsWeekend',
        #           'IsAbsentSat',
        #           'IsAbsentSun',
        #           'IsAbsentHol',
        #           'CycleMode',
        #
        #           )
        # read_only_fields = ('id',
        # 'UserIDShedule',
        # 'EmployerIDSchedule',
        # 'CompanyIDSchedule',
        # 'DateWork',
        # )


class LocationViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        # fields = (
        #     'id',
        #     'GPS_EMP_LAT',
        #     'GPS_EMP_LONG',
        #     'UserIDLocation',
        #     'checkinout',
        #     'TimeL'
        # )


####################### Schedule CheckInOut ##############################


# ############################################## BANK #########################################################
#
# class EmployerUserBankViewSetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserBank
#         fields = ('id', 'UserIDUserBank', 'EmployerIDUserBank', 'AddressIDUserBank', 'idTK', 'ownTK', 'BankName',
#                   'BranchName', 'DateCreate', 'DateAuth')
#         read_only_fields = ('UserIDUserBank', 'EmployerIDUserBank',)
#
# class EmployerUserBankDetailSerializer(serializers.ModelSerializer):
#     employerbank = EmployerUserBankViewSetSerializer(many=True)
#
#     class Meta:
#         model = Employer
#         fields = ('id', 'UserNoted', 'employerbank',)
#
#     def update(self, instance, validated_data):
#         employerbank = validated_data.pop('employerbank')
#         instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
#         instance.save()
#         for ebank in employerbank:
#             if 'id' in ebank.keys():
#                 if UserBank.objects.filter(id=ebank['id']).exists():
#                     e = UserBank.objects.get(id=ebank['id'])
#                     e.AddressIDUserBank = ebank.get('AddressIDUserBank', e.AddressIDUserBank)
#                     e.idTK = ebank.get('idTK', e.idTK)
#                     e.ownTK = ebank.get('ownTK', e.ownTK)
#                     e.BankName = ebank.get('BankName', e.idTK)
#                     e.BranchName = ebank.get('BranchName', e.BranchName)
#                     e.DateCreate = ebank.get('DateCreate', e.DateCreate)
#                     e.DateAuth = ebank.get('DateAuth', e.DateAuth)
#                     e.save()
#                 else:
#                     continue
#             else:
#                 UserBank.objects.create(EmployerIDUserBank=instance, UserIDUserBank=instance.UserIDBank, **ebank)
#         return instance
#
#
# ############################################## COMPANY #########################################################
# # **************************** Company - Employer ****************************************
#
#
# # ***************************** Detail - Employer - Company ****************************
# class EmployerCompanyDetailSerializer(serializers.ModelSerializer):
#     employercompany = EmployerCompanySerializer(many=True)
#
#     class Meta:
#         model = Employer
#         fields = ('id', 'UserNoted', 'employercompany',)
#
#     def update(self, instance, validated_data):
#         employercompany = validated_data.pop('employercompany')
#         instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
#         instance.save()
#         for ecom in employercompany:
#             if 'id' in ecom.keys():
#                 if Company.objects.filter(id=ecom['id']).exists():
#                     c = Company.objects.get(id=ecom['id'])
#                     c.AddressIDCompany = ecom.get('AddressIDCompany', c.AddressIDCompany)
#                     c.ComTel = ecom.get('ComTel', c.ComTel)
#                     c.Logo = ecom.get('Logo', c.Logo)
#                     c.CompCode = ecom.get('CompCode', c.CompCode)
#                     c.Status = ecom.get('Status', c.Status)
#                     c.ComAddress = ecom.get('ComAddress', c.ComAddress)
#                     c.save()
#                 else:
#                     continue
#             else:
#                 Company.objects.create(EmployerIDCompany=instance, UserIDCompany=instance.UserIDCompany, **ecom)
#         return instance
#
#
# #  ############################################## ADDRESS #########################################################
# # ************************************** Employer - Address *************************
# class EmployerAdressViewSetSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Address
#         fields = (
#             'Place', 'Ward', 'District', 'Province', 'Nation', 'AddressFull', 'UserIDAddress',
#             'EmployerIDAddress')
#         read_only_fields = ('id', 'UserIDAddress', 'EmployerIDAddress')
#
#
# # ***************************** Detail - Employer - Address ****************************
# class EmployerAddressDetailSerializer(serializers.ModelSerializer):
#     employeraddress = EmployerAdressViewSetSerializer(many=True)
#
#     class Meta:
#         model = Employer
#         fields = ('id', 'UserNoted', 'employeraddress',)
#
#     def update(self, instance, validated_data):
#         employeraddress = validated_data.pop('employeraddress')
#         instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
#         instance.save()
#         for eradd in employeraddress:
#             if 'id' in eradd.keys():
#                 if Address.objects.filter(id=eradd['id']).exists():
#                     a = Address.objects.get(id=eradd['id'])
#                     a.Place = eradd.get('Place', a.Place)
#                     a.Ward = eradd.get('Ward', a.Ward)
#                     a.District = eradd.get('District', a.District)
#                     a.Province = eradd.get('Province', a.Province)
#                     a.Nation = eradd.get('Nation', a.Nation)
#                     a.save()
#                 else:
#                     continue
#             else:
#                 Address.objects.create(EmployerIDAddress=instance, UserIDAddress=instance.UserIDAddress, **eradd)
#         return instance
#
#
# #  ############################################## JOB #########################################################
# ************************************************* Employer Full JOB *********************************************

############################ EMPLOYER JOB ###################################

# # ***************************************** Detail - Employer - JOB ********************************************
# class EmployerJobDetailSerializer(serializers.ModelSerializer):
#     employerjobs = EmployerJobsViewSetSerializer(many=True)
#
#     class Meta:
#         model = Employer
#         fields = ('id', 'UserNoted', 'employerjobs',)
#
#     def update(self, instance, validated_data):
#         employerjobs = validated_data.pop('employerjobs')
#         instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
#         instance.save()
#         for erjob in employerjobs:
#             if 'id' in erjob.keys():
#                 if Jobs.objects.filter(id=erjob['id']).exists():
#                     j = Jobs.objects.get(id=erjob['id'])
#                     j.CompanyIDJob = erjob.get('CompanyIDJob', j.CompanyIDJob)
#                     j.AddressIDJob = erjob.get('AddressIDJob', j.AddressIDJob)
#                     j.JobClassificationIDJob = erjob.get('JobClassificationIDJob', j.JobClassificationIDJob)
#                     j.ScheduleIDJob = erjob.get('ScheduleIDJob', j.ScheduleIDJob)
#                     j.DegreeIDJob = erjob.get('DegreeIDJob', j.DegreeIDJob)
#                     j.JobTitle = erjob.get('JobTitle', j.JobTitle)
#                     j.JobType = erjob.get('JobType', j.JobType)
#                     j.JobRole = erjob.get('JobRole', j.JobRole)
#                     j.ImageJob = erjob.get('ImageJob', j.ImageJob)
#                     j.JobRequirements = erjob.get('JobRequirements', j.JobRequirements)
#                     j.JobExperience = erjob.get('JobExperience', j.JobExperience)
#                     j.JobDescription = erjob.get('JobDescription', j.JobDescription)
#                     j.MinSalary = erjob.get('MinSalary', j.MinSalary)
#                     j.MaxSalary = erjob.get('MaxSalary', j.MaxSalary)
#                     j.DateTime_create = erjob.get('DateTime_create', j.DateTime_create)
#
#                     j.save()
#                 else:
#                     continue
#             else:
#                 Jobs.objects.create(EmployerIDJob=instance, UserIDJob=instance.UserIDJobs, **erjob)
#         return instance
#
#
# # ************************************************* Employer Full Schedule  *******************************************
# class EmployerScheduleViewSetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Schedule
#         fields = ('id', 'UserIDSchedule', 'EmployerIDSchedule', 'CompanyIDSchedule', 'SchID',
#                   'SchName', 'CycleMode', 'IsWeekend', 'IsAbsentSat', 'IsAbsentSun', 'IsAbsentHol', 'IsCountHol',
#                   'IsDateOfOutTime', 'isSchedule')
#
#         read_only_fields = ('id', 'UserIDSchedule', 'EmployerIDSchedule')
#
#
# # ***************************************** Detail - Employer - Schedule ********************************************
# class EmployerScheduleDetailSerializer(serializers.ModelSerializer):
#     employerschedule = EmployerScheduleViewSetSerializer(many=True)
#
#     class Meta:
#         model = Employer
#         fields = ('id', 'UserNoted', 'employerjobs',)
#
#     def update(self, instance, validated_data):
#         employerschedule = validated_data.pop('employerschedule')
#         instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
#         instance.save()
#         for eschedule in employerschedule:
#             if 'id' in eschedule.keys():
#                 if Schedule.objects.filter(id=eschedule['id']).exists():
#                     j = Schedule.objects.get(id=eschedule['id'])
#                     j.CompanyIDSchedule = eschedule.get('CompanyIDSchedule', j.CompanyIDSchedule)
#                     j.SchID = eschedule.get('SchID', j.SchID)
#                     j.SchName = eschedule.get('SchName', j.SchName)
#                     j.IsWeekend = eschedule.get('IsWeekend', j.IsWeekend)
#                     j.IsAbsentSat = eschedule.get('IsAbsentSat', j.IsAbsentSat)
#                     j.IsAbsentSun = eschedule.get('IsAbsentSun', j.IsAbsentSun)
#                     j.IsAbsentHol = eschedule.get('IsAbsentHol', j.IsAbsentHol)
#                     j.IsCountHol = eschedule.get('IsCountHol', j.IsCountHol)
#                     j.CycleMode = eschedule.get('CycleMode', j.CycleMode)
#                     j.isSchedule = eschedule.get('isSchedule', j.isSchedule)
#                     j.save()
#                 else:
#                     continue
#             else:
#                 Schedule.objects.create(EmlpoyerIDSchedule=instance, UserIDSchedule=instance.UserIDSchedule,
#                                         **eschedule)
#         return instance
#
#
# # ************************************************* Employer Full InOut  *********************************************
# class EmployerInOutViewSetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InOut
#         fields = ('id', 'UserIDInOut', 'EmployerIDInOut', 'ScheduleIDInOut',
#                   'TimeIn', 'TimeOut')
#
#         read_only_fields = ('id', 'UserIDInOut', 'EmployerIDInOut')
#
#
# class EmployerInOutDetailSerializer(serializers.ModelSerializer):
#     employerinout = EmployerInOutViewSetSerializer(many=True)
#
#     class Meta:
#         model = Employer
#         fields = ('id', 'UserNoted', 'employerinout',)
#
#     def update(self, instance, validated_data):
#         employerinout = validated_data.pop('employerinout')
#         instance.UserNoted = validated_data.get('UserNoted', instance.UserNoted)
#         instance.save()
#         for esinout in employerinout:
#             if 'id' in esinout.keys():
#                 if Schedule.objects.filter(id=esinout['id']).exists():
#                     j = Schedule.objects.get(id=esinout['id'])
#                     j.ScheduleIDInOut = esinout.get('ScheduleIDInOut', j.ScheduleIDInOut)
#                     j.TimeIn = esinout.get('TimeIn', j.TimeIn)
#                     j.TimeOut = esinout.get('TimeOut', j.TimeOut)
#                     j.save()
#                 else:
#                     continue
#             else:
#                 Schedule.objects.create(EmployerIDInOut=instance, UserIDInOut=instance.UserIDInOut,
#                                         **esinout)
#         return instance


###################### SCHEDULE DATE INOUT DATE INOUT ###########################

############################## Serializer INOUT ##################################

class InOutNested(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = InOut
        fields = ['id',
                  'UserIDInOut',
                  'EmployerIDInOut',
                  'InOutName',
                  'TimeIn',
                  'TimeOut',
                  'DateInOutIDInOut',
                  'ScheduleIDInOut',

                  ]
        read_only_fields = ['id',
                            'UserIDInOut',
                            'EmployerIDInOut',
                            'ScheduleIDInOut',
                            'DateInOutIDInOut',
                            ]


############################## Serializer INOUT ##################################

############################ Serializer DateInOut ################################

class DateInOutNested(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = DateInOut
        fields = ('id',
                  'UserIDDateInOut',
                  'EmployerIDDateInOut',
                  'ScheduleIDDateInOut',
                  'DateIDInOut',

                  )
        read_only_fields = ('id',
                            'UserIDDateInOut',
                            'EmployerIDDateInOut',
                            'ScheduleIDDateInOut',
                            )


############################ Serializer DateInOut ################################

############################# Serializer Schedule ################################

class ScheduleDateInOutNested(serializers.ModelSerializer):
    dateinoutschedule = DateInOutNested(many=True)
    inoutidschedule = InOutNested(many=True)

    class Meta:
        model = Schedule
        fields = ('id',
                  'UserIDShedule',
                  'EmployerIDSchedule',
                  'SchName',
                  'DateStartWork',
                  'DateEndWork',
                  'DateWork',
                  'IsWeekend',
                  'IsAbsentSat',
                  'IsAbsentSun',
                  'IsAbsentHol',
                  'CycleMode',
                  'dateinoutschedule',
                  'inoutidschedule',
                  )
        read_only_fields = ('id',
                            'UserIDShedule',
                            'EmployerIDSchedule',
                            'DateWork',
                            )

    def create(self, validated_data):
        dateinoutschedule = validated_data.pop('dateinoutschedule')
        inoutidschedule = validated_data.pop('inoutidschedule')
        schedule = Schedule.objects.create(**validated_data)
        scheduleid = Employer.objects.get(UserIDEmployer=schedule.UserIDShedule)

        for dateinout in dateinoutschedule:
            t = DateInOut.objects.create(**dateinout,
                                         UserIDDateInOut=schedule.UserIDShedule,
                                         EmployerIDDateInOut=scheduleid,
                                         ScheduleIDDateInOut=schedule,
                                         )

        for inout in inoutidschedule:
            io = InOut.objects.create(**inout,
                                      EmployerIDInOut=scheduleid,
                                      UserIDInOut=schedule.UserIDShedule,
                                      ScheduleIDInOut=schedule,
                                      # DateInOutIDInOut= list(x)
                                      )
            io.DateInOutIDInOut.set(t)

        return schedule

    # def update(self, instance, validated_data):
    #     inoutidschedule = validated_data.pop('inoutidschedule')
    #     instance.SchName = validated_data.get('SchName', instance.SchName)
    #     instance.DateStartWork = validated_data.get('DateStartWork', instance.DateStartWork)
    #     instance.DateEndWork = validated_data.get('DateEndWork', instance.DateEndWork)
    #     instance.IsWeekend = validated_data.get('IsWeekend', instance.IsWeekend)
    #     instance.IsAbsentSat = validated_data.get('IsAbsentSat', instance.IsAbsentSat)
    #     instance.CycleMode = validated_data.get('CycleMode', instance.CycleMode)
    #     instance.save()
    #     keep_inoutidschedule = []
    #     existing_ids = [c.id for c in instance.inoutidschedule.all()]
    #     for inout in inoutidschedule:
    #         if 'id' in inout.keys():
    #             if InOut.objects.filter(id=inout['id']).exists():
    #                 c = InOut.objects.get(id=inout['id'])
    #                 c.InOutName = inout.get('InOutName', c.InOutName)
    #                 c.TimeIn = inout.get('TimeIn', c.TimeIn)
    #                 c.TimeOut = inout.get('TimeOut', c.TimeOut)
    #                 c.save()
    #                 keep_inoutidschedule.append(c.id)
    #             else:
    #                 continue
    #         else:
    #             scheduleidinout = Employer.objects.get(UserIDEmployer=instance.UserIDShedule)
    #             c = InOut.objects.create(**inout,
    #                                      EmployerIDInOut=scheduleidinout,
    #                                      UserIDInOut=c.UserIDInOut,
    #                                      ScheduleIDInOut=instance
    #                                      )
    #             keep_inoutidschedule.append(c.id)
    #
    #     for inout in instance.inoutidschedule.all():
    #         if inout.id not in keep_inoutidschedule:
    #             inout.delete()
    #     return instance


####################### UPDATE SCHEDULE JOB DATE INOUT ###########################


class ScheduleDateInOutNestedList(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id',
                  'UserIDShedule',
                  'EmployerIDSchedule',
                  # 'CompanyIDSchedule',
                  'SchName',
                  'DateStartWork',
                  'DateEndWork',
                  'DateWork',
                  'IsWeekend',
                  'IsAbsentSat',
                  'IsAbsentSun',
                  'IsAbsentHol',
                  'CycleMode',
                  )
        read_only_fields = ('id',
                            'UserIDShedule',
                            'EmployerIDSchedule',
                            # 'CompanyIDSchedule',
                            'DateWork',
                            )


####################### UPDATE SCHEDULE JOB DATE INOUT ###########################

####################### UPDATE SCHEDULE JOB DATE INOUT ###########################

########################## SCHEDULE JOB DATE INOUT ###############################


############################ SCHEDULE DATE INOUT #################################

# class DateInOutSingleSerialzier(serializers.ModelSerializer):
#     class Meta:
#         model = DateInOut
#         fields = ('id',
#                   'UserIDDateInOut',
#                   'EmployerIDDateInOut',
#                   'CompanyIDDateInOut',
#                   'ScheduleIDDateInOut',
#                   'DateIDInOut')
#         read_only_fields = ('id',
#                             'UserIDDateInOut',
#                             'EmployerIDDateInOut',
#                             'CompanyIDDateInOut',
#                             'ScheduleIDDateInOut',
#                             )
#
#
# class ScheduleDateTimeSerializer(serializers.ModelSerializer):
#     dateinoutschedule = DateInOutSingleSerialzier(many=True)
#
#     class Meta:
#         model = Schedule
#         fields = ('id',
#                   'UserIDShedule',
#                   'EmployerIDSchedule',
#                   'CompanyIDSchedule',
#                   'SchName',
#                   'DateStartWork',
#                   'DateEndWork',
#                   'DateWork',
#                   'IsWeekend',
#                   'IsAbsentSat',
#                   'IsAbsentSun',
#                   'IsAbsentHol',
#                   'CycleMode',
#                   'dateinoutschedule',
#                   )
#         read_only_fields = ('id',
#                             'UserIDShedule',
#                             'EmployerIDSchedule',
#                             # 'CompanyIDSchedule',
#                             'DateWork',
#                             )
#
#     def create(self, validated_data):
#         dateinout_data = validated_data.pop('dateinoutschedule')
#         sch = Schedule.objects.create(**validated_data)
#         for dateinout in dateinout_data:
#             DateInOut.objects.create(**dateinout, UserIDDateInOut=sch.UserIDShedule,
#                                      EmployerIDDateInOut=sch.EmployerIDSchedule,
#                                      ScheduleIDDateInOut=sch,
#                                      CompanyIDDateInOut=sch.CompanyIDSchedule,
#                                      # CompanyIDSchedule = sch.CompanyIDSchedule,
#                                      )
#         return sch


###################### SCHEDULE DATE INOUT DATE INOUT ###########################


# ########################### SCHEDULE DATE INOUT #################################

# ############################# Serializer INOUT ##################################

class InoutSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = InOut
        fields = ['id',
                  'UserIDInOut',
                  'EmployerIDInOut',
                  # 'CompanyIDInOut',
                  'InOutName',
                  'TimeIn',
                  'TimeOut',
                  'DateInOutIDInOutSchedule',
                  'ScheduleIDInOut',

                  ]
        read_only_fields = ['id',
                            'UserIDInOut',
                            'EmployerIDInOut',
                            'DateInOutIDInOutSchedule',
                            'ScheduleIDInOut',
                            # 'CompanyIDInOut'
                            ]


# ############################# Serializer INOUT ##################################

# ########################### Serializer DateInOut ################################

class DateInOutSerialzier(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    inoutdateinout = InoutSerializer(many=True, required=False)

    class Meta:
        model = DateInOut
        fields = ('id',
                  'UserIDDateInOut',
                  'EmployerIDDateInOut',
                  # 'CompanyIDDateInOut',
                  'ScheduleIDDateInOut',
                  'DateIDInOut',
                  'inoutdateinout')
        read_only_fields = ('id',
                            'UserIDDateInOut',
                            'EmployerIDDateInOut',
                            # 'CompanyIDDateInOut',
                            'ScheduleIDDateInOut',)


# ########################### Serializer DateInOut ################################

# ############################ Serializer Schedule ################################

class ScheduleDateInOutSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    dateinoutschedule = DateInOutSerialzier(many=True, required=False)

    class Meta:
        model = Schedule
        fields = ('id',
                  'UserIDShedule',
                  'EmployerIDSchedule',
                  # 'CompanyIDSchedule',
                  'SchName',
                  'DateStartWork',
                  'DateEndWork',
                  'DateWork',
                  'IsWeekend',
                  'IsAbsentSat',
                  'IsAbsentSun',
                  'IsAbsentHol',
                  'CycleMode',
                  'dateinoutschedule',
                  )
        read_only_fields = ('id',
                            'UserIDShedule',
                            'EmployerIDSchedule',
                            # 'CompanyIDSchedule',
                            'DateWork',
                            )

    def create(self, validated_data):
        dateinout_data = validated_data.pop('dateinoutschedule')
        sch = Schedule.objects.create(**validated_data)
        for dateinout in dateinout_data:
            inout_data = dateinout.pop('inoutdateinout')
            date = DateInOut.objects.create(UserIDDateInOut=sch.UserIDShedule,
                                            EmployerIDDateInOut=sch.EmployerIDSchedule,
                                            ScheduleIDDateInOut=sch, **dateinout)
            # CompanyIDDateInOut=sch.CompanyIDSchedule,)
            for inout in inout_data:
                InOut.objects.create(UserIDInOut=date.UserIDDateInOut,
                                     EmployerIDInOut=date.EmployerIDDateInOut,
                                     DateInOutIDInOutSchedule=date,
                                     ScheduleIDInOut=date.ScheduleIDDateInOut, **inout)
        return sch

# ###################################### Update Schedule ####################################
    def update(self, instance, validated_data):
        dateinout_data = validated_data.pop('dateinoutschedule')  # Gọi Serialzer DateInOut
        instance.SchName = validated_data.get('SchName', instance.SchName)
        instance.DateStartWork = validated_data.get('DateStartWork', instance.DateStartWork)
        instance.DateEndWork = validated_data.get('DateEndWork', instance.DateEndWork)
        instance.IsWeekend = validated_data.get('IsWeekend', instance.IsWeekend)
        instance.IsAbsentSat = validated_data.get('IsAbsentSat', instance.IsAbsentSat)
        instance.CycleMode = validated_data.get('CycleMode', instance.CycleMode)
        instance.save()

# ############################## Update DateInOut ###########################################
        keep_dateinoutschedule = []
        existing_ids = [c.id for c in instance.inoutidschedule.all()]
        for dateinout in dateinout_data:
            inoutdateinout = dateinout.pop('inoutdateinout')  # Gọi Serialzer InOut
            keep_inoutdateinout = []
            existing_ids = [i.id for i in instance.inoutidschedule.all()]

# ########################## Kiểm tra nếu tồn tại thì cập nhật ##############################
            if 'id' in dateinout.keys():
                if DateInOut.objects.filter(id=dateinout['id']).exists():
                    c = DateInOut.objects.get(id=dateinout['id'])
                    c.DateIDInOut = dateinout.get('DateIDInOut', c.DateIDInOut)
                    c.save()
                    keep_dateinoutschedule.append(c.id)
                else:
                    continue

# ################################ Không tồn tại thì tạo mới #################################
            else:
                c = DateInOut.objects.create(
                    EmployerIDDateInOut=instance.EmployerIDSchedule,
                    UserIDDateInOut=instance.UserIDShedule,
                    ScheduleIDDateInOut=instance, **dateinout)
                keep_dateinoutschedule.append(c.id)  # Giữ DateInOut lại để kiểm tra

# ###################################### Update InOut #########################################
# ############################## Kiểm tra tồn tại thì cập nhật ################################
            for inout in inoutdateinout:
                if 'id' in inout.keys():
                    if InOut.objects.filter(id=inout['id']).exists():
                        i = InOut.objects.get(id=inout['id'])
                        i.InOutName = inout.get('InOutName', i.InOutName)
                        i.TimeIn = inout.get('TimeIn', i.TimeIn)
                        i.TimeOut = inout.get('TimeOut', i.TimeOut)
                        i.save()
                        keep_inoutdateinout.append(i.id)
                    else:
                        continue

# #################################### Không tồn tại thì tạo mới ###############################
                else:
                    i = InOut.objects.create(EmployerIDInOut=instance.EmployerIDSchedule,
                                             UserIDInOut=instance.UserIDShedule,
                                             ScheduleIDInOut=instance,
                                             DateInOutIDInOutSchedule=c,  # c là DateInOut (c.save ở trên)
                                             **inout)
                    keep_inoutdateinout.append(i.id)  # Giữ InOut lại kiểm tra

# ################################### InOut không tồn tại thì xóa ###############################
            for inout in c.inoutdateinout.all():
                if inout.id not in keep_inoutdateinout:
                    inout.delete()

# ###################################### Date InOut ko tồn tại thì xóa ##########################
        for dateinout in instance.dateinoutschedule.all():
            if dateinout.id not in keep_dateinoutschedule:
                dateinout.delete()

        return instance

# ############################ Serializer Schedule ################################
# ########################### SCHEDULE DATE INOUT #################################
