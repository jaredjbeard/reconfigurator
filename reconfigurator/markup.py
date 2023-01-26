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
            if isinstance(stitch_config,list):
                for el in stitch_all(stitch_config, config):
                    yield el 
            else:
                yield stitch(stitch_config, config)         

def push_default(default_config: dict, config : dict):
    """
    Distributes default settings to dictionary
    
    :param default_config: (dict) configuration file defaults
    :param config: (dict) configuration file
    :return: (dict) configuration file with defaults
    """
    temp_stitch = ()
    if "sample" in default_config:
        s = default_config.pop("sample")
        default_config = sample.sample_all(s, default_config)
        config["stitch"].append(temp_stitch)
    return nd.merge(default_config,config)

def stitch_all(stitch_configs : dict, configs : dict):
    """
    Generator that will stitch together expanded configurations.
    Stitch should be specified as a list. If the element encountered is
    
    :param stitch_config: (list) how to stitch together configurations
    :param config: (dict) dense configuration
    :return: yields all combinations. 
    """
    for el in stitch_configs:
        for itm in stitch(el, configs):
            yield itm      

def stitch(stitch_config, configs : dict):
    """
    Generator that will stitch together expanded configurations.
    
    Stitch should be specified as a list. If the element encountered is 
    - a tuple -> the product of all elements in tuple will be expanded
    - a list  -> a pairwise arrangement of elements will be expanded
    - a dict  -> this will be expanded directly
    - else    -> the element will be yielded
    
    :param stitch_config: () how to stitch together configurations
    :param config: (dict) dense configuration
    :return: yields all combinations. 
    """
    if isinstance(stitch_config,tuple) or isinstance(stitch_config,list):
        # d_flat = nd.unstructure(configs)
        # d_filter = {}
        # for el in stitch_config:
        #     d_filter[el] = d_flat[el]

        # if isinstance(stitch_config,tuple):
        #     for stitch_config in d_filter:
        #         if not isinstance(d_filter[stitch_config], Iterable):
        #             d_filter[stitch_config] = [d_filter[stitch_config]]
        #     gen = itertools.product(*d_filter.values())
        # else:
        #     gen = itertools.pairwise(d_filter.values())

        # for config in gen:
        #     temp = dict(zip(list(d_filter.keys()), deepcopy(config)))
        #     temp = nd.merge(d_flat,temp)
        #     yield expand_as_generator(nd.structure(temp,configs))
        yield 1
    elif isinstance(configs[stitch_config],dict):
        yield 2
        # yield expand_as_generator(configs[stitch_config])
    elif isinstance(configs[stitch_config],Iterable):
        for el in configs[stitch_config]:
            temp = deepcopy(configs)
            if isinstance(el,dict):
                for itm in expand_as_generator(el):
                    temp[stitch_config] = itm
                    yield temp
            else:
                temp[stitch_config] = el
                yield temp
    else:
        yield configs

