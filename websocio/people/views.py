from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from images.models import Image
from main.models import Profile, Contact
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action

# Create your views here.


def user_detail(request, id):
    if request.method == "POST":
        follower_action = request.POST.get("action")
        user_to = User.objects.get(id=id)
        try:
            if follower_action == "follow":
                Contact.objects.create(user_from=request.user, user_to=user_to)
                create_action(request.user, "followed", user_to)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user_to).delete()
                create_action(request.user, "unfollowed", user_to)
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
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



