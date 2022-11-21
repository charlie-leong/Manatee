from django.shortcuts import render
from .forms import RequestForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def request_lessons(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))

    form = RequestForm(request.POST or None)
    return render(request, 'request-lessons.html', {'form': form})

def home(request):
    return render(request, 'home.html')
