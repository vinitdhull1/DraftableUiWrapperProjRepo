from operator import mod
from django.db import models

# Create your models here.

def input_files_location(instance, filename):
    return "pdf_files/{file}".format(file=filename)

class UserFiles(models.Model):
    left_file = models.FileField(upload_to=input_files_location, verbose_name="Older version File(Left)")
    right_file = models.FileField(upload_to=input_files_location, verbose_name="Older version File(Right)")
