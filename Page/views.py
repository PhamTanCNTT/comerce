from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import response, decorators, permissions, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


# Create your views here.

def about_views(request):
    return render(request, "about.html")

def adposts_views(request):
    return render(request, "ad-posts.html")

def adposts2_views(request):
    return render(request, "ad-posts2.html")

def advancedsearch_views(request):
    return render(request, "advanced-search.html")

def blogdetails_views(request):
    return render(request, "blog-details.html")

def blogdetailscenter_views(request):
    return render(request, "blog-details-center.html")

def blogdetailsright_views(request):
    return render(request, "blog-details-right.html")

def bloggrid_views(request):
    return render(request, "blog-grid.html")

def bloggridcenter_views(request):
    return render(request, "blog-grid-center.html")

def bloggridright_views(request):
    return render(request, "blog-details-right.html")

def bloglist_views(request):
    return render(request, "blog-list.html")

def bloglistcenter_views(request):
    return render(request, "blog-list-center.html")

def bloglistright_views(request):
    return render(request, "blog-list-right.html")

def candidatelisting_views(request):
    return render(request, "candidate-listing.html")

def candidatelisting2_views(request):
    return render(request, "candidate-listing2.html")

def candidateprofile_views(request):
    return render(request, "candidate-profile.html")

def categories_views(request):
    return render(request, "categories.html")

def companydetails_views(request):
    return render(request, "company-details.html")

def companylist_views(request):
    return render(request, "company-list.html")

def companylist2_views(request):
    return render(request, "company-list2.html")

def companylistmap_views(request):
    return render(request, "company-list-map.html")

def companylistmap2_views(request):
    return render(request, "company-list-map2.html")

def companylistmap3_views(request):
    return render(request, "company-list-map3.html")

def companyreviews_views(request):
    return render(request, "company-reviews.html")

def contact_views(request):
    return render(request, "contact.html")

def createresume_views(request):
    return render(request, "employee/create_resume_viet.html")

def info_employee(request):
    return render(request, "Page/info_employee.html")

def updateresume_views(request,id):
    context = {"ID_CurriculumVitae":id}
    return render(request, "employee/create_resume_viet.html", context)

def faq_views(request):
    return render(request, "faq.html")

def footerstyle1_views(request):
    return render(request, "footer-style1.html")

def footerstyle2_views(request):
    return render(request, "footer-style2.html")

def footerstyle3_views(request):
    return render(request, "footer-style3.html")

def footerstyle4_views(request):
    return render(request, "footer-style4.html")

def forgot_views(request):
    return render(request, "forgot.html")

def headerstyle1_views(request):
    return render(request, "header-style1.html")

def headerstyle2_views(request):
    return render(request, "header-style2.html")

def headerstyle3_views(request):
    return render(request, "header-style3.html")

def headerstyle4_views(request):
    return render(request, "header-style4.html")

def index_views(request):
    return render(request, "Page/index.html")

def index2_views(request):
    return render(request, "index2.html")

def index3_views(request):
    return render(request, "index3.html")

def index4_views(request):
    return render(request, "index4.html")

def index5_views(request):
    return render(request, "index5.html")

def index6_views(request):
    return render(request, "index6.html")

def index7_views(request):
    return render(request, "index7.html")

def inovice_views(request):
    return render(request, "inovice.html")

def intropage_views(request):
    return render(request, "intro-page.html")

def jobs_views(request):
    return render(request, "employer/create_job.html")

def jobslist_views(request):
    return render(request, "jobs-list.html")

def jobslistmap_views(request):
    return render(request, "jobs-list-map.html")

def jobslistmap2_views(request):
    return render(request, "jobs-list-map2.html")

def jobslistmap3_views(request):
    return render(request, "jobs-list-map3.html")

def jobslistright_views(request):
    return render(request, "jobs-list-right.html")

def jobsright_views(request):
    return render(request, "jobs-right.html")

def lockscreen_views(request):
    return render(request, "lockscreen.html")

def login_views(request):
    return render(request, "login.html")

def login2_views(request):
    return render(request, "login-2.html")

def manged_views(request):
    return render(request, "manged.html")

def myjobs_views(request):
    return render(request, "my-jobs.html")

def mydash_views(request):
    return render(request, "Page/mydash2.html")

# def mydash_views2(request):
#     return render(request, "m")

def myfavorite_views(request):
    return render(request, "myfavorite.html")

def myjobs_views(request):
    return render(request, "employer/list_jobs.html")

def updatejob_views(request,id):
    context = {"ID_job":id}
    return render(request, "employer/create_job.html", context)

def mycv_views(request):
    return render(request, "employee/list_CV.html")

def orders_views(request):
    return render(request, "orders.html")

def payments_views(request):
    return render(request, "payments.html")

def popuplogin_views(request):
    return render(request, "popup-login.html")

def pricing_views(request):
    return render(request, "pricing.html")

def profile_views(request):
    return render(request, "profile.html")

def register_views(request):
    return render(request, "register.html")

def settings_views(request):
    return render(request, "settings.html")

def tips_views(request):
    return render(request, "tips.html")

def typography_views(request):
    return render(request, "typography.html")

def underconstrustion_views(request):
    return render(request, "underconstruction.html")

def userprofile_views(request):
    return render(request, "userprofile.html")

def usersall_views(request):
    return render(request, "usersall.html")

def widgets_views(request):
    return render(request, "widgets.html")

def widgetscarousel_views(request):
    return render(request, "widgets-carousel.html")

def widgetsverticalscroll_views(request):
    return render(request, "widgets-verticalscroll.html")

def error_400_views(request):
    return render(request, "error_400.html")

def error_404_views(request):
    return render(request, "error_404.html")

def error_404inline_views(request):
    return render(request, "error_404-inline.html")

def error_500_views(request):
    return render(request, "error_500.html")

# class UserUploadPhotoView(APIView):
#     serializer_class = UserUploadPhotoSerializer
#     parser_classes = (FormParser, MultiPartParser)
#     def post(self, request):
#         print(self.request.user.id)
#         print(request.FILES)
#         up_file = request.FILES['Photo']
#         destination = open('media/' + up_file.name, 'wb+')
#         for chunk in up_file.chunks():
#             destination.write(chunk)
#         destination.close()  # File should be closed only after all chuns are added
#         urlfilepath = "http://gojoco.com:8000/media/" +  up_file.name
#         UserPhotoVerify.objects.get_or_create(UserID=self.request.user.id,
#                                  UserName=self.request.user,
#                                  Notes=request.data["Notes"],
#                                  UserPhoto=urlfilepath,
#                                  Status="Waitting")        # ...
#         return Response({"error" : {"code": 0,"message" : "Upload file success","urlfilepath" : urlfilepath} })
#

# ----------------------------
def base_views(request):
    return render(request, "base.html")

def baseadmin_views(request):
    return render(request, "base_admin2.html")


def registeruser(request):
    return render(request, "registeruser.html")

def detail_resume(request, id):
    context = {"ID_resume": id}
    return render(request, "employee/detail_resume.html", context)

def detail_job(request, id):
    context = {"ID_job": id}
    return render(request, "employer/list_job_categories.html", context)

def jobs(request, id):
    context = {"ID_job": id}
    return render(request, "employer/jobs.html", context)

def timekeeping(request):
    return render(request, "employee/Timekeeping.html")

def getip(request):
    return render(request, "employer/getip.html")

def listapply(request,id):
    context = {"id_apply": id}
    return render(request, "employer/list_apply.html",context)

def viewdetailjobapply(request,id):
    context = {"id_detail_job": id}
    return render(request, "employer/view_detail_jobapply.html",context)

def createcalendar2(request):
    return render(request, "employer/calendar2.html")

def listschedule(request):
    return render(request, "employer/list_schedule.html")

def editschedule(request,id):
    context = {"id_detail_sche": id}
    return render(request, "employer/calendar.html",context)

def listinout2(request,id):
    context = {"id_detail_sche": id}
    return render(request, "employer/list_in_out2.html",context)

def listinout3(request):
    return render(request, "employer/list_in_out2.html")

def calendar2(request):
    return render(request, "Page/calendar2.html")