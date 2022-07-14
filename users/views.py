from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth import update_session_auth_hash

from users.forms import RegisterUserForm, EditProfileForm


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('../totalsJSON')
        else:
            messages.success(
                request, ("Wrong username or password. Please try again."))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    return redirect('../')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            #messages.success(request, ("User account created!"))
            return redirect('../totalsJSON')
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {'form': form, })


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # if you leave this out auth session will be invalidated
            update_session_auth_hash(request, user)
            messages.success(
                request, ("Password updated."))
            return redirect('change_password')
        else:
            messages.error(request, "Something went wrong. Try again.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'authenticate/change_password.html', {'form': form})


def edit_profile(request):
    form = EditProfileForm(instance=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # return redirect('../totalsJSON')
            messages.success(request, ("Account info updated."))
            return render(request, 'authenticate/edit_profile.html', {'form': form})
    return render(request, 'authenticate/edit_profile.html', {'form': form})
