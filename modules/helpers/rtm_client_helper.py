def send_message(rtm_client_with_channel,
                 message):
    rtm_client_with_channel['client'].send_over_websocket(payload={
        "id": 1,
        "type": "message",
        "channel": rtm_client_with_channel['channel'],
        "text": message
    })
