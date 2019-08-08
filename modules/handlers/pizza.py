"""Toppings array: [origin_index,topping_name,is_meat]
"""
import random
import json

from modules.helpers import rtm_client_helper

USAGE_TIPS = "Usage:\n#pizza number-of-toppings [-v|-m]"

DEFAULT_PIZZA_JOINT = "panago"
DEFAULT_SOURCE = "data/pizza.{}.json"
DEFAULT_PREFERENCE_FLAG = None

MINIMUM_TOPPINGS = 1
MAXIMUM_TOPPINGS = 8

CRUST_KEY = 'crust'
SAUCE_KEY = 'sauce'
TOPPINGS_KEY = 'toppings'


class PizzaHandler:
    def __init__(self, tokens, **rtm_client_with_channel):
        """
        Not fully implemented. Only lists toppings and responds to #pizza and #pizza number-of-toppings
        :param tokens: array of string tokens
        :param rtm_client_with_channel: dict of client and channel
        """
        self.number_of_toppings = get_random_int(MINIMUM_TOPPINGS, MAXIMUM_TOPPINGS)
        self.pizza_joint = DEFAULT_PIZZA_JOINT
        self.topping_preference_flag = DEFAULT_PREFERENCE_FLAG
        self.rtm_client_with_channel = rtm_client_with_channel

        commands = {
            int: self.randomize_pizza_toppings
        }

        if len(tokens) == 0:
            tokens = [self.number_of_toppings]

        cast_type = get_cast_type(tokens[0], commands.keys())

        if cast_type is None:
            self.send_usage_tips()
        else:
            commands[cast_type].__call__(tokens)

    def randomize_pizza_toppings(self, tokens):
        self.number_of_toppings = int(tokens[0])

        if MINIMUM_TOPPINGS <= self.number_of_toppings <= MAXIMUM_TOPPINGS:
            if len(tokens) > 1:
                self.topping_preference_flag = tokens[1]
            self.handle_pizza()
        else:
            rtm_client_helper.send_message(self.rtm_client_with_channel,
                                           f"Minimum toppings: {MINIMUM_TOPPINGS}\nMaximum toppings: {MAXIMUM_TOPPINGS}")

    def handle_pizza(self):
        j = json.load(open(DEFAULT_SOURCE.format(self.pizza_joint), 'r', encoding='utf8'))

        crust = get_random_element(j, CRUST_KEY)
        sauce = get_random_element(j, SAUCE_KEY)
        toppings = [get_random_element(j, TOPPINGS_KEY) for i in range(self.number_of_toppings)]

        rtm_client_helper.send_message(self.rtm_client_with_channel,
                                       f"How about a:\n"
                                       f"{crust} with {sauce}\n"
                                       f"And the toppings:\n{format_pizza_toppings(toppings)}")

    def send_usage_tips(self):
        rtm_client_helper.send_message(self.rtm_client_with_channel,
                                       USAGE_TIPS)


def format_pizza_toppings(toppings):
    def format_extras(_kv):
        prefix = " ".join(["Extra" for i in range(_kv[1] - 1)])
        return f"{prefix} {_kv[0]}".strip()

    already_counted = {}
    for topping in [t[1] for t in toppings]:
        if topping in already_counted.keys():
            already_counted[topping] += 1
        else:
            already_counted[topping] = 1
    ret = ""
    for i, kv in enumerate(already_counted.items()):
        ret += f"{i + 1}) {format_extras(kv)}\n"
    return ret


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
