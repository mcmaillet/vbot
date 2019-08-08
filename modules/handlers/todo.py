import json

from modules.helpers import rtm_client_helper

DEFAULT_SOURCE = 'data/todo.json'
DEFAULT_COMMAND = 'list'


class TodoHandler:
    def __init__(self, tokens, **rtm_client_with_channel):
        """
        Setup local source json file if it does not exist. If it does, leave it.
        :param tokens: array of string tokens
        :param rtm_client_with_channel: dict of client and channel
        TODO refactor to stop controlling logic with exceptions
        """
        try:
            json.load(open(DEFAULT_SOURCE, 'r', encoding='utf8'))
        except FileNotFoundError:
            json.dump({"todo": []}, open(DEFAULT_SOURCE, 'w+', encoding='utf8'))
        try:
            if len(tokens) == 0:
                tokens = [DEFAULT_COMMAND]
            {
                'list': self.list,
                'add': self.add,
                'remove': self.remove
            }[tokens[0]].__call__([token for i, token in enumerate(tokens) if i > 0], rtm_client_with_channel)
        except KeyError:
            rtm_client_helper.send_message(
                rtm_client_with_channel,
                "Sorry! that todo command is not supported.")

    def list(self, trailing_tokens, rtm_client_with_channel):
        todo = get_todo()
        if len(todo) == 0:
            rtm_client_helper.send_message(
                rtm_client_with_channel,
                'Your todo list is empty')
        else:
            rtm_client_helper.send_message(
                rtm_client_with_channel,
                'Here is your current todo list:\n {}'.format('\n'.join(f"{i}) {t}"
                                                                        for i, t in enumerate(get_todo()))))

    def add(self, to_add, rtm_client_with_channel):
        added = ' '.join(to_add)
        todo = get_todo()
        todo.append(added)
        write_todo(todo)
        rtm_client_helper.send_message(
            rtm_client_with_channel,
            f"Added the following to your todo list:\n {added}")

    def remove(self, index_to_remove, rtm_client_with_channel):
        try:
            index_to_remove = int(index_to_remove[0])
            todo = get_todo()
            if index_to_remove >= len(todo):
                rtm_client_helper.send_message(
                    rtm_client_with_channel,
                    f"Index {index_to_remove} is out of bounds. (Arrays start at 0)")
            else:
                removed = todo[index_to_remove]
                todo.pop(index_to_remove)
                write_todo(todo)
                rtm_client_helper.send_message(
                    rtm_client_with_channel,
                    f"Removed the following from your todo list:\n {removed}")
        except ValueError:
            rtm_client_helper.send_message(
                rtm_client_with_channel,
                f"Invalid argument '{' '.join(index_to_remove)}', must be an integer")


def get_todo():
    return json.load(open(DEFAULT_SOURCE, 'r', encoding='utf8'))['todo']


def write_todo(todo):
    json.dump({'todo': todo}, open(DEFAULT_SOURCE, 'w+', encoding='utf8'))
