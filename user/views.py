from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import User
from .forms import UserForm
# Create your views here.


def useradd(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            useradded = form.save(commit=False)
            useradded.save()

        else:
            print('form is not valid')

    else:
        form = UserForm()
    return render(request, 'useradd.html', {'form': form})


def userread(request):
    user = User.objects.all()
    return render(request, 'userread.html', {'user': user})
