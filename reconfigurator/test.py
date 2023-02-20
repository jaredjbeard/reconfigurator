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
            "envs": #[
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
                        ],
                    },
                    "params": {
                        "p": [0, 0.1],
                        "dimensions": [50, 50] 
                    }
                },
                # {
                #     "env": "irl_gym/Sailing-v0",
                #     "stitch": [{"combo": ["p"]}],
                #     "params": {
                #         "p": [0, 0.1]
                #     }
                # }
            #],
            "algs": [
                {
                    "alg": "aogs",
                },
                {
                    "alg": "gbop",
                }
            ]
        }
    for el in compile_as_generator(config):
        print(el)

if __name__ == '__main__':
    test_compile_to_list()
