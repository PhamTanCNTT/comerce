import os

from django.core import validators
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"users/{instance.pk}//{instance.UserProfile}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"

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

