from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Comment
from images.models import Image
from actions.utils import create_action

# Create your views here.


@login_required
def add_comment(request):
    image_id = request.POST.get('id')
    image = Image.objects.get(id=image_id)
    text = request.POST.get('text')
    Comment.objects.create(user=request.user, image=image, body=text)
    comment = Comment.objects.first()
    create_action(request.user, 'commented', image)

    return render(request, 'comments/comments_ajax.html', {'comments': [comment]})
