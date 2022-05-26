from django.contrib import admin
from .models import UserFiles


# Register your models here.
@admin.register(UserFiles)
class UserFilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'left_file', 'right_file']
