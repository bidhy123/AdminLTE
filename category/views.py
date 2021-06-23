from django.shortcuts import render

# Create your views here.


def categoryadd(request):
    return render(request, 'categoryadd.html')


def categoryread(request):
    return render(request, 'categoryread.html')
