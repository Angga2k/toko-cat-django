from django.shortcuts import render
from django.http import HttpResponse
from . import templates

# Create your views here.

def index(request):
    context = {
        'header' : 'Hello World',
        'user_authentication' : True
    }

    return render(request, 'test.html', context)