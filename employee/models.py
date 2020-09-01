
from django.db import models
from django.contrib.auth import get_user_model

#from connectdata.models import UserBank
#from connectdata.models import UserBank

User = get_user_model()
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

################################ Employee User #####################################

