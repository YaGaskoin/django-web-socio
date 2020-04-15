from django.shortcuts import render
from . forms import RegistrationForm
from .models import Profile

# Create your views here.


def dashboard(request):
    return render(request, 'main/dashboard.html')


def register(request):
    if request.method == "POST":
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data['password1'])
            new_user.save()
            Profile.objects.create(user=new_user).save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:

        register_form = RegistrationForm()
    return render(request, 'registration/register.html', {'register_form': register_form})
