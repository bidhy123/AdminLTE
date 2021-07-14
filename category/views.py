from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Category
from .forms import CategoryForm
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="/")
def Categoryadd(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            Category.categoryname = form.cleaned_data['categoryname']
            Category.vendor = form.cleaned_data['vendor']

            categoryadded = form.save(commit=False)
            categoryadded.save()
            form = CategoryForm()
        else:
            print('form is not valid')

    else:
        form = CategoryForm()
    return render(request, 'categoryadd.html', {'form': form})


@login_required(login_url="/")
def categoryread(request):
    category = Category.objects.all()
    return render(request, 'categoryread.html', {'category': category})


@login_required(login_url="/")
def category_delete(request, id):
    if request.method == 'POST':
        delt = Category.objects.get(pk=id)
        delt.delete()
        return HttpResponseRedirect("/category/categoryread")


@login_required(login_url="/")
def category_update(request, id):
    if request.method == 'POST':
        updt = Category.objects.get(pk=id)
        form = CategoryForm(request.POST, instance=updt)
        if form.is_valid():
            form.save()
        else:
            print('invalid form')
    updt = Category.objects.get(pk=id)
    form = CategoryForm(instance=updt)
    return render(request, 'categoryupdate.html', {'form': form})
