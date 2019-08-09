import json
import random


def get_random_int(inclusive_minimum, inclusive_maximum):
    return random.randint(inclusive_minimum, inclusive_maximum)


def get_random_element(some_dict, key_of_array):
    return some_dict[key_of_array][get_random_int(0, len(some_dict[key_of_array]) - 1)]


def get_cast_type(arg, types):
    for t in types:
        try:
            t(arg)
            return t
        except ValueError:
            pass
    return None


def read_json(path_and_filename):
    return json.load(open_file_for_read(path_and_filename))


def write_json(path_and_filename, json_to_write):
    json.dump(json_to_write, open_file_for_write(path_and_filename))


def open_file_for_read(path_and_filename):
    return open(path_and_filename, 'r', encoding='utf8')


def open_file_for_write(path_and_filename):
    return open(path_and_filename, 'w+', encoding='utf8')
