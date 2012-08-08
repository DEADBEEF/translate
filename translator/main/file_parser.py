#!/usr/bin/python

import os

#globals
top = "/home/zuch/WWW/translate/archive" #root directory of archive
dir_list = []

#returns array of Dicts with 'name' and 'depth' variables
def parser(path):
  
  startinglevel = path.count(os.sep)
  
  for path, dirs, files in os.walk(path):
    level = path.count(os.sep) - startinglevel
    node = {'name': path, 'depth': level}
    dir_list.append(node)
    
    #print level, ':', top

#-----------------------------------Main---------------------------------------        
if __name__ == "__main__":
  parser(top) 
  
  #for node in dir_list:
    #print "depth:",node['depth'],"name:",node['name']

  
  