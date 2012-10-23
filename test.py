#!/usr/bin/env python
import sys, os
import web
from urlparse import urlparse, parse_qsl

try:
    import mymodel
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    try:
        import mymodel
    finally:
        sys.path.remove(os.path.dirname(__file__))

def do_stuff():
	#we are going to run some test of the mymodel module here
	mymodel.get_score("9366451048")
	mymodel.get_score("9366451048",1)

if __name__ == "__main__":
	do_stuff()
