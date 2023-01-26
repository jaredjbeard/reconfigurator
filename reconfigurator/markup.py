#!/usr/bin/python
"""
This script contains functions related to getting sets of configurations, particularly for use in experiments.
"""
__license__ = "BSD-3"
__docformat__ = 'reStructuredText'
__author__ = "Jared Beard"

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import itertools
from collections.abc import Iterable
from copy import deepcopy

import nestifydict as nd

import sample

__all__ = ["merge_configs", "merge_configs_from_file"]

RECONFIG_ARGS = ["merge", "default", "sample-control", "configs"]
    
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
    default_config = {}
    if "default" in config:
            default_config = config.pop("default")   
    config = push_default(default_config, config)
    
    n_copies = 1
    if "n_copies" in config:
            n_copies = config.pop("n_copies")
    
    if "stitch" not in config:
        for i in range(n_copies):
            yield config
    else:
        stitch_config = config.pop("stitch")
        
        for i in range(n_copies):
            for el in stitch(stitch_config, config):
                yield el          

def push_default(default_config: dict, config : dict):
    """
    Distributes default settings to dictionary
    
    :param default_config: (dict) configuration file defaults
    :param config: (dict) configuration file
    :return: (dict) configuration file with defaults
    """
    if "sample" in default_config:
        s = default_config.pop("sample")
        default_config = sample.sample_all(s, default_config)
    return nd.merge(default_config,config)        

def stitch(stitch_config : dict, configs : dict):
    """
    Generator that will stitch together expanded configurations.
    
    Stitch should be specified as a list. If the element encountered is 
    - a tuple -> the product of all elements in tuple will be expanded
    - a list  -> a pairwise arrangement of elements will be expanded
    - a dict  -> this will be expanded directly
    - else    -> the element will be yielded
    
    :param stitch_config: (list) how to stitch together configurations
    :param config: (dict) dense configuration
    :return: yields all combinations. 
    """
    for el in stitch_config:
        if isinstance(el,tuple) or isinstance(el,list):
            d_flat = nd.unstructure(configs)
            d_filter = {}
            for itm in el:
                d_filter[itm] = d_flat[itm]

            if isinstance(el,tuple):
                for el in d_filter:
                    if not isinstance(d_filter[el], Iterable):
                        d_filter[el] = [d_filter[el]]
                gen = itertools.product(*d_filter.values())
            else:
                gen = itertools.pairwise(d_filter.values())

            for config in gen:
                temp = dict(zip(list(d_filter.keys()), deepcopy(config)))
                temp = nd.merge(d_flat,temp)
                yield expand_as_generator(nd.structure(temp,configs))
        elif isinstance(configs[el],dict):
            yield expand_as_generator(configs[el])
        elif isinstance(configs[el],Iterable):
            for itm in configs[el]:
                if isinstance(itm,dict):
                    yield expand_as_generator(itm)
                else:
                    yield itm
        else:
            yield configs[el]

