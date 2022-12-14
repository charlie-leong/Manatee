"""msms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from lessons import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log_in/', views.log_in, name='log_in'),
    path("dashboard/", views.dashboard, name = "dashboard"),
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('', views.home, name='home'),
    path('request-lessons/', views.request_lessons, name='request-lessons'),
    path("log_out/", views.log_out, name = "log_out"),
    path('bank-transfer/<uuid:lesson_id>', views.bank_transfer, name='bank-transfer'),
    path('transfer-display/', views.transfer_display, name='transfer-display'),
    path('delete-request/<uuid:req_id>', views.deleteRequest, name='delete-request'),
    path('edit-request/<uuid:req_id>', views.editRequest, name='edit-request'),
    path('accounts/', include('allauth.urls')),
]

