from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import  render

# Create your views here.


def index(request):

    return render(request, 'shop/index.html')


def about(request):

    return render(request, 'shop/about.html')