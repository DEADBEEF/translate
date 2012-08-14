from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import Http404
from django.shortcuts import redirect

# DOM
import json
from xml.dom.minidom import parse, parseString

from main.models import *
from main.forms import *

MEDIA_ROOT = "/home/ttrewartha/www/archive/lloydbleek/"

def responseDict(request,base):
    print int(request.user.is_authenticated())
    if request.user.is_authenticated():
        base['user_o'] = request.user.username
        base['projects'] = [ ( pro.story.notebook.short_title, pro.story.id, pro.story.title)
                                       for pro in Project.objects.filter(user=request.user) ]
    return base

# Create your views here.
def index(request):
    return render(request, 'main/index.html',responseDict(request,{}))

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
                "author": ", ".join(json.loads(story.contributor)), "short_title":notebook.short_title, "id":story.id }
        stories.append(current_story)
    base["book"] = stories
    return render(request, 'main/notebook.html' , responseDict(request,base))

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
            base["notes"] = project.notes
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
    return render(request, 'main/story.html' , responseDict(request,base))

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
            base["notes"] = trans.notes
            print trans.notes
        except:
            pass
    base["story_title"] = story_book.title
    base["pages"] = xrange(1,story_book.pages+1)
    base["page_num"] = int(page)
    if base["page_num"] != story_book.pages:
        base["page_next"] = int(page) + 1
    if base["page_num"] != 1:
        base["page_prev"] = int(page) - 1
    base["uuid"] = page_object.uuid
    return render(request, 'main/page.html' , responseDict(request,base))



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password  = form.cleaned_data["password"]
            User.objects.create_user(username,email,password)
            user = authenticate(username=username,password=password)
            if user.is_authenticated():
                login(request,user)
                return redirect("main.views.index")
        #process
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', responseDict(request,{'form': form}))

def loginView(request):
    if request.user.is_authenticated():
        return redirect("main.views.index")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password  = form.cleaned_data["password"]
            user = authenticate(username=username,password=password)
            if user != None:
                login(request,user)
                return redirect('main.views.index')
    else:
        form = LoginForm()
    return render(request,'main/login.html',responseDict(request,{'form': form}))

def logoutView(request):
    logout(request)
    return redirect('main.views.index')

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

def update_notes(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            query = request.POST
            note = query["note"]
            notebook_name = query["notebook"]
            story_name = query["story"]
            field = query["field"]
            try:
                notebook = Notebook.objects.get(short_title=notebook_name)
                story_book = Story.objects.get(notebook=notebook,id=story_name)
            except:
                raise Http404
            project, created = Project.objects.get_or_create(user=request.user,story=story_book,
                    defaults={"notes":""})
            if (field == "project"):
                project.notes = note
                project.save()
            else:
                page_num = int(field)
                try:
                    page = Page.objects.get(story=story_book,number=page_num)
                except:
                    raise Http404
                trans, created = Translation.objects.get_or_create(project=project,page=page)
                trans.notes = note
                trans.save()
            return HttpResponse("good")
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()


def get_note(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            query = request.GET
            notebook_name = query["notebook"]
            story_name = query["story"]
            field = query["field"]
            try:
                notebook = Notebook.objects.get(short_title=notebook_name)
                story_book = Story.objects.get(notebook=notebook,id=story_name)
            except:
                raise Http404
            project, created = Project.objects.get_or_create(user=request.user,story=story_book,
                    defaults={"notes":""})
            if (field == "project"):
                note = project.notes
            else:
                page_num = int(field)
                try:
                    page = Page.objects.get(story=story_book,number=page_num)
                except:
                    raise Http404
                trans, created = Translation.objects.get_or_create(project=project,page=page)
                note = trans.notes
            return HttpResponse(note)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()


