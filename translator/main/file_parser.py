#!/usr/bin/python

import os

top = "/home/zuch/WWW/translate/archive"

#tree Node class
class Node(object):
  
  def __init__(self,path,dirs):
    self.path = path
    self.dirs = dirs
 
#file_parser class 
class file_parser: 

  def __init__(self,top):
    self.top = top  
  
  base_dir = ""
  archive_paths = {}
  nodes = {}

  i = 0

  for (top, dirs, files) in os.walk(top):
    #print path
    #print dirs
    #print files
    #print "--------------------"

    i += 1
    print i
    if i == 4:
      break
  
  startinglevel = top.count(os.sep)
  for top, dirs, files in os.walk(top):
    level = top.count(os.sep) - startinglevel
    print level, ':', top 

  print "end"

  
if __name__ == "__main__":
  file_parser(top)
