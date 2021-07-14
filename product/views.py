from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Product
from .forms import ProductForm
# Create your views here.


@login_required(login_url="/")
def productadd(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            Product.productname = form.cleaned_data['productname']
            Product.productquantity = form.cleaned_data['productquantity']
            Product.productstock = form.cleaned_data['productstock']
            Product.productprice = form.cleaned_data['productprice']

            productadded = form.save(commit=False)
            productadded.save()
            form = ProductForm()
        else:
            print('form is not valid')

    else:
        form = ProductForm()
    return render(request, 'productadd.html', {'form': form})


@login_required(login_url="/")
def productread(request):
    product = Product.objects.all()
    return render(request, 'productread.html', {'product': product})


@login_required(login_url="/")
def product_delete(request, id):
    if request.method == 'POST':
        delt = Product.objects.get(pk=id)
        delt.delete()
        return HttpResponseRedirect("/product/productread")


@login_required(login_url="/")
def product_update(request, id):
    if request.method == 'POST':
        updt = Product.objects.get(pk=id)
        form = ProductForm(request.POST, instance=updt)
        if form.is_valid():
            form.save()
        else:
            print('invalid form')
    updt = Product.objects.get(pk=id)
    form = ProductForm(instance=updt)
    return render(request, 'productupdate.html', {'form': form})
