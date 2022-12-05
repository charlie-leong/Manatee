from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Request
from .forms import LogInForm, RequestForm, SignUpForm, BankTransferForm
from .helpers import login_prohibited

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        next = request.POST.get('next') or ''
        if form.is_valid():
            #extract and verify email passwrod combo
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                redirect_url = next or "dashboard"
                return redirect(redirect_url)
        # If invalid login details
        messages.add_message(request, messages.ERROR, "Invalid email or password")
    else:
        next = request.GET.get('next') or ''
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form, "next" : next})

@login_prohibited
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

@login_required
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

@login_required
def request_display(request):
    all_requests = Request.objects.all()
    return render (request, 'request-display.html', {'allRequests':all_requests})

@login_required
def log_out(request):
    logout(request)
    return redirect("home")

@login_required
def bank_transfer(request):
    if request.method == 'POST':
      form = BankTransferForm(request.POST)
      if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('transfer-display'))

    form = BankTransferForm(request.POST or None)
    return render(request, 'bank-transfer.html',{'form':form})

@login_required
def transfer_display(request):
    return render(request, 'transfer-display.html')
