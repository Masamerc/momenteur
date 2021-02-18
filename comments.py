#!/usr/env/bin/python3

import sys
import time
import json
import pickle

from googleapiclient.discovery import build
from decouple import config
from typing import List, Tuple
from utils import extract_timestamp, extract_video_id, has_timestamp
from collections import defaultdict


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


def fetch_comments(video_id: str, pages: int, interval: int=1, max_results: int=1) -> List[dict]:

    all_items = []

    request = create_request(video_id, max_results)

    for idx in range(pages):
        res = request.execute()
        all_items += res['items']

        request = youtube.commentThreads().list_next(request, res)

        time.sleep(interval)

    return all_items


def find_timestamped_comments(iterable: List[str]) -> List[dict]:
    timestamped_comments  = []

    for comment in iterable:
        timestamp_match = has_timestamp(comment['comment'])

        if timestamp_match:
            timestamped_comments.append(
                {'comment':comment['comment'].replace('\n', ' '),
                'timestamp':timestamp_match.group(1)}
                )

    return timestamped_comments


def rank_sort_timestamps(timestamp_comment_pairs: List[dict]) -> List[dict]:
    count = defaultdict(list)

    for pair in timestamp_comment_pairs:
        count[pair['timestamp']].append(pair['comment'])

    sorted_keys = sorted(count, key=lambda k: len(count[k]), reverse=True)
    sorted_count = [{key:count[key]} for key in sorted_keys]

    return sorted_count


if __name__ == "__main__":

    target_url = sys.argv[1]
    video_id = extract_video_id(target_url)

    ### getting multiple-page worth of data ###
    all_items = fetch_comments(video_id, pages=2, max_results=50)

    comments_list = [create_record(item) for item in all_items]
    timestamed_comments = find_timestamped_comments(comments_list)
    final_ranked_timestamps = rank_sort_timestamps(timestamed_comments)


    # with open('dump_ranked_ts.json', 'w') as f:
    #     json.dump(final_ranked_timestamps, f)

