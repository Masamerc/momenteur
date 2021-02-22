#!/usr/env/bin/python3

import time
import json
import os
import pickle

from googleapiclient.discovery import build
from decouple import config
from typing import List
from .utils import extract_video_id, has_timestamp, create_timestamped_url
from collections import defaultdict


API_KEY = config("YOUTUBE_API_KEY")
youtube = build(serviceName='youtube', version='v3', developerKey=API_KEY)


class Momenteur(object):
    
    def __init__(self, video_url:str):
        self.video_url = video_url
        self.video_id = extract_video_id(self.video_url)
    

    def _create_request(self, max_results: int=1) -> None:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=self.video_id,
            maxResults=max_results,
            order='relevance'
        )
        return request

    
    def _extract_from_snippet(self, object: dict, element_name: str) -> str:
        return object["snippet"]["topLevelComment"]["snippet"][element_name]


    def _create_record(self, object: dict) -> dict:
        return {
            "comment": self._extract_from_snippet(object, "textOriginal"),
            "author": self._extract_from_snippet(object, "authorDisplayName"),
            "like_count": self._extract_from_snippet(object, "likeCount"),
            "updated_at": self._extract_from_snippet(object, "updatedAt")
            }
        

    def fetch_comments(self, pages: int=1, interval: int=1, max_results: int=1) -> List[dict]:

        all_items = []

        request = self._create_request(max_results)

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
    

    def find_timestamped_comments(self, all_items: List[dict]) -> List[dict]:

        comments_list = [self._create_record(item) for item in all_items]

        timestamped_comments  = []

        for comment in comments_list:
            timestamp_match = has_timestamp(comment['comment'])

            if timestamp_match:
                timestamped_comments.append(
                    {'comment':comment['comment'].replace('\n', ' '),
                    'timestamp':timestamp_match.group(1)}
                    )

        return timestamped_comments


    def rank_sort_timestamps(self, timestamped_comments: List[dict]) -> List[dict]:
        count = defaultdict(list)

        for pair in timestamped_comments:
            count[pair['timestamp']].append(pair['comment'])

        sorted_keys = sorted(count, key=lambda k: len(count[k]), reverse=True)
        sorted_count = [{'timestamp':key, 'comments': count[key], 'comment_count': len(count[key])} for key in sorted_keys]

        return sorted_count


    def add_timestamped_url(self, ranked_sorted_timestamps: List[dict]) -> List[dict]:
        for record in ranked_sorted_timestamps:
            record['url'] = create_timestamped_url(self.video_url, record['timestamp'])
        
        return ranked_sorted_timestamps


    #### for development ####
    def _load_items(self, path=os.path.join(os.getcwd(), 'sample_data/sample_items.pkl')) -> List[dict]:
        with open(path, 'rb') as f:
            data = pickle.load(f)

        return data


if __name__ == "__main__":

    m = Momenteur('https://www.youtube.com/watch?v=tFjNH9l6-sQ')

    # res_items = m.fetch_comments(pages=5, max_results=100)
    res_items = m._load_items()
    timestamped_comments = m.find_timestamped_comments(res_items)
    ranked_timestamped_comments = m.rank_sort_timestamps(timestamped_comments)
    final_records = m.add_timestamped_url(ranked_timestamped_comments)
