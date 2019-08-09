from modules.handlers.todo import TodoHandler
from modules.handlers.pizza import PizzaHandler
from modules.handlers.stats import StatsHandler
from modules.handlers.subscription import SubscriptionHandler


class MessageHandler:
    commands = {
        '#todo': TodoHandler,
        '#pizza': PizzaHandler,
        '#stats': StatsHandler,
        '#subscribe': SubscriptionHandler
    }

    def __init__(self, message, rtm_client_helper):
        tokens = [token.strip() for token in message.split(' ')]
        if is_valid_command(tokens):
            MessageHandler.commands[tokens[0]](
                tokens[1:],
                rtm_client_helper)


def is_valid_command(tokens):
    if len(tokens) == 0:
        return False
    return tokens[0] in MessageHandler.commands.keys()
