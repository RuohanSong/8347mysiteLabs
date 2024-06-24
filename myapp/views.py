from django.http import HttpResponse
from django.shortcuts import render

from myapp.models import Book


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index0.html', {'booklist': booklist})

def about_view(request):
    return render(request, 'myapp/about0.html')