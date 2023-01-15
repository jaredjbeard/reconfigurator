#!/usr/bin/python
"""
This file contains methods to stitch together different configs.
"""
__license__ = "BSD-3"
__docformat__ = 'reStructuredText'
__author__ = "Jared Beard"

from copy import deepcopy
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class Stitch():

    __init__ if declared with variable will add and compile
    add_stitch - > adds to a queue
    compile -> will merge in parallel 