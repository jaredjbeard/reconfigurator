.. _markup:
=====================
Reconfigurator Markup
=====================

Reconfigurator is a tool for setting up and modify configuration files.
It has support for the following:
    - grouping together configurations of multiple modules,
    - setting default configurations and modification through both an API and command line interface,
    - a dense markdown for easily setting configurations or compressing data.
    - sampling configurations when used to set up experiments, and
    - setting default parameters.

On terminology, please note a *group* is a type of configuration, and a *configuration* is a set of parameters.

Basic Configuration
###################

At a fundamental level, configurations are organized into groups each containing a configuration or list of configurations. 
What's more, these configurations can be nested, so any markup described below will be called recursively whenever a dictionary is encountered (assuming it contains markdown directives described here).::

    {
        "group1": <val>, 
        "randomGroup name": [ {}, {}, ...], 
        371: [ {}, {}, ...], 
        ...
    }


If you wish to replacate a configuration you can include a `"n_copies" : <#copies>` to do so. 

If you wish to specify a default configuration, you can include a `"default" : {"var1": <val>, ... }` to do so.
This will be used to fill in any missing values in the configurations, however, if they exist internally, the specific values will overwrite the default case.

Stitching
*********

Stitching is the process of combining configurations from different groups. 
To define a stitch, users must include a key called stitch which contains the name of variables we want to stitch/compose into a set of configurations.
Stitch will be parse as follows:
    - a tuple: stitch variables as the component product (combination of the elements in the variable)
    - a list: stitch variables in a pairwise fashion (they will be matched one-to-one for each value in the variables which must be of the same length)
    - a key: parse variable sequentially. If the values contained in the member 
        - a dict: elements will be expanded as a normal
        - any other iterable: elements will be parse sequentially then be returned (or if dict, expanded)
        - any other type: elements will be returned as is 

What's more, pairwise and product stitching can be combined by nesting tuples and lists.
This is useful when you need to share some variables across trials, but also want to vary some others.

Please note, we use `NestifyDict <https://pypi.org/project/nestifydict/>`_ to find nested variables so you should only specify the deepest key and it will find them.
I apologize for any inconvencience this may cause. Where there are multiple of the sample keys, simply place these in nested configurations.

Product Example
---------------

Start with the configuration::

    {
        stitch : [ ( "a", "b" ) ],
        "a" : [1, 2],
        "b' : [4, 5]
    }


We would get::

    [
        {
            "a" : 1,
            "b" : 4
        },
        {
            "a" : 1,
            "b" : 5
        },
        {
            "a" : 2,
            "b" : 4
        },
        {
            "a" : 2,
            "b" : 5
        }
    ]


Pairwise Example
----------------
Start with the configuration::

    {
        stitch : [ ["a", "b"] ],
        "a" : [1, 2],
        "b' : [4, 5]
    }


We would get::

    [
        {
            "a" : 1,
            "b" : 4
        },
        {
            "a" : 2,
            "b" : 5
        }
    ]


Sequential Examples
-------------------
Start with the configuration::

    {
        stitch : [ "a", "b" ],
        "a" : [1, 2],
        "b' : [4, 5]
    }


We would get::

    [
        {
            "a" : 1,
            "b" : [4, 5]
        },
        {
            "a" : 2,
            "b" : [4, 5]
        }
        {
            "a" : [1, 2],
            "b" : 4
        },
        {
            "a" : [1, 2],
            "b" : 5
        }
    ]


Dictionary
^^^^^^^^^^
Start with the configuration::

    {
        stitch : [ ( "a", "b" ) ],
        "a" : 
            { "stitch" : ["c"],
                "c" : [1, 2]
                "d" : [3, 4]
            },    
        "b' : [4, 5]
    }


We end up with ::

    [
        {
            "a" : 
                { "c" : 1,
                "d" : [3, 4]
                },
            "b" : 4
        },
        {
            "a" : 
                { "c" : 1,
                "d" : [3, 4]
                },
            "b" : 5
        },
        {
            "a" : 
                { "c" : 2,
                "d" : [3, 4]
                },
            "b" : 4
        },
        {
            "a" : 
                { "c" : 2,
                "d" : [3, 4]
                },
            "b" : 5
        }
    ]


Other Iterables
^^^^^^^^^^^^^^^
Start with the configuration::

    {
        stitch : [ "a" ],
        "a" : [ 1, 
                {
                "c" : 
                    {
                        "stitch": "d", 
                        "d":[7,8]
                    }
                }, 
                3 ],  
        "b" : [4, 5]
    }


We end up with::

    {
        "a" : 1,
        "b" : [4, 5]
    },
    {
        "a" : 
            {
                "c" : 
                    {
                        "d" : 7
                    }
            },
        "b" : [4, 5]
    },
    {
        "a" : 
            {
                "c" : 
                    {
                        "d" : 8
                    }
            },
        "b" : [4, 5]
    },
    {
        "a" : 3,
        "b" : [4, 5]
    }


Other Types
^^^^^^^^^^^
Start with the configuration::

    {
        stitch : [ "a" ],
        "a" : 1,  
        "b" : [4, 5]
    }


We would end up with::

    {
        "a" : 1,
        "b" : [4, 5]
    }


Sample Configuration
####################

Let's say you want to to run Monte Carlo trials, you need some way to sample.
Doing so can tend to be quite case specific, but here we provide a basic framework for sampling configurations.
Begin by adding your variable key to `"stitch"` as you normally would. 
Within the `"default"` object, you can specify a `"sample"` key which will contain all variables we wish to sample.::

    "sample" : [ {}, {}, ... ]

Within the sample you should have a variable `"key"` with which you can specify where to place the sample.
This can be a nested key.

You can reference other variables in the configuration by replacing any value with a dictionary `{"ref": "key"}`.

We support three types of sampling: discrete, continuous, and incremented. 
Additionally, allow users to reference other variables as criteria.

Discrete Sampling
-----------------

To sample uniformly, you would specify the following::

    "sample" : 
    [
        {
            "key" : ["a", "b"],
            "choice": Options to sample from
            "probability": probability to sample from
            "num": (optional) number of times to sample
        }
    ]

Continuous and Incremental Sampling
-----------------------------------

To sample a continuous distribution, you would specify the following::

    "sample" : 
    [
        {
            "key" : ["a", "b"],
            "low": lower limit
            "high": upper limit
            "num_increments": (optional) number of increments to down sample a continuous space
            "num": (optional) number of times to sample
        }
    ]

If `num_increments` is not specified, the values will be sampled continuously.
