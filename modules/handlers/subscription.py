from modules.helpers import common_helper as ch

DEFAULT_SOURCE = 'data/subscription.users.json'
DEFAULT_COMMAND = 'subscribe_to_dm'
DEFAULT_USERS_KEY = 'users'
DEFAULT_SUBSCRIPTION = {DEFAULT_USERS_KEY: {}}
DEFAULT_DM_PREFIX = 'D'


class SubscriptionHandler:
    def __init__(self, tokens, rtm_client_helper):
        self.rtm_client_helper = rtm_client_helper
        if len(tokens) == 0:
            tokens = [DEFAULT_COMMAND]

        commands = {
            'subscribe_to_dm': self.subscribe_to_dm
        }

        if tokens[0] in commands.keys():
            commands[tokens[0]].__call__(tokens[1:])

    def subscribe_to_dm(self, trailing_tokens):
        if self.rtm_client_helper.channel[0] == DEFAULT_DM_PREFIX:
            j = ch.read_json(DEFAULT_SOURCE)
            if self.rtm_client_helper.user not in j[DEFAULT_USERS_KEY].keys():
                j[DEFAULT_USERS_KEY][
                    self.rtm_client_helper.user
                ] = self.rtm_client_helper.channel
                ch.write_json(DEFAULT_SOURCE, j)
                self.rtm_client_helper.send_message(
                    "You've subscribed to direct messaging!"
                )
            else:
                self.rtm_client_helper.send_message(
                    "You're already subscribed"
                )
        else:
            self.rtm_client_helper.send_message(
                "Type #subscribe in a direct message")
