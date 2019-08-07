import os
import json


def get_bot_user_oauth_access_token(environment='DEV'):
    key = 'BOTUSEROAUTHACCESSTOKEN'

    def get_environment_var():
        return os.environ[key]

    def get_local_env():
        return json.load(open('.env', 'r'))[key]

    return {
        'DEV': get_local_env,
        'PROD': get_environment_var
    }[environment].__call__()
