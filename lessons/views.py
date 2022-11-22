from django.shortcuts import render
from .forms import RequestForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Request


def request_lessons(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('request-display'))

    form = RequestForm(request.POST or None)
    return render(request, 'request-lessons.html', {'form': form})

def home(request):
    return render(request, 'home.html')


def request_display(request):
    allRequests = Request.objects.all()
    return render (request, 'request-display.html', {'allRequests':allRequests})
