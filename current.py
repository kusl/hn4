#!/usr/bin/env python3

import os, time, random, requests, datetime
from dataclasses import dataclass
from ast import literal_eval
import os, shutil

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
            print(comment_data)
            for kidkid in kids:
                kidkid_data = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story}.json",
                    headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
                ).json()
                print(kidkid_data)
