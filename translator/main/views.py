from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import Http404

# DOM
from xml.dom.minidom import parse, parseString

from main.models import *
from main.forms import *

def responseDict(request,base):
    if request.user.is_authenticated:
        base['user'] = request.user.username
    return base

# Create your views here.
def index(request):
    return render(request, 'index.html',responseDict(request,{}))

def notebook(request, book):
    #Should be filled in from books
    base = {}
    base["book_title"] = "Wilhelm Bleek Notebook"
    stories = [{"name": "The Mantis turned into a hartebeest.",
        "author": "|| kabo (Jantje)", "url":("/%s/%s/" % (book, "101")) },
        {"name": "The Mantis turned is a bitch.",
        "author": "|| kabo ()", "url":("/%s/%s/" % (book, "102")) }]
    base["book"] = stories
    return render(request, 'notebook.html' , responseDict(request,base))

def story(request, book, story):
    #Should be filled in from books
    try:
        notebook = Notebook.objects.get(short_title=book)
        story_book = Story.objects.get(notebook=notebook,id=story)
    except:
        raise Http404
    base = {}
    if request.user.is_authenticated():
        #project
        try:
            project = Project.objects.get(user=request.user,story=story_book)
            base["project"] = True
        except:
            pass
    dom = parse("/home/michiel/git/translate/101.metadata")
    resource = dom.getElementsByTagName("resource")[0]
    base["story_title"] = resource.getElementsByTagName("dc:title")[0].firstChild.nodeValue
    base["contributors"] = ", ".join([x.firstChild.nodeValue
        for x in resource.getElementsByTagName("dcterms:contributor") ])
    base["pages"] = xrange(1,len(resource.getElementsByTagName("dcterms:requires"))+1)
    base["date"] = resource.getElementsByTagName("dcterms:created")[0].firstChild.nodeValue
    base["description"] = resource.getElementsByTagName("dc:description")[0].firstChild.nodeValue
    base["comments"] = resource.getElementsByTagName("bl:comments")[0].firstChild.nodeValue
    base["subjects"] = [sub.firstChild.nodeValue for sub in resource.getElementsByTagName("dc:subject")]
    keywords = []
    temp = dom.getElementsByTagName("bl:keywords")[0]
    for word in temp.getElementsByTagName("bl:keyword"):
        k = word.getElementsByTagName("bl:kw")[0].firstChild.nodeValue
        subkw = word.getElementsByTagName("bl:subkeywords")[0]
        v = ", ".join(sub.firstChild.nodeValue
                for sub in subkw.getElementsByTagName("bl:subkw"))
        keywords.append((k, v))
    base["keywords"] = keywords
    return render(request, 'story.html' , responseDict(request,base))

def page(request, book, story, page):
    try:
        notebook = Notebook.objects.get(short_title=book)
        story_book = Story.objects.get(notebook=notebook,id=story)
    except:
        raise Http404
    base = {}
    if request.user.is_authenticated():
        #project
        try:
            project = Project.objects.get(user=request.user,story=story_book)
            base["project"] = True
        except:
            pass
    base["story_title"] = story_book.title
    base["pages"] = xrange(1,story_book.pages+1)
    base["page_num"] = int(page)
    return render(request, 'page.html' , responseDict(request,base))



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

#AJAX
def start_project(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            query = request.POST
            book = query["book"]
            story=query["story"]
            try:
                print book,story
                notebook = Notebook.objects.get(short_title=book)
                story_book = Story.objects.get(notebook=notebook,id=story)
                print notebook.short_title, story_book.id
            except:
                raise Http404
            obj, created = Project.objects.get_or_create(user=request.user,story=story_book,
                    defaults={"notes":""})
            return HttpResponse(str(created))
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()

