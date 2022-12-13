"""
All views for the lessons application.
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import redirect, render 
from django.urls import reverse
from .forms import BankTransferForm, LogInForm, RequestForm, SignUpForm
from .helpers import login_prohibited
from .models import BankTransfer, Request, Lesson
from .utils import updateReqEntry
from django.core.exceptions import PermissionDenied

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    pendingReqs = Request.objects.filter(user = request.user, is_approved = False)
    approvedReqs = Request.objects.filter(user = request.user, is_approved = True)
    unpaidReqs = Lesson.objects.filter(request__in = approvedReqs, paid = False)
    paidReqs = Lesson.objects.filter(request__in = approvedReqs, paid = True)
              
    return render(request, "dashboard.html", {"pending": pendingReqs, "unpaid": unpaidReqs, "paid": paidReqs})

@login_required
def deleteRequest(httpReq, req_id):
    try:
        req = Request.objects.get(id = req_id)
        if (req.user.id != httpReq.user.id):
            raise PermissionDenied
        req.delete()
        return redirect('dashboard')
    except Request.DoesNotExist:
        return HttpResponseNotFound()

@login_required
def editRequest(httpReq, req_id):
    try:
        reqToBeUpdated = Request.objects.get(id = req_id)
        if (reqToBeUpdated.user.id != httpReq.user.id):
            raise PermissionDenied
        if httpReq.method == 'POST':
            form = RequestForm(httpReq.POST, instance= reqToBeUpdated)      # form is initialised with the req data and prev entry to check for changes
            if form.is_valid():
                if form.has_changed():
                    updateReqEntry(reqToBeUpdated, form.cleaned_data)
                return redirect('dashboard')
            messages.add_message(httpReq, messages.ERROR, "Invalid form input")
        editForm = RequestForm(instance= reqToBeUpdated)
        return render(httpReq, 'edit-request.html', {'requestId': req_id,'form': editForm})
    except Request.DoesNotExist:
        return HttpResponseNotFound()

@login_required
def bank_transfer(httpReq, lesson_id):
    lessonToBePaid = Lesson.objects.get(request_id = lesson_id)
    if httpReq.method == 'POST':
        form = BankTransferForm(httpReq.POST)
        if form.is_valid():
            try:
                lessonToBePaid.pay_lesson(form.cleaned_data.get("invoice_number"))
                return HttpResponseRedirect(reverse('transfer-display'))
            except ValueError as errorMessage:
                messages.add_message(httpReq, messages.ERROR, errorMessage)
            except IntegrityError:
                messages.add_message(httpReq, messages.ERROR, "Invoice number must be unique.")

    form = BankTransferForm(httpReq.POST or None)
    return render(httpReq, 'bank-transfer.html',{'lessonId':lesson_id, 'lessonTBP':lessonToBePaid,'form':form})

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
            login(request, user, backend="allauth.account.auth_backends.AuthenticationBackend")
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
            return redirect('dashboard')
        # invalid form input
        messages.add_message(request, messages.ERROR, "Invalid form input")
    form = RequestForm(request.POST or None)
    return render(request, 'request-lessons.html', {'form': form})

@login_required
def log_out(request):
    logout(request)
    return redirect("home")



@login_required
def transfer_display(request):
    all_transfers= BankTransfer.objects.filter(user = request.user)
    return render(request, 'transfer-display.html', {'allTransfers':all_transfers})
