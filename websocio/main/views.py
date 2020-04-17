from django.shortcuts import render
from . forms import RegistrationForm, ProfileEdit, UserEdit
from .models import Profile
from django.contrib import messages

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


def edit(request):
    if request.method == "POST":
        user_form = UserEdit(data=request.POST, instance=request.user)
        profile_form = ProfileEdit(data=request.POST, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile update successfully")
        else:
            messages.error(request, "Profile update error")
    else:
        profile_form = ProfileEdit(instance=request.user.profile)
        user_form = UserEdit(instance=request.user)
    return render(request, "main/edit.html", {"user_form": user_form, "profile_form": profile_form})
