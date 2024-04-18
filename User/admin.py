from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(TeacherDetails)
admin.site.register(TeacherDocument)
admin.site.register(UserProfile)