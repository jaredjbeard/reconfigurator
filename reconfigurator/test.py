import unittest

from markup import expand_to_list, expand_as_generator

def test_expand_to_list():
    config = {
        "default": {
            "a": 1,
            "b": 2
        },
        "n_copies": 2,
        "stitch": [
    #         ("a", "b"),
    #         ["c", "d"], 
            # "e", 
            "f",
            # "g"
        ],
    #     "c": 3,
    #     "d": 4,
        # "e": 
        # {
        #     "default": {
        #         "e1": 5,
        #         "e2": [6,7]
        #     },
        #     "n_copies": 2,
        #     "stitch": ["e2"]
        # },
        "f": [8,{"h":9}],
        "g": 10
    }
    for el in expand_to_list(config):
        print(el)

if __name__ == '__main__':
    test_expand_to_list()
