#!/usr/bin/env python3

import os, time, random, requests, datetime
from dataclasses import dataclass
from ast import literal_eval

while True:
    import os, shutil

    folder = "data"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))
    try:
        today = datetime.date.today()
        today_string = today.strftime("%Y%m%d")
        top_stories = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
        ).json()
        with open("hn", "w") as hn:
            # hn.write(f"\nTop Stories: {repr(top_stories)}\n")
            for story in top_stories:
                story_data = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story}.json",
                    headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
                ).json()
                try:
                    os.makedirs(f"data/{today_string}", exist_ok=True)
                except Exception as err:
                    print(str(err))
                    # open("err", "a").write(str(err))
                    continue
                try:
                    os.makedirs(f"data/{today_string}/{story}", exist_ok=True)
                except Exception as err:
                    print(str(err))
                    # open("err", "a").write(str(err))
                    continue
                try:
                    if (
                        "title" in story_data
                        and "score" in story_data
                        and "url" in story_data
                    ):
                        hn.write(f"\nStory: {story}")
                        print(f"\nStory: {story}")
                        title = story_data.get("title")
                        with open(
                            f"data/{today_string}/{story}/{story}.txt", "w"
                        ) as story_file:
                            # story_file.write(f"\nTitle: {title}")
                            score = story_data["score"]
                            # story_file.write(f"\nScore: {score}")
                            url = story_data.get("url")
                            print(url)
                            # story_file.write(f"\nURL: {url}\n")
                            story_file.write(f"\nRaw Story: {repr(story_data)}\n")
                            story_original_html = requests.post(
                                "https://archive.fo/submit", data={"url": url}
                            )
                except Exception as err:
                    print(str(err))
                    # open("err", "a").write(str(err))
                    continue
                with open(
                    f"data/{today_string}/{story}/{story}-comment.txt", "w"
                ) as comment_file:
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
                                    # comment_file.write(f"\nComment: \n")
                                    comment_by = comment_data.get("by")
                                    # comment_file.write(f"\nComment by: {comment_by}\n")
                                if "text" in comment_data:
                                    comment_text = comment_data.get("text")
                                    # comment_file.write(
                                    #     f"\nComment text: {comment_text}\n"
                                    # )
                                    continue
                                if "time" in comment_data:
                                    comment_time = comment_data.get("time")
                                    # comment_file.write(
                                    #     f"\nComment time: {comment_time}\n"
                                    # )
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
                                                # comment_file.write(f"\nReply: \n")
                                                reply_by = reply_data.get("by")
                                                # comment_file.write(
                                                #     f"\nReply by: {reply_by}\n"
                                                # )
                                            if "text" in reply_data:
                                                reply_text = reply_data.get("text")
                                                # comment_file.write(
                                                #     f"\nreply text: {reply_text}\n"
                                                # )
                                                continue
                                            if "time" in reply_data:
                                                reply_time = reply_data.get("time")
                                                # comment_file.write(
                                                #     f"\nReply time: {reply_time}\n"
                                                # )
        os.system("date")
        # os.system("git add .")
        # os.system('git commit -m "add hn"')
        # os.system("git pull -r origin master")
        # os.system("git push origin master")
        time.sleep(60)
    except Exception as err:
        print(str(err))
        open("err", "a").write(str(err))
        continue
