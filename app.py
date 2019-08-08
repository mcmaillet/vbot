import sys
import slack

import env

from modules.handlers.message import MessageHandler


def main():
    if len(sys.argv) == 2:
        bot_token = env.get_bot_user_oauth_access_token(sys.argv[1])
    else:
        bot_token = env.get_bot_user_oauth_access_token()

    @slack.RTMClient.run_on(event="message")
    def handle_message(**payload):
        data = payload['data']
        if data is not None:
            if isinstance(data, dict):
                MessageHandler(data['text'],
                               client=rtm_client,
                               channel=data['channel'])

    rtm_client = slack.RTMClient(token=bot_token)
    rtm_client.start()


if __name__ == '__main__':
    main()
