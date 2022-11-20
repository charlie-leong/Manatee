from django.shortcuts import render, redirect
from .forms import SignUpForm, LogInForm
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, "dashboard.html")

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            #extract and verify username passwrod combo
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        # contains a dictionary of data that has been  posted
        form = SignUpForm(request.POST) # creates a bound version of form with post data
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})
