import os

from django.core.management.base import BaseCommand, CommandError
from main.models import Page, Notebook, Story
from xml.dom.minidom import parse, parseString # DOM
import json

#globals
top = "/home/swatermeyer/WWW/translate/archive/lloydbleek/stories/" #root directory of stories archive

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
      popdb()
	  
	  
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
  print "popdb"
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
  notebook_name = path.split("/")[-1][:-9]
  print "story_meta"
  dom = parse(path+"/"+filename)
  resource = dom.getElementsByTagName("resource")[0]
  story_title = resource.getElementsByTagName("dc:title")[0].firstChild.nodeValue
  raw_contrib = [x.firstChild.nodeValue
      for x in resource.getElementsByTagName("dcterms:contributor") ]
  contrib = json.dumps(raw_contrib)
  pages = len(resource.getElementsByTagName("dcterms:requires"))
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
  notebook = Notebook.object.get(short_title=notebook_name)[0]
  
  
  story = Story(notebook=notebook, title=story_title, created=date, description=description, 
		comment=comments, contributor=contrib, subject=subject, keyword=keyword, pages=pages
  story.save()
    
#-----------------------------------Main---------------------------------------
if __name__ == "__main__":
  nodes = parse_path(top)
    
  i = 0
  for node in nodes:
    print "path:", node.path
    print "depth:",node.depth
    print "dirs:",node.dirs
    print "files:",node.files
    print "-"*100
    i += 1
    if(i >= 7):
      break
  
  
  

