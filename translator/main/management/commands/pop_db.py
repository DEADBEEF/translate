import os
import uuid
import json
import time
from django.core.management.base import BaseCommand, CommandError
from main.models import Page, Notebook, Story
from xml.dom.minidom import parse, parseString # DOM
from timeit import Timer

#globals
top = "/home/zuch/WWW/translate/archive/lloydbleek/stories/" #root directory of stories archive

#node class
class node:
  path = ""
  depth = ""
  dirs = []
  files = []
  
  def __init__(self,path,depth,dirs,files):
    self.path = path
    self.depth = depth
    self.dirs = dirs
    self.files = files

class Command(BaseCommand):
    args = ""
    def handle(self, *args, **options):
      print "die die die die"
      start = time.clock()
      popdb()
      end = time.clock()
      print 'Code time %.2f seconds', (end - start)
	  
	  
#returns array of node objects for a given path
def parse_path(path):
  
  dir_list = []
  startinglevel = path.count(os.sep)
  
  for path, dirs, files in os.walk(path):
    depth = path.count(os.sep) - startinglevel
    Node = node(path,depth,dirs,files)
    dir_list.append(Node)
    
  return dir_list
 
#populate database
def popdb():
  nodes = parse_path(top)
  
  i = 0
  for node in nodes:
    if(i == 0):#populate notebook models
      nb_meta = node.files
      for filename in nb_meta:
	notebook_meta(filename)
    
    if (len(node.path) > len(top) ):#populate story models
      s_meta = node.files
      for filename in s_meta:
	path = node.path
	story_meta(filename, path)
	
    i+=1

#parses notebook metadata files
def notebook_meta(filename):
  
  print "notebook_meta"
  dom = parse(top+filename)
  resource = dom.getElementsByTagName("resource")[0]
  nb = resource.getElementsByTagName("dc:title")[0].firstChild.nodeValue
  short = filename[:-18]
  
  notebook = Notebook(title=nb, short_title=short)
  notebook.save()
  
  hasPart = [resource.getElementsByTagName("dcterms:hasPart")]  
  
#parses story metadata files
def story_meta(filename, path):
  print "story_meta"
  notebook_name = path.split("/")[-1][:-9]
  dom = parse(path+"/"+filename)
  resource = dom.getElementsByTagName("resource")[0]
  story_title = resource.getElementsByTagName("dc:title")[0].firstChild.nodeValue
  raw_contrib = [x.firstChild.nodeValue
      for x in resource.getElementsByTagName("dcterms:contributor") ]
  contrib = json.dumps(raw_contrib)
  required = resource.getElementsByTagName("dcterms:requires")
  pages = len(required)
  try:
    date = resource.getElementsByTagName("dcterms:created")[0].firstChild.nodeValue
  except AttributeError:
    date = ""
  try:
    description = resource.getElementsByTagName("dc:description")[0].firstChild.nodeValue
  except AttributeError:
    description = ""
  try:
    comments = resource.getElementsByTagName("bl:comments")[0].firstChild.nodeValue
  except AttributeError:
    comments = ""
  raw_subject = [sub.firstChild.nodeValue for sub in resource.getElementsByTagName("dc:subject")]
  subject = json.dumps(raw_subject)
  raw_keywords = []
  try:
    temp = dom.getElementsByTagName("bl:keywords")[0]
    for word in temp.getElementsByTagName("bl:keyword"):
	k = word.getElementsByTagName("bl:kw")[0].firstChild.nodeValue
	subkw = word.getElementsByTagName("bl:subkeywords")[0]
	v = ", ".join(sub.firstChild.nodeValue
		for sub in subkw.getElementsByTagName("bl:subkw"))
	raw_keywords.append((k, v))
  except AttributeError:
    pass
  keyword = json.dumps(raw_keywords)
  notebook = Notebook.objects.get(short_title=notebook_name)
  
  story = Story(notebook=notebook, title=story_title, created=date, description=description, 
		comment=comments, contributor=contrib, subject=subject, keyword=keyword, pages=pages )
  story.save()
  i=1
  for page in required:
    page_path = page.firstChild.nodeValue
    page_uuid = uuid.uuid4()
    page_entry = Page(story = story, filename = page_path, uuid = page_uuid,number=i)
    i+=1
    page_entry.save()
  
  
  

