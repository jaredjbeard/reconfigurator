#!/usr/bin/python3
"""
This file supports functionality for aliasing reconfigurator commands
"""
__license__ = "BSD-3"
__docformat__ = 'reStructuredText'
__author__ = "Jared Beard"

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

__all__ = []

class Alias():
    """
    This class supports aliases provided by a user. 

    Users should specify 
    """