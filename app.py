import sys
import slack

import __env__

if __name__ == '__main__':
    if len(sys.argv) == 2:
        bot_token = __env__.get_bot_user_oauth_access_token(sys.argv[1])
    else:
        bot_token = __env__.get_bot_user_oauth_access_token()


    @slack.RTMClient.run_on(event="message")
    def handle_message(**payload):
        data = payload['data']
        if data.get('text').lower().strip() == 'hello':
            rtm_client.send_over_websocket(payload={
                "id": 1,
                "type": "message",
                "channel": data.get("channel"),
                "text": f":tada: Hello <@{data.get('user')}>! :tada:"
            })


    rtm_client = slack.RTMClient(token=bot_token)
    rtm_client.start()
