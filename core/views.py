from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "core/index.html")

def subscriptions(request):
    return render(request, "core/subscriptions.html")

def payments(request):
    return render(request, "core/payments.html")

def help_center(request):
    return render(request, "core/help-center.html")

def blog(request):
    return render(request, "core/blog.html")

def security(request):
    return render(request, "core/security.html")

def about(request):
    return render(request, "core/about.html")
