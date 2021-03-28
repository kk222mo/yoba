"""yoba URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from yob.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/login/', loginView),
    path('account/register/', registerView),
    path('account/logout/', logoutView),
    path('courses/create/', createCourse),
    path('courses/getUserCourses/', getMyCourses),
    path('courses/getAll/', getAllCourses),
    path('courses/join/', joinCourse),
    path('reviews/post/', postReview),
    path('reviews/get/', getReviews),
    path('', index),
    path('mycourses/', my_courses),
    re_path(r'^course/(?P<token>[0-9a-zA-Z]+)/$', courseInfo),


]
