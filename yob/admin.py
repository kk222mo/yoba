from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from yob.models import Pupil, Course, Review

admin.site.register(Pupil)
admin.site.register(Course)
admin.site.register(Review)