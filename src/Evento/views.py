from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def home_view(*arg, **kwargs):
    return HttpResponse('<h1> Hello from MArs </h1>')
