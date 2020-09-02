from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import NewUserRegistration

def registration(request):
    if request.method == 'POST':
        form = NewUserRegistration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NewUserRegistration()

    return render(request, 'users/registration.html', {'form': form})


def cabinet(request):
    if request.user.is_authenticated:
        name = request.user.get_username()
        usr = User.objects.get(username=name)
        context = {
            'user': usr
        }
        return render(request, 'users/cabinet.html', {'user': context})
    else:
        return redirect('login')