from modules.handlers.todo import TodoHandler
from modules.handlers.pizza import PizzaHandler

from modules.helpers import rtm_client_helper


class MessageHandler:
    commands = {
        '#todo': TodoHandler,
        '#pizza': PizzaHandler
    }

    def __init__(self, message, **rtm_client_with_channel):
        tokens = message.split(' ')
        try:
            MessageHandler.commands[tokens[0]]([token for i, token in enumerate(tokens) if i > 0],
                                               client=rtm_client_with_channel['client'],
                                               channel=rtm_client_with_channel['channel'])
        except KeyError:
            rtm_client_helper.send_message(rtm_client_with_channel,
                                           "Sorry! That command is not supported!")
            rtm_client_helper.send_message(rtm_client_with_channel,
                                           f"Here's a list of supported commands: \n"
                                           f"{', '.join(MessageHandler.commands.keys())}")
