from modules.handlers.todo import TodoHandler
from modules.handlers.pizza import PizzaHandler
from modules.handlers.stats import StatsHandler


class MessageHandler:
    commands = {
        '#todo': TodoHandler,
        '#pizza': PizzaHandler,
        '#stats': StatsHandler
    }

    def __init__(self, message, **rtm_client_with_channel):
        tokens = message.split(' ')
        if is_valid_command(tokens):
            MessageHandler.commands[tokens[0]](
                [
                    token
                    for i, token in enumerate(tokens)
                    if i > 0
                ],
                client=rtm_client_with_channel['client'],
                channel=rtm_client_with_channel['channel'])


def is_valid_command(tokens):
    if len(tokens) == 0:
        return False
    return tokens[0] in MessageHandler.commands.keys()
