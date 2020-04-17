from django.shortcuts import render
from .forms import ImageForm
from django.contrib import messages

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