from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from images.models import Image
from main.models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def user_detail(request, id):
    user = User.objects.get(id=id)
    user_images = Image.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    return render(request, 'people/user_detail.html', {'user': user, 'images': user_images[:10], 'profile': profile})


def people(request, page):
    users = User.objects.all()
    paginator = Paginator(users, 2)
    try:
        users = paginator.page(page)
    except EmptyPage:
        return HttpResponse("")
    except PageNotAnInteger:
        users = paginator.page(1)

    if request.is_ajax():
        return render(request, 'people/people_ajax.html', {'users': users})

    return render(request, 'people/people.html', {'users': users})



