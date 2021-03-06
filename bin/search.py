#!/usr/bin/env python3
#
# Search script for the WikiPedia sqlite db
#
# Copyright (c) 2016    Pieter-Jan Moreels - pieterjan.moreels@gmail.com

# Imports
import argparse
import os
import sys
runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

from specter import Specter

from lib.Config import Configuration as conf
from lib.DatabaseConnection import dbConnector

def search(text):
  results = db.searchPages(text)
  if len(results) == 0:
    print('No results found')
  else:
    footer=["Press the ESC key to quit"]
    al = lambda x, y: x+" "*(y-len(x))
    text = [[x['id'], x['title'], x['text']] for x in results]
    lI = max(max([len(str(x[0])) for x in text]), len("Index")) + 2
    lT = max(max([len(x[1]) for x in text]), len("Title")) + 2
    text=[[x[0], x[1], x[2].replace("\n", " -- ")] for x in text]
    text=[al(str(x[0]), lI)+al(x[1], lT)+x[2][:50] for x in text]
    text = [{'t': x.replace("\n", " -- ")} for x in text]
    text.insert(0, al('Index', lI)+al('Title', lT)+'Content')
    display(text)

def open(index):
  try:
    text = db.openPage(index)
    if text:
      text = text.split("\n")
      text = [{'t': x} for x in text]
      display(text)
    else:    print('Page not found')
  except ValueError:
    print('Please specify the index number')

def display(text):
  header=["Press ESC to quit. Use the keys to navigate, or use the hotkeys:", "(h)ome, (e)nd, (n)ext, (p)revious, page_(u)p and page_(d)own"]
  nav={"home": "h", "end": "e", "next": "n", "prev": "p", "pg_up": "u", "pg_dn": "d"}
  screen = Specter()
  screen.start()
  screen.scroll(text, header=header, nav=nav)
  screen.stop()

def formatText(text):
  return text

if __name__=='__main__':
  description='''Query the Wikipedia data'''

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-db', metavar="path",      help='Location of the wikipedia sqlite db')
  parser.add_argument('act', metavar="action",    help='Action to take [(s)earch/(o)pen]')
  parser.add_argument('arg', metavar="argument",  help='Argument for action (title string for search, entry # for open')
  args = parser.parse_args()

  # Select DB
  if args.db: db = dbConnector(args.db); print("Using %s"%args.db)
  else:       db = dbConnector(conf.getDBLocation()); print("Using %s"%conf.getDBLocation())

  # Parse actions
  action = args.act.lower()
  if   action in ['s', 'search']: search(args.arg)
  elif action in ['o', 'open']:   open(args.arg)

