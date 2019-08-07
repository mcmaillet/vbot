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
        if data is not None and isinstance(data, dict):
            message = data['text']
            if message.lower().strip() == 'hello':
                rtm_client.send_over_websocket(payload={
                    "id": 1,
                    "type": "message",
                    "channel": data['channel'],
                    "text": f":tada: Hello <@{data.get('user')}>! :tada:"
                })
            MessageHandler(message,
                           client=rtm_client,
                           channel=data['channel'])

    rtm_client = slack.RTMClient(token=bot_token)
    rtm_client.start()


if __name__ == '__main__':
    main()
