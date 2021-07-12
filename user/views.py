from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import User
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


@login_required(login_url="/")
def useradd(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            User.name = form.cleaned_data['name']
            User.address = form.cleaned_data['address']
            User.email = form.cleaned_data['password']
            User.password = form.cleaned_data['password']

            useradded = form.save(commit=False)
            useradded.save()
            form = UserForm()
            messages.add_message(request, messages.SUCCESS,
                                 'your Account has been registered Successfully.')
        else:
            print('form is not valid')

    else:
        form = UserForm()
    return render(request, 'useradd.html', {'form': form})


@login_required(login_url="/")
def userread(request):
    user = User.objects.all()
    return render(request, 'userread.html', {'user': user})


@login_required(login_url="/")
def user_update(request, id):
    if request.method == 'POST':
        updt = User.objects.get(pk=id)
        form = UserForm(request.POST, instance=updt)
        if form.is_valid():
            form.save()
        else:
            print('invalid')
    updt = User.objects.get(pk=id)
    form = UserForm(instance=updt)
    messages.add_message(request, messages.SUCCESS,
                         'Your Account Has Been Updated.')
    return render(request, 'userupdate.html', {'form': form})


@login_required(login_url="/")
def user_delete(request, id):
    if request.method == 'POST':
        delt = User.objects.get(pk=id)
        delt.delete()
        messages.add_message(request, messages.SUCCESS,
                             'Your Account Has Been Deleted.')
        return HttpResponseRedirect("/user/userread")
