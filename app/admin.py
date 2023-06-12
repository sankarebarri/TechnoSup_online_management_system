from django.contrib import admin
from .models import CustomUser, Course, SessionYear, Student, Staff, StaffNotification
from django.contrib.auth.admin import UserAdmin

class UserModel(UserAdmin):
    list_display = ['username', 'user_type']

admin.site.register(CustomUser, UserModel)
admin.site.register(Course)
admin.site.register(SessionYear)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(StaffNotification)