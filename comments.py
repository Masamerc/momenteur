#!/usr/env/bin/python3

import sys
import time
import json

from googleapiclient.discovery import build
from decouple import config
from typing import List, Tuple
from utils import extract_timestamp, extract_video_id, has_timestamp


API_KEY = config("YOUTUBE_API_KEY")

youtube = build(serviceName='youtube', version='v3', developerKey=API_KEY)


def create_request(video_id: str, max_results: int=1) -> None:
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=max_results,
        order='relevance'
    )
    return request


def extract_from_snippet(object: dict, element_name: str) -> str:
    return object["snippet"]["topLevelComment"]["snippet"][element_name]


def create_record(object: dict) -> dict:
    return {
        "comment": extract_from_snippet(object, "textOriginal"),
        "author": extract_from_snippet(object, "authorDisplayName"),
        "like_count": extract_from_snippet(object, "likeCount"),
        "updated_at": extract_from_snippet(object, "updatedAt")
        }


def extract_timestamped_comments(iterable: List[str]) -> List[Tuple[str]]:
    timestamped_comments  = []

    for comment in iterable:
        timestamp_match = has_timestamp(comment['comment'])

        if timestamp_match:
            timestamped_comments.append((comment['comment'], timestamp_match.group(1)))

    return timestamped_comments


def fetch_comments(video_id: str, pages: int, interval: int=1, max_results: int=1) -> List[dict]:

    all_items = []

    request = create_request(video_id, max_results)

    for idx in range(pages):
        res = request.execute()
        all_items += res['items']
        
        request = youtube.commentThreads().list_next(request, res)

        time.sleep(interval)

    return all_items


if __name__ == "__main__":

    # target_url = sys.argv[1]
    # video_id = extract_video_id(target_url)

    ### getting multiple-page worth of data ###
    all_items = fetch_comments('yllMFY1Mb08', pages=5, max_results=100)


    # comments_list = [create_record(item) for item in all_items]
    # timestamed_comments = extract_timestamped_comments(comments_list)


    # comments_list.sort(key=lambda x: x["like_count"], reverse=True)

    ### sunp to text ###
    # with open(f'comments_dump_{video_id}.txt', 'w') as f:
    #     for comment in comments_list:
    #         f.write(comment["author"])
    #         f.write('\n')
    #         f.write(comment['comment'])
    #         f.write('\n')
    #         f.write(f"Likes: {comment['like_count']}")
    #         f.write('\n')
    #         f.write('-'*50)
    #         f.write('\n')

    ### find timestamps ###
    # all_texts = " ".join([comment['comment'] for comment in comments_list])
    # timestamps = extract_timestamp(all_texts)
    # print(timestamps)

