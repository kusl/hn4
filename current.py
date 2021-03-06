#!/usr/bin/env python3

import os, time, random, requests, datetime
from dataclasses import dataclass
from ast import literal_eval
import os, shutil

# {"by":"jcarpio","descendants":25,"id":24120013,"kids":[24120306,24120848,24120901,24121745,24121142,24120989],"score":16,"time":1597152193,"title":"Paper Money with an Expiration Date","type":"story","url":"https://www.npr.org/sections/money/2019/08/27/754323652/the-strange-unduly-neglected-prophet"}


@dataclass
class Item:
    """Class for Hacker News item"""

    by: str
    descendants: int
    kids: [int]
    score: int
    time: int
    title: str
    itemtype: str
    url: str
    parent: int
    text: str

    def __init__(
        self,
        by: str,
        descendants: int,
        kids: [int],
        score: int,
        time: int,
        title: str,
        itemtype: str,
        url: str,
        parent: int,
        text: str,
    ):
        super().__init__()
        self.by = by
        self.descendants = descendants
        self.kids = kids
        self.score = score
        self.time = time
        self.title = title
        self.itemtype = itemtype
        self.url = url
        self.parent = (parent,)
        self.text = text


def get_item_from_data(comment_data):
    my_item = Item(
        comment_data.get("by"),
        comment_data.get("descendants"),
        comment_data.get("kids"),
        comment_data.get("score"),
        comment_data.get("time"),
        comment_data.get("title"),
        comment_data.get("type"),
        comment_data.get("url"),
        comment_data.get("parent"),
        comment_data.get("text"),
    )
    return my_item


def recursive(kid):
    comment_url = f"https://hacker-news.firebaseio.com/v0/item/{kid}.json"
    MAX_RETRIES = 20
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    comment_data = session.get(
        comment_url, headers={"Cache-Control": "no-cache", "Pragma": "no-cache",},
    ).json()
    if comment_data is not None:
        my_item = get_item_from_data(comment_data)
        with open(f"data/{kid}.txt", "w") as comment_file:
            comment_file.write(repr(my_item))
        print(my_item)
        if "kids" in comment_data:
            itemkids = comment_data["kids"]
            for kid in itemkids:
                recursive(kid)


top_stories = requests.get(
    "https://hacker-news.firebaseio.com/v0/topstories.json",
    headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
).json()
for story in top_stories:
    recursive(story)

new_stories = requests.get(
    "https://hacker-news.firebaseio.com/v0/newstories.json",
    headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
).json()
for story in new_stories:
    recursive(story)

best_stories = requests.get(
    "https://hacker-news.firebaseio.com/v0/beststories.json",
    headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
).json()
for story in best_stories:
    recursive(story)
