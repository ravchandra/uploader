from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings

import datetime

def content_file_name(instance, filename):
    name, ext = filename.split('.')
    filename = "%s_%s.%s" % (name, datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), ext)
    return filename

class DropZoneModel(models.Model):
    #user = models.ForeignKey(User, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    file = models.FileField(upload_to=content_file_name)
