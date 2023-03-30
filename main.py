from mattermostdriver import Driver
from threading import Thread
import json

from secret import TOKEN
from ws import WebSocket

bot_channels = ["717mezsoofdhbpc7pijgih9t4r"]

def delete_new_posts_in_clean_channels(driver: Driver):
    for channel in bot_channels:
        res = driver.posts.get_posts_for_channel(channel_id = channel)
        for post in res["posts"]:
            if res["posts"][post]["type"] == "system_add_to_channel":
                print(f"Reacting to post {post}")
                driver.reactions.create_reaction({
                    "user_id": driver.client.userid,
                    "post_id": res["posts"][post]["id"],
                    "emoji_name": "duck"
                    })


def main():
    driver = Driver(
            {
                'url': 'mattermost.fysiksektionen.se',
                'basepath': '/api/v4',
                'verify': True,
                'scheme': 'https',
                'port': 443,
                'auth': None,
                'token': TOKEN,
                'keepalive': True,
                'keepalive_delay': 5,
                }
            )

    driver.login()
#    ws = WebSocket()

    delete_new_posts_in_clean_channels(driver)

#    ws.subscribe("posted", )


if __name__ == "__main__":
    main()
