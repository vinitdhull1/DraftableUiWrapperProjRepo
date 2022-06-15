from django.contrib import admin
from .models import UserFiles, Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
@admin.register(UserFiles)
class UserFilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'left_file', 'right_file']

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"

class CustomizedUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

