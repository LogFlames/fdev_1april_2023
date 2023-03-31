from mattermostdriver import Driver
from threading import Thread
import json

from secret import TOKEN
from ws import WebSocket

def get_all_channels(driver: Driver, page, per_page):
    return driver.client.get(
        f'/channels?page={page}&per_page={per_page}'
    )

def add_dock_emojis(driver: Driver, channels):
    threads = []
    for channel in channels:
        res = driver.posts.get_posts_for_channel(channel_id = channel)
        for post in res["posts"]:
#            print(f"Reacting to post {post}")
            thread = Thread(target=driver.reactions.create_reaction, args = ({
                "user_id": driver.client.userid,
                "post_id": res["posts"][post]["id"],
                "emoji_name": "duck"
                },))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

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

    channels = []

    page = 0
    chans = get_all_channels(driver, page = page, per_page = 10)
    while len(chans) == 10:
        print(f"Getting channels from page: {page}")
        for chan in chans:
            channels.append(chan["id"])
        page += 1
        chans = get_all_channels(driver, page = page, per_page = 10)

    print(channels)


    channels = ["717mezsoofdhbpc7pijgih9t4r"] # remove on 1 first
    add_dock_emojis(driver, channels)


if __name__ == "__main__":
    main()
