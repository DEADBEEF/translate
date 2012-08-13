#!/usr/bin/python

import os

from xml.dom.minidom import parse, parseString # DOM

#globals
top = "/home/swatermeyer/WWW/translate/archive" #root directory of archive

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
  
  for node in nodes:
      if():
	#/home/swatermeyer/WWW/translate/archive/lloydbleek/books/
  
def notebook(book):
  
  #Should be filled in from books
  base = {}
  base["book_title"] = "Wilhelm Bleek Notebook"
  stories = [{"name": "The Mantis turned into a hartebeest.",
      "author": "|| kabo (Jantje)", "url":("/%s/%s/" % (book, "101")) },
      {"name": "The Mantis turned is a bitch.",
      "author": "|| kabo ()", "url":("/%s/%s/" % (book, "102")) }]
  base["book"] = stories
  

def story(book, story):
  #Should be filled in from books
  dom = parse("/home/michiel/git/translate/101.metadata")
  resource = dom.getElementsByTagName("resource")[0]
  base = {}
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
  
  
  