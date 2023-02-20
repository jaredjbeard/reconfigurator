import unittest

from compiler import compile_to_list, compile_as_generator

def test_compile_to_list():
    # config = {
    #     "default": {
    #         "a": [1, 2],
    #         "b": [3, 4]
    #     },
    #     "n_copies": 2,
    #     "stitch": [
    #         ("a", "b", "c"),
    #         ["a", "b"],
    #         ["c", "d"], 
    #         "e", 
    #         "f",
    #         "g"
    #     ],
    #     "c": 3,
    #     "d": 4,
    #     "e": 
    #     {
    #         "default": {
    #             "e1": 5,
    #             "e2": [6,7]
    #         },
    #         "n_copies": 2,
    #         "stitch": ["e2"]
    #     },
    #     "f": [8,{"h":9}, [10,11], 12],
    #     "g": 13
    # }
    config = {
            "stitch" : [{"combo": ["algs", "envs"]}],
            "envs": [
                {
                    "env": "irl_gym/GridWorld-v0",
                    "stitch": [{"combo": ["p"]}],
                    "default" : {
                        "sample" : [
                            {
                                "key": ["params", "state", "pose"],
                                "low": [0, 0],
                                "high": {"ref":"dimensions"},
                                "num_increments": "+1"
                            },
                            {
                                "key": ["params", "goal"],
                                "low": [0, 0],
                                "high": {"ref":"dimensions"},
                                "num_increments": "+1"
                            },
                        ],
                    },
                    "params": {
                        "max_time": 100,
                        "r_radius": 5,
                        "render": "none",
                        "cell_size": 50,
                        "save_frames": False,
                        "log_level": "WARNING",
                        "p": [0, 0.1],
                        "dimensions": [50, 50],
                        "r_range": [-0.01, 1 ],
                    }
                },
                {
                    "env": "irl_gym/Sailing-v0",
                    "stitch": [{"combo": ["p"]}],
                    "default" : {
                        "sample" : [
                            {
                                "key": ["params", "state", "pose"],
                                "low": [0, 0],
                                "high": {"ref":"dimensions"},
                                "num_increments": "+1"
                            },
                            {
                                "key": ["params", "goal"],
                                "low": [0, 0],
                                "high": {"ref":"dimensions"},
                                "num_increments": "+1"
                            },
                        ],
                    },
                    "params": {
                        "max_time": 100,
                        "r_radius": 5,
                        "render": "none",
                        "cell_size": 50,
                        "save_frames": False,
                        "log_level": "WARNING",
                        "p": [0, 0.1],
                        "dimensions": [40, 40],
                        "r_range": [-400, 1100 ],
                    }
                },
            ],
            "algs": [
                {
                    "alg": "aogs",
                    "stitch" : [{"combo": ["max_samples", "alpha"]}],
                    "params" :
                    {
                        "max_iter": 6000.0,
                        "gamma": 0.95,
                        "max_graph_size": 50000.0,
                        "rng_seed": 45,
                        "model_accuracy": 
                        {
                            "epsilon": 0.2,
                            "delta": 0.1
                        },
                        "action_selection": 
                        {
                            "function": "ambiguity_aware",
                            "params": {
                                "alpha": [ 0, 0.05, 1, 0.25, 0.5, 0.75, 0.9, 0.95, 1]
                            }
                        }
                    },
                    "search": 
                    {
                        "max_samples": [
                            500,
                            1000.0,
                            5000.0
                        ],
                        "horizon": 50,
                        "timeout": 5,
                        "reinit": True
                    }
                },
                {
                    "alg": "gbop",
                    "stitch" : [{"combo": ["max_samples", "alpha"]}],
                    "params" : {
                        "max_iter": 6000.0,
                        "gamma": 0.95,
                        "max_graph_size": 50000.0,
                        "rng_seed": 45,
                        "model_accuracy": 
                        {
                            "epsilon": 0.2,
                            "delta": 0.1
                        },
                        "action_selection": {
                            "bound_function": "gbop_dm",
                            "bound_params": {},
                            "move_function": "gbop_best_action",
                            "move_params": {
                                "alpha": [ 0, 0.05, 1, 0.25, 0.5, 0.75, 0.9, 0.95, 1]
                            }
                        }
                    },
                    "search": {
                        "branch_factor_s": 4,
                        "branch_factor_a": 4,
                        "max_samples": [
                            500,
                            1000.0,
                            5000.0
                        ],
                        "horizon": 50,
                        "timeout": 5,
                        "reinit": True
                    }
                }
            ]
        }
    for el in compile_as_generator(config):
        print(el)

if __name__ == '__main__':
    test_compile_to_list()
