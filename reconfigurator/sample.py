"""
This script is samples a set of variables and adds them to a configuration file
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

import numpy as np
from numpy import random

from collections.abc import Iterable

import nestifydict as nd

__all__ = ["from_file_to_file", "sample", "sample_all"]

def from_file_to_file(sample_file : str, save_file : str):
    """
    Samples variables for experiments
    
    :param sample_file: (str) Filename for sample params
    :param save_file: (str) Filename for saving params
    """
    f_sample = open(sample_file)
    f_save = open(save_file)
    
    sample_config = json.load(f_sample)
    save_output = json.load(f_save)
    
    f_sample.close()
    
    f_save.dump(sample_all(sample_config, save_output))
    f_save.close()
    
def sample_all(sample_config : dict, output : dict):
    """
    Sample configuration to an output dictionary
    
    Sampling uses `NestifyDict <https://pypi.org/project/nestifydict/>`_ so variables can be specified as their deepest key assuming this variable is only used in one place. 
    Otherwise the variable should be defined as a list.
    Nonexistent keys are skipped as the sampling declarations are contained here. 
    
    :param sample_config: (dict) Sample configuration
    :param output: (dict) Where to add samples
    """

    for i, el in enumerate(sample_config):
        # Replace references
        for param in el:
            if isinstance(el[param],dict) and "ref" in el[param]:
                sample_config[i][param] = deepcopy(nd.recursive_get(output,nd.find_key(output, el[param]["ref"])))
    
        s = sample(el)
                
        nd.recursive_set(output,el["key"],s)
    return output

def sample(sample_params : dict):
    """
    Samples variables using specification
    
    **Note** For those using `from_file_to_file` or `sample_all`,
    sample params can be specified with the string key of another variable and it will be replaced with a copy of that value.
    Additionally, samples can be multi-dimensional
    
    :params sample_params: (dict) Contains sample parameters as follows::
        
        Continous sample
        {
            "low": lower limit
            "high": upper limit
            "num_increments": (optional) number of increments to down sample a continuous space
            "num": (optional) number of times to sample
        }
        
        Discrete sample
        {
            "choice": Options to sample from
            "probability": probability to sample from
            "num": (optional) number of times to sample
        }
    
    :returns: (list) sampled values
    """
    rng = random.default_rng()
    
    if "choice" in sample_params:
        return sample_discrete(rng, sample_params)
    elif "low" in sample_params:
        return sample_continuous(rng, sample_params)
    return None
        
def sample_continuous(rng, params):
    """
    Samples one or more continuous distributions
    
    :param rng: (rng) random number generator
    :param params: (dict) params to sample dist of the form::
    
        {
            "low": lower limit
            "high": upper limit
            "num_increments": (optional) number of increments to down sample a continuous space (+1 will use unit increments)
            "num": (optional) number of times to sample
        }
        
    :return: list of samples
    """    
    if "num" not in params:
        params["num"] = 1   
    if "num_increments" in params and params["num_increments"] is not None:
        if isinstance(params["num_increments"], str) and params["num_increments"] == "+1":
            params["num_increments"] = recursive_increment(params)
        if not isinstance(params["num_increments"], Iterable):
            params["num_increments"] = recursive_update(params)
        
        num = params["num"]
        del params["num"]
        samples = []
        if num == 1:
            return recursive_discrete(rng, params)
        for i in range(num):
            samples.append(recursive_discrete(rng, params))
        return samples
    else:
        num = params["num"] if "num" in params else None
        vals = rng.random(num)
        return list((np.asarray(params["high"])-np.asarray(params["low"]))*vals + np.asarray(params["low"]))

def recursive_increment(params):
    """
    Recursively sets the increments for a continuous space to unit increments
    
    :param params: (dict) params to sample dist of the form::
    
        {
            "low": lower limit
            "high": upper limit
        }
    """
    incs = []
    for i in range(len(params["low"])):
        if isinstance(params["low"][i], Iterable):
            temp = []
            for j in range(len(params["low"][i])):
                temp.append(recursive_increment({"low": params["low"][i], "high": params["high"][i]}))
            incs.append(temp)
        else:
            incs.append(params["high"][i]-params["low"][i]+1)
    return incs

def recursive_update(params):
    """
    Recursively sets the increments for a continuous space to unit increments
    
    :param params: (dict) params to sample dist of the form::
    
        {
            
            "low": lower limit
            "high": upper limit
        }
    """
    incs = []
    for i in range(len(params["low"])):
        if isinstance(params["low"][i], Iterable):
            temp = []
            for j in range(len(params["low"][i])):
                temp.append(recursive_update({"low": params["low"][i], "high": params["high"][i], "num_increments": params["num_increments"]}))
            incs.append(temp)
        else:
            incs.append(params["num_increments"])
    return incs

def recursive_discrete(rng, params):
    """
    Resursively samples discrete distributions
    
    :param rng: (rng) random number generator
    :param params: (dict) params to sample dist of the form::
    
        {
            "low": lower limit
            "high": upper limit
            "num_increments": (optional) number of increments to down sample a continuous space
            "num": (optional) number of times to sample
        }
    :return: list of samples
    """
    sample = []
    for i in range(len(params["low"])):
        if isinstance(params["low"][i], Iterable):
            temp = []
            for j in range(len(params["low"][i])):
                temp.append(recursive_increment({"low": params["low"][i], "high": params["high"][i], "num_increments": params["num_increments"][i]}))
            sample.append(temp)
        else:
            temp = {"num": 1}
            temp["choice"] = np.linspace(params["low"][i], params["high"][i], params["num_increments"][i])
            sample.append(sample_discrete(rng,temp)[0])
    return sample        

def sample_discrete(rng, params):
    """
    Samples one or more discrete distributions
    
    :param rng: (rng) random number generator
    :param params: (dict) params to sample dist of the form::
    
        {
            "choice": Options to sample from
            "probability": probability to sample from
            "num": (optional) number of times to sample
        }
        
    :return: list of samples
    """
    num = params["num"] if "num" in params else None
    p = params["probability"] if "probability" in params else None
    return list(rng.choice(params["choice"], num, replace = True, p = p))

def filter(self):
    """
    Not Implemented... Perhaps add in later version
    """
    pass

if __name__=='__main__':
    sample_config_file = sys.argv[1]
    save_config_file = sys.argv[2]
    
    sample_config_file = parent + "/config/" + sample_config_file +  ".json"
    save_config_file = parent + "/config/" + save_config_file +  ".json"

    from_file_to_file(sample_config_file, save_config_file)
    
