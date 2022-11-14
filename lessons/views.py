from django.shortcuts import render
from .forms import RequestForm


def request_lessons(request):
    form = RequestForm()
    return render(request, 'request-lessons.html', {'form': form})

def home(request):
    return render(request, 'home.html')