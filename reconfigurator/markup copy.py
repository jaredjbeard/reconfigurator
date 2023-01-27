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
    # print(config)
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
                for el in stitch(stitch_config, config):
                    yield el

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
        for itm in stitch(el, deepcopy(configs)):
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
        # print(configs)
        """"""
        # d_filter = {}

        # for el in stitch_config:
        #     if el in configs:
        #         d_filter[el] = configs[el]

        # d_flat = nd.unstructure(configs)
        
        # for el in stitch_config:
        #     if el in d_flat:
        #         d_filter[el] = d_flat[el]

        """"""
        # d_flat = nd.unstructure(configs)
        # d_filter = {}
        # for el in stitch_config:
        #     d_filter[el] = d_flat[el]
        #     if not isinstance(d_filter[el], list):
        #             d_filter[el] = [d_filter[el]]

        keys = []
        vals = []
        for el in stitch_config:
            temp_key = nd.find_key(configs, el)
            keys.append(temp_key)
            temp_val = nd.recursive_get(configs, temp_key)
            if not isinstance(temp_val, list):
                temp_val = [temp_val]
            vals.append(temp_val)

        # Instead of doing the above options, do a find all and then lump these together. Use recursive set
        # Will need to test whether or not this can handle nested variables of the same name

        if isinstance(stitch_config,tuple):
            gen = itertools.product(vals)
        else:
            gen = pairwise(vals)

        for config in gen:
            # temp = dict(zip(list(d_filter.keys()), deepcopy(config)))
            # temp = nd.merge(d_flat,temp)
            for i, val in enumerate(config):
                nd.recursive_set(configs, keys[i], val)
            for itm in expand_as_generator(configs):
                yield itm
            # for itm in expand_as_generator(nd.structure(temp,configs)):
                # yield itm

    elif isinstance(configs[stitch_config],dict):
        for itm in expand_as_generator(configs[stitch_config]):
            temp = deepcopy(configs)
            temp[stitch_config] = itm
            yield temp

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

def pairwise(groups : Iterable):
    """
    Takes element from each group and pairs them together by index

    :param groups: (list) list of lists
    :return: (generator) yields all combinations
    """
    for i in range(len(groups[0])):
        els = [0]*len(groups)
        for j in range(len(groups)):
            els[j] = groups[j][i]
        yield els