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
import argparse

import nestifydict as nd

RECONFIGURATOR_CONFIG_FILE = "config.json"

__all__ = ["replace_file", "merge_file" "update_file", "update", "print_config_file", "print_config"]

def replace_file(sink_file : str, source_file : str):
    """
    Replace one file with another

    :param sink_file: (str) location of new to write into
    :param source_file: (str) location of file to write from
    """
    with open(RECONFIGURATOR_CONFIG_FILE, "rb") as f:
        config = json.load(f)
        abs_path = config["abs_path"]
    with open(abs_path + source_file, "rb") as source:
        params = json.load(source)
    with open(abs_path + sink_file, "w+") as core_f:
        json.dump(params, core_f, indent = 4)
        
def merge_file(source_files : list, do_append : bool = False):
    """
    Accepts a list of configuration files and merges them into a single file. Last file will be destination

    :param source_files: (list(str)) Files to merge, if priority matters, later defaults will overwrite earlier ones.
    :param do_append: (bool) if true, iterables inside dictionaries will be merged as well, *default*: False
    """
    configs = []
    for fp in source_files:
        with open(fp, 'rb') as f:
            configs.append(json.load(f))
    
    with open(source_files[len(source_files)], "wb") as f:
        json.dump(nd.merge_all(configs, do_append), f)
        
def update_file(var, val, file : str, update_all : bool = False):
    """
    Update one or more config values in a file

    :param var: () parameter to update
    :param val: () new value of parameter
    :param file: (str) location of file
    :param update_all: (bool) if true, accepts var as a list of keys, *defualt*: False
    """
    with open(RECONFIGURATOR_CONFIG_FILE, "rb") as f:
        config = json.load(f)
        abs_path = config["abs_path"]
    with open(abs_path + file, 'r+') as f: 
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
    with open(RECONFIGURATOR_CONFIG_FILE, "rb") as f:
        config = json.load(f)
        abs_path = config["abs_path"]
    with open(abs_path + file, "rb") as f:
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
        
def set_abs_path(path : str = ""):
    """
    Sets the absolute path for config files.
    
    :param path: (str)
    """ 
    with open(RECONFIGURATOR_CONFIG_FILE, "r+") as f:
        data = json.load(f)
        data["abs_path"] = path
        json.dump(data,f)
        
def reset_abs_path():
    """
    Resets the absolute path for config files to relative path
    """ 
    set_abs_path()

if __name__=='__main__':  
    
    parser = argparse.ArgumentParser(description='Reconfigurator CLI')
    parser.add_argument('-p',  '--print',   type=str, nargs = 1, help='prints configuration from specified file')
    parser.add_argument('-s',  '--set',     type=str, nargs = 1, help='Sets absolute path to specified')
    parser.add_argument('-rs', '--reset',   type=str,            help='Reset absolute path to absolute')
    parser.add_argument('-r',  '--replace', type=str, nargs = 2, help='Replaces config file with another: Should specify sink_file source_file')
    parser.add_argument('-m',  '--merge',   type=str, nargs="+", help='Merges config files: Earlier files take precendence')
    parser.add_argument('-mr', '--merge-recursive',   type=str, nargs="+", help='Merges config files and iterables within them, last file will be destination')
    parser.add_argument('-u',  '--update',  type=str, nargs='+', help='Updates variables in a file: Should specify file key val key2 val2 ...')

    args = parser.parse_args()
    
    if hasattr(args, "print"):
        print_config_file(getattr(args,"print")[0])
    if hasattr(args, "setpath"):
        set_abs_path(getattr(args,"setpath")[0])
    if hasattr(args, "resetpath"):
        reset_abs_path()
    if hasattr(args, "replace"):
        replace_file(getattr(args,"replace")[0],getattr(args,"replace")[1])
    if hasattr(args, "merge"):
        merge_file(getattr(args,"merge"))  
    if hasattr(args, "merge-recrusive"):
        merge_file(getattr(args,"merge-recrusive"), True)  
    if hasattr(args, "update"):
        val = []
        var = []
        i = 1
        while i < len(args.update):
            val.append(getattr(args,"update")[i])
            val.append(getattr(args,"update")[i+1])
            i += 1
        update_file(val, var, getattr(args,"update")[0], True)


