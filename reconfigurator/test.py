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
            ("a", "b"),
            ["c", "d"]
        ],
        "c": 3,
        "d": 4
    }
    expected_output = [
        {"a": 1, "b": 2, "c": 3, "d": 4},
        {"a": 1, "b": 2, "c": 3, "d": 4}
    ]
    print(expand_to_list(config))

if __name__ == '__main__':
    test_expand_to_list()
