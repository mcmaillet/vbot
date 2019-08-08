class RtmClientHelper:
    def __init__(self, client, channel):
        self.client = client
        self.channel = channel

    def send_message(self, message):
        self.client.send_over_websocket(payload={
            "id": 1,
            "type": "message",
            "channel": self.channel,
            "text": message
        })
