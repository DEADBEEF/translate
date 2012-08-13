from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import Http404

# DOM
import json
from xml.dom.minidom import parse, parseString

from main.models import *
from main.forms import *

MEDIA_ROOT = ""

def responseDict(request,base):
    if request.user.is_authenticated:
        base['user'] = request.user.username
    return base

# Create your views here.
def index(request):
    return render(request, 'index.html',responseDict(request,{}))

def notebook(request, book):
    #Should be filled in from notebook
    try:
        notebook = Notebook.objects.get(short_title=book)
        story_list = Story.objects.filter(notebook=notebook)
    except:
        raise Http404
    base = {}
    base["book_title"] = notebook.title
    stories = []
    for story in story_list:
        current_story = {"name": story.title,
        "author": ", ".join(json.loads(story.contributor)), "url":("/story/%s/%s/" % (notebook.short_title, story.id)) }
        stories.append(current_story)
    base["book"] = stories
    return render(request, 'notebook.html' , responseDict(request,base))

def story(request, book, story):
    #Should be filled in from story
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
            trans = Translation.objects.get(project=project,page=page)
            base["trans"] = trans.translation
        except:
            pass
    base["story_title"] = story_book.title
    base["contributors"] = ", ".join(json.loads(story_book.contributor))
    base["pages"] = xrange(1,story_book.pages+1)
    base["date"] = story_book.created
    base["description"] = story_book.description
    base["comments"] = story_book.comment
    base["subjects"] = json.loads(story_book.subject)
    base["keywords"] = json.loads(story_book.keyword)
    return render(request, 'story.html' , responseDict(request,base))

def page(request, book, story, page):
    try:
        notebook = Notebook.objects.get(short_title=book)
        story_book = Story.objects.get(notebook=notebook,id=story)
        page_object = Page.objects.get(story=story_book,number=page)
    except:
        raise Http404
    base = {}
    if request.user.is_authenticated():
        #project
        try:
            project = Project.objects.get(user=request.user,story=story_book)
            base["project"] = True
            trans = Translation.objects.get(project=project,page=page_object)
            base["trans"] = trans.translation
        except:
            pass
    base["story_title"] = story_book.title
    base["pages"] = xrange(1,story_book.pages+1)
    base["page_num"] = int(page)
    base["uuid"] = page_object.uuid
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

def get_image(request, image):
    try:
        page = Page.objects.get(uuid=image)
    except:
        raise Http404
    filename = page.filename
    response = HttpResponse(mimetype='image/jpeg')
    try:
        f = file(MEDIA_ROOT+ filename)
    except:
        raise Http404
    response.write(f.read())
    return response

#AJAX
def start_project(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            query = request.POST
            book = query["book"]
            story=query["story"]
            try:
                notebook = Notebook.objects.get(short_title=book)
                story_book = Story.objects.get(notebook=notebook,id=story)
            except:
                raise Http404
            obj, created = Project.objects.get_or_create(user=request.user,story=story_book,
                    defaults={"notes":""})
            return HttpResponse(str(created))
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()

def update_page_translation(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            query = request.POST
            translation = query["translation"]
            notebook_name = query["notebook"]
            story_name = query["story"]
            page_num = query["page"]
            try:
                notebook = Notebook.objects.get(short_title=notebook_name)
                story_book = Story.objects.get(notebook=notebook,id=story_name)
                page = Page.objects.get(story=story_book,number=page_num)
            except:
                raise Http404
            project, created = Project.objects.get_or_create(user=request.user,story=story_book,
                    defaults={"notes":""})
            trans, created = Translation.objects.get_or_create(project=project,page=page)
            trans.translation = translation
            trans.save()
            return HttpResponse("good")
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()
