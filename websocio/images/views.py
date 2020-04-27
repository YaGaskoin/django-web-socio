import redis
from django.shortcuts import render, get_object_or_404
from .forms import ImageForm
from django.contrib import messages
from .models import Image
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action
from django.contrib.auth.decorators import login_required
from comments.forms import CommentForm
from comments.models import Comment


# Create your views here.
r = redis.Redis(host="localhost", port=6379, db=0)


@login_required
def add_image(request):
    if request.method == "POST":
        image_form = ImageForm(request.POST)
        if image_form.is_valid():
            image_save = image_form.save(commit=False)
            image_save.user = request.user
            image_save.save()
            messages.success(request, "Image saved successfully!")
            create_action(request.user, "added image", image_save)
        else:
            messages.error(request, "Image save error")
    else:
        image_form = ImageForm()
    return render(request, "images/add.html", {'image_form': image_form})


@login_required
def detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    total_views = r.incr("image:{}:views".format(image.id))
    r.zincrby("image_ranking", image.id, 1)
    comments = Comment.objects.filter(image_id=image.id)
    comment_form = CommentForm()
    return render(request, 'images/detail.html', {'image': image, 'total_views': total_views,
                                                  'comment_form': comment_form, 'comments': comments})


@login_required
def image_like(request):
    image_id = request.POST.get('id')
    image_action = request.POST.get('action')
    print(image_id, image_action)
    if image_id and image_action:
        try:
            image = Image.objects.get(id=image_id)
            if image_action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, "likes", image)
            else:
                image.users_like.remove(request.user)
        except Exception:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'ok'})


@login_required
def images(request, page):
    images = Image.objects.all()
    paginator = Paginator(images, 2)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
    if request.is_ajax():
        return render(request, "images/images_ajax.html", {"images": images})
    return render(request, "images/images.html", {"images": images})


@login_required
def image_ranking(request):
    # Получаем набор рейтинга картинок.
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    print(image_ranking)
    image_ranking_ids = [int(id) for id in image_ranking]
    # Получаем отсортированный список самых популярных картинок.
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    print(most_viewed)
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request,
                 'images/ranking.html',
                 {'section': 'images',
                 'images': most_viewed})