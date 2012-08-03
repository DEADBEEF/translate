from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

from main.forms import *

# Create your views here.
def index(request):
    return HttpResponse("Hello there.")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password  = form.cleaned_data["password"]
            User.objects.create_user(username,email,password)
            user = authenticate(username=username,password=password)
            login(request,user)
            return HttpResponseRedirect("/success")
        #process
    else:
        form = RegisterForm()
    return render(request, 'register.html', { 'form': form})

def success(request):
    if request.user.is_authenticated():
        return HttpResponse("yay")
    else:
        return HttpResponseRedirect("/")

