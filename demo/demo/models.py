from django.db import models

class DropZoneModel(models.Model):
    file = models.FileField(upload_to='files/%Y/%m/%d')
