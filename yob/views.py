from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.views import View

from yob.models import Pupil, Course


@csrf_exempt
def registerView(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        passw = request.POST.get('pass')
        try:
            User.objects.get(username=email)
            return HttpResponse(request, status=403)
        except:
            pass
        if name != '' and email != '' and passw != '':
            user = User.objects.create_user(email, email=email, password=passw)
            user.save()
            pupil = Pupil()
            pupil.user = user
            pupil.is_teacher = False
            pupil.name = name
            pupil.save()
            return HttpResponse(request, status=200)
        return HttpResponse(request, status=403)
    elif request.method == "GET":
        return render(request, "register.html")


@csrf_exempt
def loginView(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    elif request.method == "POST":
        email = request.POST.get('email')
        passw = request.POST.get('pass')
        user = authenticate(username=email, password=passw)
        if user is not None:
            login(request, user)
            return redirect('/')
        return redirect('/account/login/')

@csrf_exempt
def logoutView(request):
    if not request.user.is_authenticated:
        return redirect('/account/login/')
    logout(request)
    return redirect('/account/login/')

@csrf_exempt
def createCourse(request):
    if request.method == "POST" and request.user.is_authenticated:
        title = request.POST.get('title')
        tags = request.POST.get('tags')
        teacher = Pupil.objects.get(user=request.user)
        lesson_time = request.POST.get('lesson_time')
        if title != '' and tags != '' and lesson_time != '':
            course = Course()
            course.lesson_time = lesson_time
            course.title = title
            course.tags = tags
            course.teacher = teacher
            course.save()
            return JsonResponse({"status":"ok"})
    else:
        return redirect('/account/login/')


@csrf_exempt
def getCourses(request):
    if request.method == "GET" and request.user.is_authenticated:
        pupil = Pupil.objects.get(user=request.user)
        courses = Course.objects.filter(pupil=pupil)
        res = {'status': 'ok', 'result': []}
        for course in courses:
            res['result'].append({'title': course.title, 'tags': course.tags, 'lesson_time': course.lesson_time,'teacher': course.teacher.name})
        return JsonResponse(res)
    else:
        return redirect('/account/login/')


@csrf_exempt
def joinCourse(request):
    if request.method == "POST" and request.user.is_authenticated:
        pupil = Pupil.objects.get(user=request.user)
        course_id = request.POST.get('course_id')
        if course_id != '':
            course_id = int(course_id)
            course = Course.objects.get(id=course_id)
            pupil.courses.add(course)
            return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'failed', 'reason': 'Authentication failed'})