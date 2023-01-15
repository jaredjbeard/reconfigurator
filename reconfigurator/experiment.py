#!/usr/bin/python
"""
This script contains functions related to getting sets of configurations, particularly for use in experiments.
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

import json
from collections.abc import Iterable
import nestifydict as nd

import ABC
from dataclasses import dataclass

import sampler
import stitch

__all__ = ["merge_configs", "merge_configs_from_file"]

RECONFIG_ARGS = ["merge", "default", "sample-control", "configs"]


def merge_configs(configs : list):
    """
    Accepts a list of configuration files and merges them into a single file

    :param source_files: (list(str)) Files to merge, if priority matters, later defaults in each group will overwrite earlier ones.
    :return: merged configuration
    """
    merged_config = {}
    for c in configs:
        merged_config = nd.merge(merged_config,c,True)

    return merged_config

def merge_configs_from_file(source_files : list, destination_file : str):
    """
    Accepts a list of configuration files and merges them into a single file

    :param source_files: (list(str)) Files to merge, if priority matters, later defaults will overwrite earlier ones.
    :param destionation_file: (str) Where to save merged configuration
    """
    configs = []
    for fp in source_files:
        with open(fp, 'rb') as f:
            configs.append(json.load(f))
    
    with open(destination_file, "wb") as f:
        json.dump(merge_configs(configs), f)
    
def expand_to_list(config : dict):
    """
    Expands dense configuration to get list of all sets of configurations
    
    :param config: (dict) dense configuration file
    :return: (list) all configurations captured
    """
    return list(expand_as_generator(config))
    

def expand_as_generator(config : dict):
    """
    Expands dense configuration using a generator to get all sets of configurations
    
    :param config: (dict) dense configuration file
    :return: (dict) a single configuration
    """
    if "merge" not in config:
        yield config
    else:
        default_config = {}
        sample_control_config = []
        values_config = []
        n_samples = 1
        
        if "default" in config:
            default_config = config.pop("default")      
        if "sample_control" in config:
            sample_control_config = config.pop("sample_control")      
        if "values" in config:
            values_config = config.pop("values")
        if "n_samples" in config:
            n_samples = config.pop("n_samples")
            
        stitch_config = config.pop("stitch")
        
        config = sample_control(sample_control_config, default_config)

        config = push_default(default_config)
            
            
        # default_config = sample_config(sample_control, "default")
            #sample each control
            # add to corresponding stitch in default
            # add values to default
        
        for i in n_samples:
            for el in stitch_config: 
                if isinstance(el,set):
                    pass
                elif isinstance(el,tuple):
                    pass
                elif isinstance(el,list):
                    for itm in stitch_config[el]:
                        #distribute
                        # sample internals
                        yield expand_as_generator(stitch_config[el])
                else:
                    #distribute defaults
                    #sample internals
                    yield expand_as_generator(stitch_config[el])
        # for el in config
            #config[el] = distribute defaults(config[el],default_config)
                # add sample to sample control??
                #? if not isinstrance(config[el], list):
                    #?????
                #? else:
                    #? apply defaults to each el in list
            
        # for i in n_samples:  
            # config_list = values_config
            # for el in config:
                # if not isinstance(config[el], list):
                    # yield expand()
                # else
                    # for itm in config[el]:
                        #yield itm

def sample_control(sample_config : dict, default_config : dict):
    """
    Samples control variables and adds them to subdictionary defaults

    :param sample_config: (dict) Variable sample declarations
    :param default_config: (dict) Default config to write sampled values to
    """
    sampler.sample_all(sample_config, default_config)
    if "stitch" not in default_config:
        default_config["stitch"] = stitch.Stitch()
    elif isinstance(default_config["stitch"], stitch.Stitch):
        default_config["stitch"] = stitch.Stitch(default_config["stitch"])


    for el in sample_config:
        #adds a stitch to the buffer
        default_config["stitch"].add_stitch(sample_config[el]["stitch"], sample_config[el]["key"])

    default_config.compile_stitch("unordered")
    

    #Get sample keys and and add them to "stitch " as combo
            # else for each el in configs, 
            #   update with first key replaced
            #   then inside if they contain "stitch" add in appropriate manner
    
    
def distribute_defaults(config : dict):
    """
    Distributes default settings to constituent members
    
    :param config: (dict) configuration file
    """
    if "default" in config:
        config_default = config.pop("default")
        for el in config:
            
            
    
    
    pass

def stitch(configs : dict):
    """
    Integrates all groups of configurations.
    By default, groups are stitchd by generating combinations of the elements in each group.
    Users can make this explicit by using a "stitch" key which has two possible values.
        - "combo" which generations combinations
        - "pairwise" which will stitch together elements from each as pairs. (A blank or default will be used if they are of different lengths)
        - "parallel" which will treat configured groups as unrelated 
    Following a stitch, elements will be stitched together using their group name as a dictionary key for each configuration.

    :param configs: (dict) list of configurations to stitch
    :return: (list(dict)) list of configurations 
    """
    
    
    pass

def combo_stitch():
    pass

def pairwise_stitch():
    pass

def parallel_stitch():
    pass

def condense_trials():
    pass

def compress_to_dict():
    pass

