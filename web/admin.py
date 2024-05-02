from django.contrib import admin
from .models import Birthplace, Job, PersonalData, Workplace

# Register your models here.

admin.site.register(Birthplace)
admin.site.register(Job)
admin.site.register(PersonalData)
admin.site.register(Workplace)