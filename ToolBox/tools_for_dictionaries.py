from collections import defaultdict
import json

dict_names = {'d1': {'name': 'bob', 'place': 'lawn', 'animal': 'man'},
              'd2': "doggggyy"}


def copy_and_clear_values_of_2d_dict(two_dimensional_dict: dict):
    tree = lambda: defaultdict(tree)
    some_dict = tree()
    for i in two_dimensional_dict:
        some_dict[i]
        if type(two_dimensional_dict.get(i)) == dict:
            nested_dict = two_dimensional_dict.get(i)
            for j in nested_dict:
                some_dict[i][j] = None
    return json.dumps(some_dict)


def clear_2d_dict(some_dict: dict):
    for i in some_dict:
        if type(some_dict.get(i)) == dict:
            nested_dict = some_dict.get(i)
            for j in nested_dict:
                some_dict[i][j] = None
        else:
            some_dict[i] = None
    return some_dict




#clear_2d_dict = clear_2d_dict(dict_names)

if __name__ == "__main__":
    print(clear_2d_dict(dict_names))
