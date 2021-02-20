from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "ok"}

@app.get('/videos/{video_id}')
def get_video(video_id: str):
    return {'video_id': video_id}