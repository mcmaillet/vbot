from modules.helpers import common_helper as ch

DEFAULT_SOURCE = 'data/todo.json'
DEFAULT_COMMAND = 'list'
DEFAULT_TODO_LIST = {"todo": []}


class TodoHandler:
    def __init__(self, tokens, rtm_client_helper):
        """
        Setup local source json file if it does not exist. If it does, leave it.
        :param tokens: array of string tokens
        :param rtm_client_helper: RtmClientHelper object
        """
        self.rtm_client_helper = rtm_client_helper
        try:
            ch.read_json(DEFAULT_SOURCE)
        except FileNotFoundError:
            ch.write_json(DEFAULT_SOURCE, DEFAULT_TODO_LIST)

        commands = {
            'list': self.list,
            'add': self.add,
            'remove': self.remove
        }

        if len(tokens) == 0:
            tokens = [DEFAULT_COMMAND]

        if tokens[0] in commands.keys():
            commands[tokens[0]].__call__(tokens[1:])
        else:
            self.rtm_client_helper.send_message(
                "Sorry! that todo command is not supported.")

    def list(self, trailing_tokens):
        todo = get_todo()
        if len(todo) == 0:
            self.rtm_client_helper.send_message('Your todo list is empty')
        else:
            self.rtm_client_helper.send_message(
                'Here is your current todo list:\n {}'.format(
                    '\n'.join(f"{i}) {t}"
                              for i, t in enumerate(get_todo()))
                )
            )

    def add(self, to_add):
        added = ' '.join(to_add)
        todo = get_todo()
        todo.append(added)
        write_todo(todo)
        self.rtm_client_helper.send_message(
            f"Added the following to your todo list:\n{added}")

    def remove(self, index_to_remove):
        try:
            index_to_remove = int(index_to_remove[0])
            todo = get_todo()
            if index_to_remove >= len(todo):
                self.rtm_client_helper.send_message(
                    f"Index "
                    f"{index_to_remove}"
                    f" is out of bounds. (Arrays start at 0)")
            else:
                removed = todo[index_to_remove]
                todo.pop(index_to_remove)
                write_todo(todo)
                self.rtm_client_helper.send_message(
                    f"Removed the following from your todo list:\n{removed}")
        except ValueError:
            self.rtm_client_helper.send_message(
                f"Invalid argument '"
                f"{' '.join(index_to_remove)}"
                f"', must be an integer")


def get_todo():
    return ch.read_json(DEFAULT_SOURCE)['todo']


def write_todo(todo):
    ch.write_json(DEFAULT_SOURCE, {'todo': todo})
