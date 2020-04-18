from django.shortcuts import render, get_object_or_404
from .forms import ImageForm
from django.contrib import messages
from .models import Image
from django.http import JsonResponse

# Create your views here.


def add_image(request):
    if request.method == "POST":
        image_form = ImageForm(request.POST)
        if image_form.is_valid():
            image_save = image_form.save(commit=False)
            image_save.user = request.user
            image_save.save()
            messages.success(request, "Image saved successfully!")
        else:
            messages.error(request, "Image save error")
    else:
        image_form = ImageForm()
    return render(request, "images/add.html", {'image_form': image_form})


#def images(request):


def detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/detail.html', {'image': image})


def image_like(request):
    image_id = request.POST.get('id')
    image_action = request.POST.get('id')
    if image_id and image_action:
        try:
            image = Image.objects.get(id=image_id)
            if image_action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.delete(request.user)
        except Exception:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'ok'})
