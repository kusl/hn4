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
    if (
        "title" in story_data
        and "score" in story_data
        and "url" in story_data
    ):
        print(f"\nStory: {story}")
        title = story_data.get("title")
        with open(
            f"data/{today_string}/{story}/{story}.txt", "w"
        ) as story_file:
            score = story_data["score"]
            url = story_data.get("url")
            print(url)
            story_original_html = requests.post(
                "https://archive.fo/submit", data={"url": url}
            )
    if "kids" in story_data:
        kids = story_data.get("kids")
        for kid in kids:
            comment_url = (
                f"https://hacker-news.firebaseio.com/v0/item/{kid}.json"
            )
            print(comment_url)
            comment_data = requests.get(
                comment_url,
                headers={
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                },
            ).json()
            if comment_data and (
                "deleted" not in comment_data
                or comment_data["deleted"] != "True"
            ):
                if "by" in comment_data:
                    comment_by = comment_data.get("by")
                if "text" in comment_data:
                    comment_text = comment_data.get("text")
                    continue
                if "time" in comment_data:
                    comment_time = comment_data.get("time")
                if "kids" in comment_data:
                    replies = comment_data.get("kids")
                    for kid in kids:
                        reply_url = f"https://hacker-news.firebaseio.com/v0/item/{kid}.json"
                        print(reply_url)
                        reply_data = requests.get(
                            reply_url,
                            headers={
                                "Cache-Control": "no-cache",
                                "Pragma": "no-cache",
                            },
                        ).json()
                        if reply_data and (
                            "deleted" not in reply_data
                            or reply_data["deleted"] != "True"
                        ):
                            if "by" in reply_data:
                                reply_by = reply_data.get("by")
                            if "text" in reply_data:
                                reply_text = reply_data.get("text")
                                continue
                            if "time" in reply_data:
                                reply_time = reply_data.get("time")