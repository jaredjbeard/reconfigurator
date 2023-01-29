import unittest

from expand import expand_to_list, expand_as_generator

def test_expand_to_list():
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
        "stitch": [
            ("a", "b"),
        ],
        "a": 
        {
            "default": {
                "a1": 1,
                "a2": [2,3]
            },
            "stitch": ["a2"]
        },
        "b": 
        {
            "default": {
                "b1": [4,5],
                "b2": [6,7]
            },
            "stitch": [("b1", "b2")]
        },
    }
    for el in expand_to_list(config):
        print(el)

if __name__ == '__main__':
    test_expand_to_list()
