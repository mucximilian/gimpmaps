#! /usr/bin/env python
from gimpfu import *

def echo(*args):
  """Print the arguments on standard output"""
  print "Hello world"

register(
  "console_echo", "", "", "", "", "",
  "<Toolbox>/Scripts/Console Echo", "",
  [],
  [],
  echo
  )

main()