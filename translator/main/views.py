from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from main.forms import *

def responseDict(request,base):
    if request.user.is_authenticated:
        base['user'] = request.user.username
    return base

# Create your views here.
def index(request):
    return render(request, 'index.html',responseDict(request,{}))

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
            return HttpResponseRedirect("/")
        #process
    else:
        form = RegisterForm()
    return render(request, 'register.html', responseDict(request,{'form': form}))

def loginView(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password  = form.cleaned_data["password"]
            user = authenticate(username=username,password=password)
            login(request,user)
            return HttpResponseRedirect("/")
    else:
        form = LoginForm()
    return render(request,'login.html',responseDict(request,{'form': form}))

def logoutView(request):
    logout(request)
    return HttpResponseRedirect("/")


