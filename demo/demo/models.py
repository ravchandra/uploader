from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings

class DropZoneModel(models.Model):
    #user = models.ForeignKey(User, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    file = models.FileField(upload_to='')
