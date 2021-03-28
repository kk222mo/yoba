import random

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.views import View

from yob.models import Pupil, Course, Review


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
        if name.rstrip() != '' and email.rstrip() != '' and passw.rstrip() != '':
            user = User.objects.create_user(email, email=email, password=passw)
            user.save()
            pupil = Pupil()
            pupil.user = user
            pupil.is_teacher = False
            pupil.name = name
            pupil.save()
            login(request, user)
            return redirect('/')
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


def generateCode(ln):
    res = ""
    chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    for i in range(ln):
        res += chars[random.randint(0, len(chars) - 1)]
    return res


@csrf_exempt
def createCourse(request):
    if request.method == "POST" and request.user.is_authenticated:
        title = request.POST.get('title')
        tags = request.POST.get('tags')
        teacher = Pupil.objects.get(user=request.user)
        lesson_time = request.POST.get('lesson_time')
        if title.rstrip() != '' and tags.rstrip() != '' and lesson_time.rstrip() != '':
            course = Course()
            course.lesson_time = lesson_time
            course.title = title
            course.tags = tags
            course.token = generateCode(64)
            course.teacher = teacher
            course.save()
            return JsonResponse({"status":"ok"})
    else:
        return redirect('/account/login/')


@csrf_exempt
def getAllCourses(request):
    courses = Course.objects.all()
    res = {'status': 'ok', 'result': []}
    for course in courses:
        res['result'].append({'title': course.title, 'tags': course.tags, 'lesson_time': course.lesson_time,
                              'teacher': course.teacher.name, 'token': course.token})
    return JsonResponse(res)


@csrf_exempt
def getMyCourses(request):
    if request.method == "GET" and request.user.is_authenticated:
        pupil = Pupil.objects.get(user=request.user)
        courses = Course.objects.filter(pupil=pupil)
        res = {'status': 'ok', 'result': []}
        for course in courses:
            res['result'].append({'title': course.title, 'tags': course.tags, 'lesson_time': course.lesson_time,'teacher': course.teacher.name,
                                  'token': course.token})
        return JsonResponse(res)
    else:
        return redirect('/account/login/')


@csrf_exempt
def joinCourse(request):
    if request.method == "POST" and request.user.is_authenticated:
        pupil = Pupil.objects.get(user=request.user)
        course_token = request.POST.get('course_token')
        if course_token != '':
            course = Course.objects.get(token=course_token)
            if len(pupil.courses.filter(token=course_token)) == 0:
                pupil.courses.add(course)
            else:
                pupil.courses.remove(course)
            return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'failed', 'reason': 'Authentication failed'})


@csrf_exempt
def index(request):
    courses = Course.objects.filter(is_private=False)
    res = []
    for course in courses:
        people = Pupil.objects.filter(courses__in=[course])
        res.append({'title': course.title, 'description': course.description, 'name': course.teacher.name,
                    'count': len(people), 'count_cropped': range(min(3, len(people))), 'token': course.token,
                    'tags': course.tags})
    return render(request, 'index.html', {'courses': res, 'is_authenticated': request.user.is_authenticated})


@csrf_exempt
def my_courses(request):
    if request.method == "GET" and request.user.is_authenticated:
        pupil = Pupil.objects.get(user=request.user)
        courses = Course.objects.filter(pupil=pupil)
        res = []
        for course in courses:
            people = Pupil.objects.filter(courses__in=[course])
            res.append({'title': course.title, 'description': course.description, 'name': course.teacher.name,
                        'count': len(people), 'count_cropped': range(min(3, len(people))), 'token': course.token,
                        'tags': course.tags})
        return render(request, 'mycourses.html', {'courses': res, 'is_authenticated': request.user.is_authenticated})
    else:
        return redirect('/account/login/')


@csrf_exempt
def postReview(request):
    if request.method == "POST" and request.user.is_authenticated:
        text = request.POST.get('text')
        token = request.POST.get('course_token')
        if text.rstrip() != '' and token.rstrip() != '':
            pupil = Pupil.objects.get(user=request.user)
            review = Review()
            review.course_token = token
            review.text = text
            review.pupil = pupil
            review.save()
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'failed'})


@csrf_exempt
def courseInfo(request, token):
    print(token)
    course = Course.objects.get(token=token)
    res = {}
    is_subscriped = False
    if request.user.is_authenticated:
        pupil = Pupil.objects.get(user=request.user)
        is_subscriped = len(pupil.courses.filter(token=course.token)) > 0
    res['name'] = course.teacher.name
    res['title'] = course.title
    res['token'] = course.token
    res['description'] = course.description
    res['count'] = len(Pupil.objects.filter(courses__in=[course]))
    res['reviews_count'] = len(Review.objects.filter(course_token=token))
    return render(request, 'course.html', {'course': res, 'is_subscribed': is_subscriped})


@csrf_exempt
def getReviews(request):
    token = request.GET.get('course_token')
    if token.rstrip() != '':
        reviews = Review.objects.filter(course_token=token)
        res = {'status': 'ok', 'result': []}
        for review in reviews:
            res['result'].append({'user_name': review.pupil.name, 'text': review.text})
        return JsonResponse(res)
    return JsonResponse({'status': 'failed'})