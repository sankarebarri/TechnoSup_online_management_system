from django.contrib import admin

from .models import (CustomUser, Student,
                    Filiere, Promotion,
                    Profile, Module,
                    StudentRecord, Staff,
                    Message, Contact
)


admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Profile)
admin.site.register(Module)
admin.site.register(StudentRecord)
admin.site.register(Staff)
admin.site.register(Filiere)
admin.site.register(Promotion)
admin.site.register(Message)
admin.site.register(Contact)
