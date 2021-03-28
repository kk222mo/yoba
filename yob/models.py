from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=256)
    tags = models.CharField(max_length=256)
    lesson_time = models.CharField(max_length=512, default='')

    is_private = models.BooleanField(default=False)
    token = models.CharField(max_length=128, default='')
    description = models.TextField(default='', blank=True)
    teacher = models.ForeignKey(to="Pupil", on_delete=models.CASCADE)


class Pupil(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    is_teacher = models.BooleanField()
    courses = models.ManyToManyField(to=Course, blank=True)


class Review(models.Model):
    pupil = models.ForeignKey(to=Pupil, on_delete=models.DO_NOTHING)
    course_token = models.CharField(max_length=128)
    text = models.CharField(max_length=256)


class Rate(models.Model):
    rate = models.IntegerField()
    pupil = models.ForeignKey(Pupil, related_name='pupil', on_delete=models.CASCADE)
    course_token = models.CharField(max_length=128, default='')