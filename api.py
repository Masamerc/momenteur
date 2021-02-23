import uuid

from decouple import config
from datetime import datetime
from fastapi import FastAPI
from momenteur.main import Momenteur
from pymongo import MongoClient, collection
from typing import List

app = FastAPI()

def load_to_mongo(documents: List[dict]) -> None:
    client = MongoClient(config('MONGO_URI'))
    db = client.momenteur
    collection = db.timestamped_comments
    
    for doc in documents:
        doc['_id'] = str(uuid.uuid1())
        doc['created_at'] = datetime.now()
        collection.insert(doc)


@app.get('/')
def root():
    return {"message": "ok"}


@app.get('/videos')
def get_timestamps(video_url: str) -> List[dict]:
    m = Momenteur(video_url)

    res_items = m.fetch_comments(pages=10, max_results=100)
    timestamped_comments = m.find_timestamped_comments(res_items)
    ranked_timestamped_comments = m.rank_sort_timestamps(timestamped_comments)
    final_records = m.add_timestamped_url(ranked_timestamped_comments)

    load_to_mongo(final_records)

    return final_records
