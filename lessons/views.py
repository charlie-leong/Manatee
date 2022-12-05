from django.shortcuts import render
from .forms import RequestForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Request

from email import message
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, "dashboard.html")

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            #extract and verify email password combo
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        # If invalid login details
        messages.add_message(request, messages.ERROR, "Invalid email or password")
        
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        # contains a dictionary of data that has been  posted
        form = SignUpForm(request.POST) # creates a bound version of form with post data
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def request_lessons(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse('request-display'))
        # invalid form input
        messages.add_message(request, messages.ERROR, "Invalid form input")
        
    form = RequestForm(request.POST or None)
    return render(request, 'request-lessons.html', {'form': form})


def request_display(request):
    allRequests = Request.objects.all()
    return render (request, 'request-display.html', {'allRequests':allRequests})

def log_out(request):
    logout(request)
    return redirect("home")
    
def bank_transfer(request):
    if request.method == 'POST':
      form = BankTransferForm(request.POST)
      if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('transfer-display'))

    form = BankTransferForm(request.POST or None)
    return render(request, 'bank-transfer.html',{'form':form})

def transfer_display(request):
    return render(request, 'transfer-display.html')
