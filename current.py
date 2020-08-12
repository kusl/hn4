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


today = datetime.date.today()
today_string = today.strftime("%Y%m%d")
top_stories = requests.get(
    "https://hacker-news.firebaseio.com/v0/topstories.json",
    headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
).json()
for story in top_stories:
    story_data = requests.get(
        f"https://hacker-news.firebaseio.com/v0/item/{story}.json",
        headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
    ).json()
    if "title" in story_data and "score" in story_data and "url" in story_data:
        print(f"\nStory: {story}")
        title = story_data.get("title")
        score = story_data["score"]
        url = story_data.get("url")
        print(url)
    if "kids" in story_data:
        kids = story_data.get("kids")
        for kid in kids:
            comment_url = f"https://hacker-news.firebaseio.com/v0/item/{kid}.json"
            print(comment_url)
            comment_data = requests.get(
                comment_url,
                headers={"Cache-Control": "no-cache", "Pragma": "no-cache",},
            ).json()
            my_item = Item(
                comment_data.get('itemby'),
                comment_data.get('itemdescendants'),
                comment_data.get('itemkids'),
                comment_data.get('itemscore'),
                comment_data.get('itemtime'),
                comment_data.get('itemtitle'),
                comment_data.get('itemtype'),
                comment_data.get('itemur')
            )
            print(my_item)
            print(comment_data)
