from django.shortcuts import render

# Create your views here.


def productadd(request):
    return render(request, 'productadd.html')


def productread(request):
    return render(request, 'productread.html')
