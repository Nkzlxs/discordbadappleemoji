import requests
import os
import json
import time

import pngToPixel

base_url = "https://discord.com/api"
version = "/v8"

TOKEN = os.environ['bot_token']

_headers = {
    "Authorization": "Bot %s" % TOKEN,
    "Content-Type": "application/json"
}

session_obj = requests.Session()
session_obj.headers.update(_headers)


mappings = {
    "0000": "<:0:818437634837184544>",
    "0001": "<:0:818437632613810186>",
    "0010": "<:0:818437632224002059>",
    "0011": "<:0:818437632555745312>",
    "0100": "<:0:818437632866123776>",
    "0101": "<:0:818437632832045066>",
    "0110": "<:0:818437632810811412>",
    "0111": "<:0:818437634941911040>",
    "1000": "<:0:818437632874512404>",
    "1001": "<:0:818437632870055957>",
    "1010": "<:0:818437632937295912>",
    "1011": "<:0:818437632803340329>",
    "1100": "<:0:818437632949747712>",
    "1101": "<:0:818437632706478091>",
    "1110": "<:0:818437632950403082>",
    "1111": "<:0:818437632987496479>",
}


def emojiTable_to_String(emoji_table):
    final_str = ""
    for y in range(8):
        for x in range(10):
            final_str += mappings[emoji_table[y][x]]
        final_str += '\n'

    return final_str


def sendPlaceHolder(session_obj):
    query = "/channels/818493590446800946/messages"

    """ Frame -1 placeholder """
    d = {
        "content": "Frame -1\n"
    }
    res = session_obj.post(
        url=base_url+version+query,
        data=json.dumps(d)
    )

    """ Get last msg id and construct query for Editing Message """
    last_msg_id = json.loads(res.text)['id']

    return last_msg_id


def singleEdit(session_obj, last_msg_id, frame_no, frame):

    query = "/channels/818493590446800946/messages/%s" % last_msg_id

    d = {
        "content": "Frame: %d\n%s" % (frame_no, frame)
    }

    res = session_obj.patch(
        url=base_url+version+query,
        data=json.dumps(d)
    )

    return res


if __name__ == '__main__':

    i = 1
    last_msg_id = sendPlaceHolder(session_obj)
    for _ in range(7777):
        im = pngToPixel.imageToGrayScale(f"test_images/{i+_:04d}.png")
        res = pngToPixel.calc_average_grayscale(im)
        emoji_table = pngToPixel.generateEmojiTable(res, 200)

        frame = emojiTable_to_String(emoji_table)
        response = singleEdit(session_obj, last_msg_id, i+_, frame)
        print(response)

        time.sleep(0.3)
