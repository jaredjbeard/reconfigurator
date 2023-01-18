#!/usr/bin/python
"""
This script is intended to set default, visualize, and update decision making configuration.
"""
__license__ = "BSD-3"
__docformat__ = 'reStructuredText'
__author__ = "Jared Beard"

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import json

import nestifydict as nd

__all__ = ["replace_file", "update_file", "update", "print_config_file", "print_config"]

def replace_file(core_file : str, default_file : str):
    """
    Resets core configuration to defaults

    :param core_file: (str) location of core to overwrite, *default*: current + "/core.json"
    :param default_file: (str) location of default file to overwrite core, *default*: current + "/core_default.json"
    """
    with open(default_file, "rb") as default_f:
        params = json.load(default_f)
    with open(core_file, "w+") as core_f:
        json.dump(params, core_f, indent = 4)
        
def update_file(var, val, file : str, update_all : bool = False):
    """
    Update one or more config values in a file

    :param var: () parameter to update
    :param val: () new value of parameter
    :param file: (str) location of file
    :param update_all: (bool) if true, accepts var as a list of keys, *defualt*: False
    """
    with (file, 'r+') as f: 
        json.dump(update(var, val, json.load(f), update_all))  
        
def update(var, val, config : dict, update_all : bool = False):
    """
    Update one or more config values in a file

    :param var: () parameter to update
    :param val: () new value of parameter
    :param config: (dict) configuration
    :param update_all: (bool) if true, accepts var as a list of keys, *defualt*: False
    """
    if update_all:
        for key, v in zip(var, val):
            nd.recursive_set(key,v)
    elif isinstance(var,list):
        nd.recursive_set(var,val)
    else:
        config[var] = val 
    return config

def print_config_file(file : str): 
    """
    Prints configuration file settings
    
    :param file: (str) Location of configuration params
    """
    with open(file, "rb") as f:
        params = json.load(f)
        print_config(params)

            
def print_config(config : dict): 
    """
    Prints configuration
    
    :param config: (dict)configuration params
    """
    print("Getting Decision Making Toolbox Configuration")
    len_key = 0
    for key in config.keys():
        if len(str(key)) > len_key:
            len_key = len(str(key))
    len_key += 2
    for key in config.keys():
        print(f'{key:-<{len_key}} -> ' + str(config[key]))     

if __name__=='__main__':  
    
    if sys.argv[1] == "-p" or sys.argv[1] == "--print":
        print_config_file(sys.argv[2])
        
    elif sys.argv[1] == "-u":
        i = 3
        while i <= len(sys.argv) -2:
            update(sys.argv[i], sys.argv[i+1], False, sys.argv[2])
            i += 2
        
    else:
        print("Invalid Configuation Directive")
