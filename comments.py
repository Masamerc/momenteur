#!/usr/env/bin/python3

import os
from googleapiclient.discovery import build
from decouple import config

API_KEY = config("YOUTUBE_API_KEY")

youtube = build(serviceName='youtube', version='v3', developerKey=API_KEY)


def fetch_commentThreads(video_id: str, num_results: int) -> None:
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=num_results,
        order='relevance'
    )
    return request.execute()


def extract_element(object: dict, element_name: str) -> str:
    return object["snippet"]["topLevelComment"]["snippet"][element_name]


def create_comment_date(object: dict) -> dict:
    return {
        "comment": extract_element(object, "textOriginal"),
        "author": extract_element(object, "authorDisplayName"),
        "like_count": extract_element(object, "likeCount"),
        "updated_at": extract_element(object, "updatedAt")
        }


if __name__ == "__main__":

    comments = fetch_commentThreads('GXZlZCcJAGs', 50)
    items = comments["items"]

    comments_list = [create_comment_date(item) for item in items]
    # comments_list.sort(key=lambda x: x["like_count"])

    with open('comments_dump.txt', 'w') as f:
        for comment in comments_list:
            f.write(comment["author"])
            f.write('\n')
            f.write(comment['comment'])
            f.write('\n')
            f.write(f"Likes: {comment['like_count']}")
            f.write('\n')
