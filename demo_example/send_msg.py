import os
import requests


GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = os.environ.get("EAANkab9YU5EBAA7ZBLbvFJqdvsRSYmxHuakZCbSZAloDWtbgsDyHfYNb4K4QMznqQqISr6mDp8M9wI7HNKj0kXFsr4FJ7rOnKvtIO47hLAjIIxtLqZBlC7IuXFdrl8eZAStzWCyhiIgG7lYpUzokSVdsqsGJKtsyhnIKXWNrcKXkZCm3sfnyX0")
def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response.text
