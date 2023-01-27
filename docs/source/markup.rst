=====================
Reconfigurator Markup
=====================

Reconfigurator Markup is a tool for providing shorthand descriptions of configurations.
It has support for the following:
    - grouping together configurations of multiple modules,
    - setting default configurations and modification through both an API and command line interface,
    - a dense markdown for easily setting configurations or compressing data.
    - (pending) sampling configurations when used to set up experiments, and
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


If you wish to replicate a configuration you can include a `"n_copies" : <#copies>` to do so. 

Stiching
********

Stitching is the process of combining configurations from different groups. 
To define a stitch, users must include a key called stitch which contains the name of variables we want to stitch/compose into a set of configurations.
Stitch will be parse as follows:
    - a tuple: stitch variables as the component product (combination of the elements in the variable)
    - a list: stitch variables in a pairwise fashion (they will be matched one-to-one for each value in the variables which must be of the same length)
    - a key: parse variable sequentially. If the values contained in the member 
        - a dict: elements will be expanded as a normal
        - any other iterable: elements will be parse sequentially then be returned (or if dict, expanded)
        - any other type: elements will be returned as is 

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


.. Sample Configuration
.. ####################

.. ```
.. {
..     {
..         "group1" : {},
..         "randomGroup name": {},
..         371: {},
..         ...
..     }, 
..     {
..         "group1" : {},
..         "randomGroup name": {},
..         371: {},
..         ...
..     }, 
..     ...
.. }
.. ```

.. Talk about stitch!-> do a list, only things in list will be added (add flag to just do everythiing unlisted too?)
..     "stitch":
..     [
..         "parallel": [],
..         "combo":
..             [
..                 itm, 
..                 {"pairwise":
..                 [

..                 ]}
..             ]
..     ]

.. "sample-control":
..     {
..         [{}, ...] # Sample all variables. Add them to pairwise. Add them to source destination
..             #not supporting with combo or pairwise as dimensions are weird and behavior can't be guaranteed
..             # Then n-copies can gerenate more of them.
..     }
.. "default": 
.. {
..     "default": True
    
..     "n_copies": <#>
..     "sample": [{}, {}]
..     "var": ...,
..     "var2": ...
.. }
.. "values": []

.. Sample dicts should look like:
.. {
..     "key": ["", ""]
..     "merge": "<merge type>"
..     "params":
.. }
.. If key contains all, then it will be added to all sub levels

.. # Expand will push 
.. Assume that shared 

.. #Alg will check for values, merge, default or sample

.. A configuration file will consist of a dictionary containing the following elements:
..     - "default": (optional) default parameters for all algorithms or environments under test. These will be overwritten by more specific described below.

.. Users should also specify either other of below:
..     - "algs": A list of algorithms with their specific parameters
..     - "envs": A list of environments with their specific parameters
.. These should be kept in their own files. 

.. ```
.. {
..     "default": 
..         {
..             ...,
..             "sample" : #(optional, see below)
..             {

..             },
..         },
..     "algs" :
..         {
..             [{}, {}, {}]
..         }
.. }
.. ```

.. Sampling Parameters
.. ###################

.. Users may wish to sample variables when running several experiments. 
.. As described above sampling may be specified in 
..     - "default" : Here a single sample is drawn for each variable every trial and will not cannot be combined with other variables
..     - "alg" or "env" : Here samples are drawn as lists, overwritting sample commands from default, and maybe be combined with other features for experiment generation.

.. Variables to be sampled are captured with a list as follows:
.. ```
.. "sample : [ "var1", "var2", ...]
.. ```

.. Within "default" or with each "alg"/"env", the corresponding variable should contain a dictionary rather than a single instance of the variable.
.. The dictionary will contain the information necessary to sample as desired. 
.. For example, discretely sampling "var1" would look something like:

.. ```
.. {
..     "alg": alg1,
..     "params": 
..     {
..         "var1":
..         {
..             "choice": [1,2,3]
..         }
..     }
.. }
.. ```

.. Sampling uses `NestifyDict <https://pypi.org/project/nestifydict/>`_ so variables can be specified as their deepest key assuming this variable is only used in one place. 
.. Otherwise the variable should be defined as a list.

.. Further detail on specifying samples can be found in :ref:`Sampler <sampler>`.