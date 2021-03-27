from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=256)
    tags = models.CharField(max_length=256)
    lesson_time = models.CharField(max_length=512, default='')
    teacher = models.ForeignKey(to="Pupil", on_delete=models.CASCADE)


class Pupil(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    is_teacher = models.BooleanField()
    courses = models.ManyToManyField(to=Course, blank=True)
