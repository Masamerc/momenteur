#!/usr/env/bin/python3

import sys
import time
import json
import pickle

from googleapiclient.discovery import build
from decouple import config
from typing import List, Tuple
from utils import extract_timestamp, extract_video_id, has_timestamp, create_timestamped_url
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
        try:
            res = request.execute()
            all_items += res['items']

            request = youtube.commentThreads().list_next(request, res)

            time.sleep(interval)
        except Exception as e:
            print('request could not execute.')
            print(e)    

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
    sorted_count = [{'timestamp':key, 'comments': count[key]} for key in sorted_keys]

    return sorted_count


def add_timestamped_url(ranked_sorted_timestamps: List[dict], video_url: str) -> List[dict]:
    for record in ranked_sorted_timestamps:
        record['url'] = create_timestamped_url(video_url, record['timestamp'])
    
    return ranked_sorted_timestamps


#### for development ####
def load_items() -> List[dict]:
    with open('sample_data/sample_items.pkl', 'rb') as f:
        data = pickle.load(f)

    return data


if __name__ == "__main__":

    # target_url = sys.argv[1]
    # video_id = extract_video_id(target_url)
    

    ### getting multiple-page worth of data ###
    # all_items = fetch_comments(video_id, pages=5, max_results=100)
    
    #### for development ####
    all_items = load_items()
    target_url = 'https://www.youtube.com/watch?v=tFjNH9l6-sQ'
    video_id = 'tFjNH9l6-sQ'

    comments_list = [create_record(item) for item in all_items]
    timestamed_comments = find_timestamped_comments(comments_list)
    ranked_timestamps = rank_sort_timestamps(timestamed_comments)
    final_records = add_timestamped_url(ranked_timestamps, target_url)


    with open('sample_data/dump_ranked_ts.json', 'w') as f:
        json.dump(final_records, f, indent=2)

