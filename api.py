import uuid

from decouple import config
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from momenteur.main import Momenteur
from pymongo import MongoClient, collection
from typing import List
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlInput(BaseModel):
    video_url: str


class TimeStampRecord(BaseModel):
    timestamp: str
    comments: List[str]
    comment_count: int
    url: str
    video_id: str
    duration_s: int
    _id: str
    created_at: datetime


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


@app.post('/videos', response_model=List[TimeStampRecord], status_code=200)
def get_timestamps(payload: UrlInput) -> List[dict]:
    m = Momenteur(payload.video_url)

    res_items = m.fetch_comments(pages=10, max_results=100)
    timestamped_comments = m.find_timestamped_comments(res_items)
    ranked_timestamped_comments = m.rank_sort_timestamps(timestamped_comments)
    final_records = m.add_timestamped_url(ranked_timestamped_comments)

    load_to_mongo(final_records)
    
    return final_records


@app.get('/testing/videos', status_code=200)
def get_timestamps_for_dev() -> List[dict]:
    m = Momenteur('https://www.youtube.com/watch?v=tFjNH9l6-sQ')
    res_items = m._load_items()
    timestamped_comments = m.find_timestamped_comments(res_items)
    ranked_timestamped_comments = m.rank_sort_timestamps(timestamped_comments)
    final_records = m.add_timestamped_url(ranked_timestamped_comments)

    return final_records