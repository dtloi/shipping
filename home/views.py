from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render



def index(request):
    return render(request, 'home/home.html')


def submit(request):
    test = request.POST
    print(test)
    return